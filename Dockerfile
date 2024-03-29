# Description: Dockerfile for the Flask app

# Use the official image as a parent image
FROM python:3.11.0a1-alpine3.14

# Set the working directory in the container
COPY ./requirements.txt /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Install the required libraries
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
