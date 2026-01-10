# Use official Python runtime
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (main.py, agent_brain.py, faiss_index, etc.) to /app
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the application
# Since main.py is right here, we just call "main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]