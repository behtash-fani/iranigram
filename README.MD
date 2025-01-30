# Project Overview

This project is a web application designed to manage various aspects of an online service. It includes multiple sections and apps to handle different functionalities such as user accounts, orders, notifications, and more.

## Technologies Used

- **Python**: The core programming language used for backend development.
- **Django**: The web framework used to build the backend of the application.
- **Docker**: Used for containerizing the application to ensure consistency across different environments.
- **Nginx**: Used as a reverse proxy server.
- **jQuery**: Used for DOM manipulation and AJAX requests.
- **CKEditor**: A rich text editor used in the application.
- **Select2**: A jQuery-based replacement for select boxes.

## Project Structure

- **app/**: Contains the Dockerfile and requirements for the main application.
- **nginx/**: Contains the Dockerfile for the Nginx server.
- **volumes/**: Contains the source code and static files for the application.
  - **app/**: Contains the Django apps and configurations.
    - **accounts/**: Manages user accounts and authentication.
    - **api/**: Handles API endpoints.
    - **comments/**: Manages user comments.
    - **common/**: Contains common utilities and configurations.
    - **config/**: Contains Django settings and configurations.
    - **notification/**: Manages notifications.
    - **orders/**: Manages orders and transactions.
    - **pages/**: Manages static pages.
    - **posts/**: Manages blog posts.
    - **seo/**: Manages SEO configurations.
    - **service/**: Contains service-related functionalities.
    - **setting/**: Manages application settings.
    - **support/**: Manages user support.
    - **templates/**: Contains HTML templates.
    - **transactions/**: Manages financial transactions.
  - **static/**: Contains static files such as CSS, JavaScript, and images.

## How to Run the Project

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

3. **Apply database migrations**:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

4. **Create a superuser**:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

5. **Collect static files**:
    ```sh
    docker-compose exec web python manage.py collectstatic
    ```

6. **Access the application**:
    Open your browser and navigate to `http://localhost`.

## Purpose of the Panel Template

The panel template is designed to provide an intuitive and user-friendly interface for managing various aspects of the application. It includes sections for managing user accounts, orders, notifications, and more, making it easy for administrators to oversee and control the application's functionalities.

## Author

- **Behtash Fani**