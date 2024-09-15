# Step 1: Use an official Python runtime as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . .

# Step 4: Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port the app runs on (adjust if needed)
EXPOSE 5000

# Step 6: Set environment variables (Optional: You can configure Flask-specific settings here)
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Step 7: Run the application (Assuming you are starting the app via main.py)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
