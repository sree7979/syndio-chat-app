# Use official Python 3.9 image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the app will run
EXPOSE 8000

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
