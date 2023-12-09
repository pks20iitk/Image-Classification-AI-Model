# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y \
    git \
    awscli \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Rust toolchain
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH $PATH:/root/.cargo/bin

# Set the path to pg_config
ENV PATH /path/to/pg_config:$PATH

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the application
CMD ["python3", "app.py"]
