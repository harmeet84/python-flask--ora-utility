# Use the official Python image from the Docker Hub
FROM docker-staging.alf.uk/python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the pip.conf file into the container
COPY pip.conf /etc/pip.conf

# Copy the requirements file into the container
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
#COPY . .

# Set the environment variable to tell Flask to run in development mode
#ENV FLASK_ENV=development

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
