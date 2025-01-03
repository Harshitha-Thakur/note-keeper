# Note Keeper

This is a simple note-keeping application with a Flask backend and a React frontend.

## Setup

1. Clone the repository.
2. Build the Docker images without using the cache:
    ```sh
    docker-compose build --no-cache
    ```
3. Start the application using Docker Compose:
    ```sh
    docker-compose up
    ```

## Usage

- The backend will be available at `http://localhost:5000`.
- The frontend will be available at `http://localhost:3000`.