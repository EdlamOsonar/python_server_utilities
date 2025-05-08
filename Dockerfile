# Use an official Python image
FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

# Uninstall any conflicting logging package
RUN pip uninstall -y logging || true

# Install pip dependencies
RUN pip install --no-cache-dir --upgrade pip

RUN pip install  -r requirements.txt 

# Copy the application code into the container
COPY ./domain_tools ./domain_tools

# Expose the application port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "domain_tools.main:app", "--host", "0.0.0.0", "--port", "8000"]