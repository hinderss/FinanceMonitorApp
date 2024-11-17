# FinanceMonitorApp

A system for tracking and monitoring financial transactions. This application provides a user-friendly interface for transaction history, and payment cards.

## Features

- User registration and authentication
- Transaction history
- Payment management
- Secure data storage in a database

## Prerequisites

Make sure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the project running with Docker:

### 1. Clone the Repository

```bash
git clone https://github.com/hinderss/FinanceMonitorApp.git
cd FinanceMonitorApp
```

### 2. Configure Environment Variables

Create a `.env` file in the project root and configure the following variables:

```env
POSTGRES_DB=finance
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
FERNET_KEY={your-fernet-key}

SECRET_KEY={your-secret-key}
DEBUG=False
```
You can generate secret keys by yourself or use [Fernet Key Generator](https://fernetkeygen.com/)

### 3. Build and Start Docker Containers

Use Docker Compose to build and start the application:

```bash
docker-compose up --build
```

This command will:

1. Build the Docker images for the application and database.
2. Start the containers.

### 4. Access the Application

Once the containers are running, you can access the application at:

- http://localhost/

### 5. Stop the Application

To stop the containers, use:

```bash
docker-compose down
```

---

Feel free to contribute and raise issues for any improvements or bugs!