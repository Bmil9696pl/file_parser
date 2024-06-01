### Comprehensive Documentation for Setup, Operation, and Interaction with the File Processing Service

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
    - [Clone the Repository](#clone-the-repository)
    - [Configure Environment Variables](#configure-environment-variables)
    - [Build and Run Docker Containers](#build-and-run-docker-containers)
5. [Accessing the Service](#accessing-the-service)
6. [Interacting with the Service](#interacting-with-the-service)
7. [Monitoring with Prometheus](#monitoring-with-prometheus)
8. [Accessing and Interpreting Metrics](#accessing-and-interpreting-metrics)
9. [Stopping the Service](#stopping-the-service)

---

## Introduction

This document provides comprehensive instructions to set up, operate, and interact with the File Processing Service. It also includes guidelines on how to access and interpret metrics using Prometheus.

## Prerequisites

Before setting up the service, ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Project Structure

```
project_root/
    ├── fileparser/
    │   ├── Dockerfile
    │   ├── Dockerfile-prometheus
    │   ├── docker-compose.yml
    │   ├── prometheus.yml
    │   ├── requirements.txt
    │   ├── manage.py
    │   ├── fileparser/
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── FileProcessor.py
    │   │   ├── parser.py
    │   │   ├── views.py
    │   └── ...
    ├── example.csv
    ├── example.json
    ├── example.txt
    └── request.py
```

## Setup Instructions

### Clone the Repository

Clone the repository to your local machine:

```sh
git clone https://github.com/Bmil9696pl/file_parser.git
cd file_parser
```

### Build and Run Docker Containers

Build and run the Docker containers using Docker Compose:

```sh
docker-compose up --build
```

This will build the images and start the services defined in `docker-compose.yml`.

## Accessing the Service

- **Django Application**: The Django application will be accessible at `http://localhost:8000`.
- **Prometheus UI**: The Prometheus UI will be accessible at `http://localhost:9090`.

## Interacting with the Service

The service provides an endpoint to upload and process files.

- **Endpoint**: `/parse/`
- **Method**: POST
- **Payload**: Form-data with a file field named `file`.

You can send files to this endpoint by running the "request.py" file.

### Example Request using `request.py`:

```sh
python request.py
```

### Example Response:

```json
{
    "file_type": "TXT", 
    "num_lines": 22, 
    "num_words": 108, 
    "num_chars": 799, 
    "emails": ["alice@example.com", "bob.smith@example.co.uk", "charlie123@example.org"], 
    "phone_numbers": ["1234567890", "0987654321", "7777777777"], 
    "names": ["Alice Someone", "Bob Smith", "Charlie Coolguy"]
}
```

## Monitoring with Prometheus

Prometheus is set up to monitor the service. The metrics are exposed by the Django application and can be scraped by Prometheus.

### Prometheus Configuration (`prometheus.yml`):

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['host.docker.internal:8000']
```

## Accessing and Interpreting Metrics

1. **Access Prometheus UI**: Navigate to `http://localhost:9090` in your browser.

2. **Metrics Available**:
    - `files_processed_total`: Total number of files processed.
    - `file_processing_time_seconds`: Time spent processing files.

### Example Queries:

- **Total Files Processed**:

    ```promql
    files_processed_total
    ```

- **File Processing Time**:

    ```promql
    file_processing_time_seconds
    ```

These metrics can be visualized in the Prometheus UI.

## Stopping the Service

To stop the running containers, use the following command:

```sh
docker-compose down
```

This will stop and remove the containers, networks, and volumes defined in your `docker-compose.yml`.

---

This documentation provides detailed steps for setting up, running, interacting with, and monitoring the File Processing Service. Ensure to follow each step closely to successfully deploy and manage the service. If you encounter any issues or have further questions, refer to the official documentation for Docker, Docker Compose, Django, and Prometheus.