# Microservices using FastAPI

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## About

This project demonstrates the implementation of a microservices architecture using FastAPI, a modern, fast web framework for building APIs with Python. The project is structured into separate microservices, each responsible for a specific functionality. It leverages the power of FastAPI to create efficient and scalable microservices.

## Technologies Used

- Python
- FastAPI
- Docker
- Nginx (for reverse proxy and load balancing - optional)

## Usage

To use and test the microservices, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/microservices-fastapi.git`
2. Enter the project directory: `cd microservices-fastapi`
3. Build and run the Docker containers: `docker-compose up -d`
4. The microservices will be accessible on the following ports:
   - Auth Service: `http://localhost:8000`
   - Blog Service: `http://localhost:8001`
   - Chat Service: `http://localhost:8002`
   - Converter Service: `http://localhost:8003`

## Contribution

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m "Add your message here"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request.

## Flow Diagram
├── Auth
│   ├── Dockerfile
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── db
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── authentication.py
│   │   │   └── profile.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── config.py
│   │       ├── hashing.py
│   │       └── token.py
│   ├── main.py
│   └── requirements.txt
│
├── Blog
│   ├── Dockerfile
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── db
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── blog.py
│   │   │   └── comments.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── authentication.py
│   │       ├── authorization.py
│   │       └── pagination.py
│   ├── main.py
│   └── requirements.txt
│
├── Chat
│   ├── Dockerfile
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── db
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── users.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── authentication.py
│   │       ├── authorization.py
│   │       └── websocket.py
│   ├── main.py
│   └── requirements.txt
│
├── Converter
│   ├── Dockerfile
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── convert.py
│   │   │   └── history.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── authentication.py
│   │       └── validation.py
│   ├── main.py
│   └── requirements.txt
│
├── README.md
├── .gitignore
├── nginx
│   └── nginx.conf
└── docker-compose.yml



## Working

1. **Auth Microservice**: Handles user authentication and profile management. It uses FastAPI's powerful routing capabilities for defining API endpoints.

2. **Blog Microservice**: Provides functionalities related to blog posts and comments. FastAPI's validation features are utilized to ensure data integrity.

3. **Chat Microservice**: Manages real-time chat functionality with WebSocket support. FastAPI WebSocket features are employed for bidirectional communication.

4. **Converter Microservice**: Converts data between different formats (e.g., JSON to XML). FastAPI's request and response models streamline data conversion.

Each microservice is containerized using Docker for easy deployment and scalability. Nginx can be optionally used as a reverse proxy and load balancer to distribute incoming requests among the microservices.

Feel free to explore each microservice's code and extend their functionalities according to your requirements.

Happy coding! 🚀

---

Please note that the actual content of the "Flow Diagram" section should include a diagram that visually represents the interaction between the microservices and any other relevant components (e.g., databases). Similarly, the usage instructions and technology details should be tailored to the specific implementation of your microservices project.