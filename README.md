# DFactory Custom Blender Add-On
Custom Blender Add-On developed for supporing production of DFactory team, leveraging open-source LLM for cost optimizitation.

## Project Structures ##
```
├──agent\                   # Folder for configuring Open Source LLM codebase.
├──logs\                    # Folder for storing FastAPI server logs.
├──script\                  # Folder for shell scripts to automate tasks.
│   ├──run_test.sh          # Script to start the FastAPI testing based on dynamic environment.
│   ├──run_server.sh        # Script to start the FastAPI server based on dynamic environment.
│   ├──setup.sh             # Script to install and configure project dependencies.
├──src\                     # Main folder containing the core application code.
│   ├──routers\             # Folder for API route definitions.
│   ├──schema\              # Folder for defining request and response formats for the API.
│   ├──main.py              # The main file to launch the FastAPI application.
│   ├──secret.py            # File for managing sensitive information from the .env file.
├──utils\                   # Folder for utility functions and tools used across the project.
│   ├──error.py             # Custom error handling for interactions with external services.
│   ├──exception.py         # Register custom error hanlder to FastAPI.
│   ├──helper.py            # General-purpose helper functions.
│   ├──logger.py            # Logging setup for tracking errors and system activities.
pyproject.toml              # Configuration file listing all required libraries and dependencies.
```


# Project Setup Instructions
This project is developed using Windows 11 with Python v3.12.3. To get started, you'll need to install Docker and Poetry.


## Prerequisites

- **Python** (Recomendation: 3.12+)
- **Docker**
- **Poetry**

## Setup steps

1. **Build docker images**
    ```
    docker build -t custom-blender-addon .
    ```

2. **Run docker images**
    ```
    docker run --name=custom-blender-dev -p 10000:10000 custom-blender-addon --development
    ```

3. **Access Backend Service via IP Address**
    ```
    http://{ip_address}:10000/docs
    ```


# Repo Owner? #
* Bastian Armananta
