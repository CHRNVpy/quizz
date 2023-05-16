# Use the official Python image as the base
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container and install dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files to the container
COPY . /app

# Expose the port that FastAPI listens on
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

