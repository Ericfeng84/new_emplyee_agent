# Scripts

This directory contains utility scripts for running and managing the Nexus Agent system.

## Available Scripts

### start_all.sh
Starts both the backend API server and the frontend development server simultaneously.
This is the recommended way to run the complete application during development.

Usage:
```bash
./scripts/start_all.sh
```

### start_dev.sh
Development startup script for running the application in development mode.
This script sets up the environment and starts the necessary services.

Usage:
```bash
./scripts/start_dev.sh
```

### run_server.py
Python script to start the backend server directly.
Useful for debugging or running the backend independently.

Usage:
```bash
python scripts/run_server.py
```

## Notes

- Make sure the scripts have executable permissions before running:
  ```bash
  chmod +x scripts/*.sh
  ```
- Ensure all environment variables are properly configured in `.env` before running these scripts.
- Log files will be created in the `logs/` directory when the servers start.
