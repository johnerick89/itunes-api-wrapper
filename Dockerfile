# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container at /app
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Define environment variables
ENV DJANGO_SETTINGS_MODULE=itunes_api_wrapper.settings

# Start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
