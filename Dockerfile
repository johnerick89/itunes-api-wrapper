# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install Celery
# Install setuptools, numpy, celery
RUN apk update && \
    apk add --no-cache python3-dev build-base && \
    apk add --no-cache postgresql-dev && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools && \
    python3 -m pip install wheel && \
    python3 -m pip install celery && \
    pip install --no-cache-dir -r requirements.txt

# Copy the Celery configuration file into the container
COPY ./itunes-api-wrapper/celery_conf.py /app/

# Set the environment variable for the Celery command
ENV C_FORCE_ROOT=1


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container at /app
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Define environment variables
ENV DJANGO_SETTINGS_MODULE=itunes-api-wrapper.settings

# Start the server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

