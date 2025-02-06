# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV TELEGRAM_TOKEN=your_telegram_token_here

# Expose any necessary ports (if applicable)
# EXPOSE 8080

# Run the bot
CMD ["python", "bot.py"]
