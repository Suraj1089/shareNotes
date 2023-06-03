# Microservices in FastAPI, with docker

This project consists of three microservices developed using FastAPI: auth, recommender, and scrapper. The microservices provide functionality for user authentication, project recommendation based on skills and experience, and scraping GitHub data, respectively.

Installation
Clone the project repository from GitHub.

```
git clone https://github.com/Suraj1089/shareNotes.git
```

Install the required dependencies for each microservice by navigating to their respective directories (auth, recommender, scrapper) and running the following command:
```
pip install -r requirements.txt
```
Setup
Auth Microservice
Configure the authentication settings in the auth/config.py file, such as the database connection details and secret key.

Run the migration to set up the database schema:

shell
Copy code
```
alembic upgrade head
```
Recommender Microservice
Configure the recommender settings in the recommender/config.py file, such as the database connection details and recommendation algorithms.

If necessary, train the recommendation models using the provided data or your own dataset.

Scrapper Microservice
Configure the scrapper settings in the scrapper/config.py file, such as the GitHub API credentials and scraping options.
Usage
Start the microservices individually by running the following commands in separate terminal windows:


```
uvicorn auth.main:app --reload
uvicorn recommender.main:app --reload
uvicorn scrapper.main:app --reload
```
Make sure to run them in the respective directories (auth, recommender, scrapper).

Access the microservices using the provided endpoints and interact with them using HTTP requests.

About
The microservices in this project are designed to work together to provide a comprehensive system for user authentication, project recommendation, and GitHub data scraping. Each microservice can be deployed independently and scaled as needed.

The auth microservice handles user authentication and authorization. It provides endpoints for user registration, login, and token management.

The recommender microservice leverages recommendation algorithms to provide project recommendations based on user skills and experience. It utilizes machine learning models trained on relevant data.

The scrapper microservice scrapes GitHub data to gather information about repositories, contributors, and other relevant details. It provides endpoints to retrieve data related to GitHub projects.

How It Works
The auth microservice handles user registration and authentication. Users can register with their credentials and receive authentication tokens upon successful login. These tokens can be used to access the protected endpoints of other microservices.

Users can make requests to the recommender microservice to get project recommendations based on their skills and experience. The recommender microservice processes the user's data, applies recommendation algorithms, and returns a list of recommended projects.

The scrapper microservice is responsible for scraping GitHub data. Users can request information about specific repositories, contributors, or other GitHub-related details. The scrapper microservice retrieves the required data from the GitHub API and returns it to the user.

By combining these microservices, users can authenticate, get project recommendations, and retrieve GitHub data seamlessly.

Contributing
If you would like to contribute to this project, please follow these steps:

Fork the repository on GitHub.

Create a new branch for your feature or bug fix.

Commit your changes to the new branch.

Push the branch to your forked repository.

Submit a pull request with a description of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

Contact
If you have any questions or inquiries about this project, please contact project@example.com.

FastAPI
GitHub