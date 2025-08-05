# Docker Basics

## Overview

This document provides step-by-step instructions for:

- Containerizing a Python application and handling environment variables at runtime.

- Containerizing a Spring Boot application and orchestrating service dependencies with Docker Compose.

**Note**: We will not use any environment files (.env) to build the images. All environment variables will be passed at run time.

## Prerequisites

- Docker CLI installed (version >= 20.x)

- Python 3.9+ & pip (for local Flask run)

- Docker Hub account (or any container registry)

- Java JDK 17+ (for Spring Boot)

- Maven (to generate the Spring Boot JAR)

- Spring Boot CLI (optional, for project initialization)

## Python Application

***Project Structure***

```tree
python-app/
├── Dockerfile
├── app.py
├── requirements.txt

```
***Source Code***

```python
# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    env_var = os.getenv('MY_ENV_VAR', 'Not Set')
    return f'MY_ENV_VAR is: {env_var}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
```txt
# requirements.txt
Flask
```
***Run Flask App Locally***
```bash
> cd python-app
> pip install -r requirements.txt
> export MY_ENV_VAR=LocalTest
> python3 app.py
```

```
# output
> curl http://localhost:5000
MY_ENV_VAR is: LocalTest
```
***Dockerfile***

```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

***Build and Run Docker Container***

```bash
> cd python-app
> docker build -t linckon/python-app:latest .
> docker run -d \
  --name python-app \
  -p 5000:5000 \
  -e MY_ENV_VAR=HelloContainer \
  linckon/python-app:latest
```

***Push to Registry***
```bash
> docker push linckon/python-app:v1
```
***Pull and Test Locally***
```bash
> docker stop python-app
> docker rm python-app
> docker rmi linckon/python-app:v1
> docker pull linckon/python-app:v1
> docker run -d \
  --name python-app \
  -p 5000:5000 \
  -e MY_ENV_VAR=HelloAgain \
  linckon/python-app:latest
```
```bash
> curl http://localhost:5000
MY_ENV_VAR is: HelloAgain
```
## Spring Boot Application
