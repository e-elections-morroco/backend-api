# Use an official Python runtime as a parent image
FROM python:3.9
LABEL authors="ouail laamiri"

# Install necessary system dependencies for dlib
RUN apt-get update && apt-get install -y --no-install-recommends  && apt-get install -y libgl1-mesa-glx\
        build-essential \
        cmake \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Specify the CMD as an array
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--log-level", "info"]
