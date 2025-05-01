import sys
import os
import requests
import httpx
import logging
import threading
import time
import schedule
import json
from typing import Union, List
from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from config.config import bearer_token_dns
from config.config import zone_id
from config.config import account_id
from config.config import domain_name


app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir,  'config'))


# Configure logging
logging.basicConfig(
    filename="ip_change.log",  # Log file name
    level=logging.WARN,   # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)


headers = {
    "Authorization": f"Bearer {bearer_token_dns}",
    "Accept": "application/json"
}

# configure scheduler
timer = 60#21600 #  segundos (6 horas)
scheduler = BackgroundScheduler()

@app.post("/domain/dns/auto_update_ip/force")
def autoUpdateDNS():
    actual_ip = getMyIP()
    ip = actual_ip["ip"]
    dns_records = checkMyDns()
    
    result = {"updated": [], "not_updated": []}
    for item in dns_records["result"]:
        if(item["content"] == str(ip)):
            result["not_updated"].append(item)
        else:
            old_dns = item["id"]
            updated = updateMyDns(old_dns, ip)
            result["updated"].append(updated)
    json_string = json.dumps(result)
    
    logging.warn("Auto Update DNS Task Executed with result : " + json_string)      
    return result

scheduler.add_job(autoUpdateDNS, 'interval', seconds=timer, id="dns_task")  
scheduler.start()

@app.get("/")
def read_root():
    return {"Domain Server Utilities": "Running!!"}

@app.get("/domain/verify") 
def tokenVerify():
    url = "https://api.cloudflare.com/client/v4/accounts/" + account_id + "/tokens/verify"

    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        return("Success:", response.json())  # Parse the JSON response if needed
    else:
        return("Error:", response.status_code, response.text)

@app.get("/domain/dns/list")       
def checkMyDns():
    url = "https://api.cloudflare.com/client/v4/zones/"+ zone_id + "/dns_records"
    headers = {
        "Authorization": f"Bearer {bearer_token_dns}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

@app.post("/domain/dns/update")       
def updateMyDns(record_id: str, new_ip: str):
    headers = {
        "Authorization": f"Bearer {bearer_token_dns}",
        "Accept": "application/json"
    }
    
    url = f"https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records/" + record_id

    data = {
        "type": "A",
        "name": domain_name,
        "content": new_ip,
        "ttl": 120,
        "proxied": True
    }

    response = requests.put(url, headers=headers, json=data)
    
    return response.json()

@app.get("/domain/ip")
def getMyIP():
    response = httpx.get("https://api64.ipify.org?format=json")
    print(response)
    
    result = response.json()
    
    return result

@app.get("/domain/dns/auto_update_task/schedule_timer")
def get_schedule_timer():
    return {"DNS task scheduled in seconds: ": timer }


""" @app.post("/domain/dns/auto_update_task/update_schedule_timer")
def update_schedule_timer(new_timer: int):
    timer = new_timer
    scheduler.pause()
    scheduler.reschedule_job('dns_task', trigger='cron', minute=timer)
    scheduler.resume()
    return {"new timer:":  new_timer,
            "Task status: ": scheduler.state} """
   

@app.post("/domain/dns/auto_update_task/update_status")
def auto_update_task_change_status(status: str):
    if status == "START" and scheduler.state != 1:
       scheduler.start()
    elif status == "STOP" and scheduler.state != 0:
        scheduler.shutdown()

    return {"Task status: " : scheduler.state }
        

    



    

