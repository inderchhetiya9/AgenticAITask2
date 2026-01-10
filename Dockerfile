# Use official Python runtime
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code (including app/, faiss_index/, etc.)
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# Adjust "app.main:app" if your main file is named differently
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]