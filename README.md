# Cloudflare domain tools 

### Update DNS routing for dynamic public ip
* Provides rest enspoints to check the dns ip redirection
* An scheduler starts with the server , the task updates the dns routing with the current public ip 
* Enpoint list collection in request_collection folder

### Compilation
    pip install -r requirements.txt

### Start server
    uvicorn main:app -reload           

## Docker build
    docker build -t domain_tools:1.0.0 .                                                                                       