# Use an official Python runtime as a parent image
FROM python:3.9
LABEL authors="ouail laamiri"

# Install necessary system dependencies for dlib
RUN apt-get update
RUN apt-get install -y --no-install-recommends
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y build-essential
RUN apt-get install -y cmake
RUN apt-get install -y git
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Specify the CMD as an array
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--log-level", "info"]
