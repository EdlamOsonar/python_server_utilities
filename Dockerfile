# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /python_server_utilities

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt

RUN pip --version

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the FastAPI app into the container
COPY ./domain_tools /code/app

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
