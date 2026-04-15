# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# (We create a minimal requirements.txt for the container if needed)
RUN pip install --no-cache-dir -r requirements.txt

# Install Git for Senior Mode
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Define environment variable
ENV NAME NeuroSysGodMode

# Run main.py when the container launches
ENTRYPOINT ["python", "main.py"]
CMD ["scan"]
