# Note Keeper

This is a simple note-keeping application with a Flask backend and a React frontend.

## Setup

1. Clone the repository.
2. Navigate to the `backend` directory and create a virtual environment.
3. Install the backend dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Navigate to the `frontend` directory and install the frontend dependencies:
    ```sh
    npm install
    ```
5. Start the application using Docker Compose:
    ```sh
    docker-compose up
    ```

## Usage

- The backend will be available at `http://localhost:5000`.
- The frontend will be available at `http://localhost:3000`.

## Running Tests

To run the backend tests, navigate to the [backend](http://_vscodecontentref_/1) directory and run:
```sh
pytest