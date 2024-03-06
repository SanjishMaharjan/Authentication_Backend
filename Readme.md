# FastAPI Learning Project

Welcome to my FastAPI learning project! This hands-on exploration focuses on using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+.

## Project Overview

This project showcases basic functionality to create a simple blogging system. The implemented features include retrieving blogs, fetching unpublished blogs, getting blog details, fetching comments, and creating new blogs.

## Getting Started

To run this project locally, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/SanjishMaharjan/FastBlogAPI
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI application:

    ```bash
    python -m uvicorn main:app --reload
    ```

4. Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to interact with the API using the provided endpoints.

## Project Structure

The project structure is organized as follows:

- `main.py`: Contains the FastAPI application and the main entry point.
- `schemas.py`: Defines the data models (schemas) used in the project.
- `models.py`: Contains SQLAlchemy models for interacting with the database.
- `database.py`: Manages the database connection and session creation.
- `requirements.txt`: Lists the project dependencies.

## Recent Changes

### Endpoint Additions

1. **Create Blog:**

    - Endpoint: `POST /blog`
    - Description: Adds a new blog with the specified title and body.
    - Example Usage:

        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"title": "New Blog", "body": "Blog content..."}' http://127.0.0.1:8000/blog
        ```

2. **Retrieve All Blogs:**

    - Endpoint: `GET /blog`
    - Description: Retrieves a list of all blogs.
    - Example Usage:

        ```bash
        curl http://127.0.0.1:8000/blog
        ```

3. **Retrieve Single Blog:**

    - Endpoint: `GET /blog/{id}`
    - Description: Retrieves details of a single blog by ID.
    - Example Usage:

        ```bash
        curl http://127.0.0.1:8000/blog/1
        ```

### Database Interaction

- Database tables are created automatically using SQLAlchemy when the application starts.

### Dependency Management

- Implemented a dependency (`get_db`) to manage database sessions.


