# Set up a base image for your container
FROM python:3.10.11

# Create a working directory within your container fro your application
WORKDIR /app

# Copy the content of my requirements.txt into a temp directory in the container
COPY requirements.txt /tmp/requirements.txt

# Install packages in the requirements.txt file
RUN python -m pip install --timeout 300000 -r /tmp/requirements.txt

# Copy all files and folders into the container's working directory
COPY . /app

# Expose port 8077 outside the container
EXPOSE 80 

# Run the fastapi application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]