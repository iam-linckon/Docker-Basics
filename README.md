<p align="center">
  <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white" />
  <img src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>


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

## Create Project via Spring CLI

```bash
spring init --groupId=com.example --artifactId=demo-maven --name=spring-boot-maven-app --dependencies=web --boot-version=3.4.0 --build=maven 
     spring-boot-maven-app

# unzip the project

unzip demo-maven.zip -d spring-boot-maven-app
```
**A*dd GrettingController.java in spring-boot-maven-app/src/main/java/com/example/demo_maven path***
```java
package com.example.demo_maven;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingController {
  @Value("${SPRING_PROFILES_ACTIVE:default}")
  private String profile;

  @GetMapping("/")
  public String greet() {
    return "Spring profile is: " + profile;
  }
}
```
## Build and Run Locally

```bash
cd spring-boot-app
./mvnw clean package -DskipTests
SPRING_PROFILES_ACTIVE=LocalDev java -jar target/demo-maven-0.0.1-SNAPSHOT.jar
```
***Verify***
```bash
> curl http://localhost:8080
Spring profile is: LocalDev
```

## Build,Run and Push

```bash
> cd spring-boot-app
> docker build -t linckon/spring-boot-app:v1 . 
> docker run -e SPRING_PROFILES_ACTIVE=LocalDev -p 8081:8080 linckon/spring-boot-app:v1
> curl http://localhost:8081
Spring profile is: LocalDev
> docker push linckon/spring-boot-app:v1
```

***Pull and Test Locally***
```bash
> docker rmi linckon/spring-boot-app:v1 --force
> docker pull linckon/spring-boot-app:v1
> docker run -e SPRING_PROFILES_ACTIVE=LocalDev -p 8081:8080 linckon/spring-boot-app:v1
```

## Docker Compose

***docker-compose.yml***

```yaml
version: '3.8'

services:
  python-app:
    image: linckon/python-app:v1
    container_name: python-app
    ports:
      - "5000:5000"
    environment:
      - MY_ENV_VAR=Running_From_python-app_Container

  spring-boot-app:
    image: linckon/spring-boot-app:v1
    container_name: spring-boot-app
    ports:
      - "8081:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=Running_From_spring-boot-app_Container
    depends_on:
      - python-app

```

  ***Start and Verify***

  ```bash
    > docker-compose up -d
    > docker ps
    CONTAINER ID   IMAGE                        COMMAND                CREATED              STATUS         PORTS                                         NAMES
    e9bb5cf55463   linckon/spring-boot-app:v1   "java -jar /app.jar"   About a minute ago   Up 6 seconds   0.0.0.0:8081->8080/tcp, [::]:8081->8080/tcp   spring-boot-app
    c96883e482e1   linckon/python-app:v1        "python app.py"        About a minute ago   Up 7 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp     python-app

    # Verify Python application
    > curl http://localhost:5000/
    # MY_ENV_VAR is: Running_From_python-app_Container

    # Verify Spring Boot application
    > curl http://localhost:8081/
    # Spring profile is: Running_From_spring-boot-app_Container
  ```

  ## Conclusion
    Now we have:

    - A Flask-based Python service run locally or containerized, accepting runtime environment variables.

    - A Spring Boot application run locally or containerized, configured via environment variables.

    - A Docker Compose setup that ensures the Spring Boot container starts only after the Python container is up.
