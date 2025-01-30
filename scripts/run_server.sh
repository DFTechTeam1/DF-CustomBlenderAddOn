#!/bin/sh

# Show usage information
show_help() {
  echo "Usage: sh $0 [ --development | --staging | --production | --help ]"
  echo ""
  echo "--development    Run the server on localhost and load the .env.development file"
  echo "--staging        Run the server on the staging IP and load the .env.staging file"
  echo "--production     Run the server on the production IP address and load the .env.production file"
  echo "--help           Show this help message"
}

# Check command-line arguments
if [ "$1" = "--help" ]; then
  show_help
  exit 0
fi

# Parse arguments
case "$1" in
  --development)
    echo "Using development environment configuration"
    ENV_FILE="env/.env.development"
    HOST="127.0.0.1"
    DEBUG_MODE="--reload --reload-dir=src"
    ;;
  --staging)
    echo "Using staging environment configuration"
    ENV_FILE="env/.env.staging"
    HOST="0.0.0.0"
    DEBUG_MODE=""
    ;;
  --production)
    echo "Using production environment configuration"
    ENV_FILE="env/.env.production"
    HOST="0.0.0.0"
    DEBUG_MODE=""
    ;;
  *)
    echo "Invalid option: $1"
    show_help
    exit 1
    ;;
esac

# Load the environment variables using the external script
export ENV_FILE
sh scripts/load_env.sh

# Checking OS Environment
echo "Checking OS Environment"
if grep -qEi "(Microsoft|WSL)" /proc/version &>/dev/null; then
  echo "WSL detected"
  . .venv/bin/activate
else
  case "$OSTYPE" in
    linux*)
      echo "Linux based OS detected"
      source .venv/bin/activate
      ;;
    darwin*)
      echo "macOS detected"
      source .venv/bin/activate
      ;;
    cygwin* | msys* | mingw*)
      echo "Windows based OS detected"
      source .venv/Scripts/activate
      ;;
    *)
      echo "Unsupported OS. Please activate venv and run the server manually."
      exit 1
      ;;
  esac
fi

# Start the server
echo "Running uvicorn server"
uvicorn src.main:app --host "$HOST" --port 8000 $DEBUG_MODE
