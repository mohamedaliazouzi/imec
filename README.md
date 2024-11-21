# Internship Candidate Exercise CSA-imec : Django

This project is a Django-based RESTful API for user registration and attribute management. Users can register with custom attributes, and their profiles, attributes, and relationships are managed seamlessly.

## Features
User registration with customizable attributes.
Group and profile management.
Comprehensive token-based authentication using JWT.
Full CRUD functionality for attributes, groups, and profiles.
Detailed error handling and validation.
Secure password handling and user data storage.

##Technologies Used
Backend Framework: Django, Django REST Framework
Authentication: JSON Web Tokens (JWT)
Database: SQLite (default), configurable for PostgreSQL/MySQL
Programming Language: Python 3.x
Deployment: Dockerized setup for easy deployment
Testing: Django Test Framework and DRF APITestCase

## Installation and Setup

### Pre-requisites
Python 3.9 or higher
Docker (for containerized deployment)
###Choice of Docker 

Why Docker?

I chose Docker for this project due to its versatility and ability to streamline the deployment of containerized applications. Here are the key reasons behind this decision:

Simplified Containerization: Docker allows running the application in isolated containers, ensuring consistency across development, testing, and production environments.

Ease of Integration: Docker seamlessly integrates with Celery and Redis, which are crucial for managing asynchronous tasks in this project.

Scalability: By containerizing the application and its services, it's easy to scale individual components like the web server, worker processes, or Redis as needed.

Portability: Docker containers ensure the project runs the same way regardless of the underlying infrastructure, whether on a local machine or a cloud server.

### Steps
1/Open the folder :`cd imec`

2/Activate Virtual enviroment :

          python3 -m venv myenv`
          Mac :source myenv/bin/activate
          Windows: myenv\Scripts\activate

3/Run docker-compose up --build
4/Access API via `http://localhost:8002/`

## API Endpoints
### Testing the Endpoints can be done using Postman or Swagger via `http://localhost:8002/swagger/` 


### Authentication
| **Method** | **Endpoint**            | **Description**                  |
|------------|--------------------------|-----------------------------------|
| POST       | `/api/token/`           | Obtain JWT tokens :**No Bearer needed**               |
| POST       | `/api/token/refresh/`   | Refresh access token  **No Bearer needed**           |

### User Management
| **Method** | **Endpoint**            | **Description**                  |
|------------|--------------------------|-----------------------------------|
| POST       | `/api/register/`        | Register a new user**No Bearer needed**              |
| GET        | `/api/users/{id}/paired`| Retrieve  show all users a user is paired with by providing its ID   |

### Attribute Management
| **Method** | **Endpoint**            | **Description**                  |
|------------|--------------------------|-----------------------------------|
| GET        | `/api/attributes/`      | Retrieve all attributes          |

### Group Management
| **Method** | **Endpoint**            | **Description**                  |
|------------|--------------------------|-----------------------------------|
| GET        | `/api/groups/`      | Retrieve all groups          |

## Contact 
Mohamed Ali Azouzi
Email :mohamedali.azaouzi@esprit.tn 

Portfolio:https://www.upwork.com/freelancers/~0196f8cbf625f2923f

Github:https://github.com/mohamedaliazouzi

Linkedin:https://www.linkedin.com/in/mohamed-ali-azouzi-software-engineering/

