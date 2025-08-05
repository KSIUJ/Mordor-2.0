# Authors
opwip
<<<<<<< HEAD
Jakub Karczyński
=======

Jakub Karczyński

>>>>>>> 63f789474e5e28c62412d2e914a2fc3b491b92ec
# Mordor-2.0(Change .md files later, most of the content is for IntroTask)
This is a template for FastAPI applications from IntroductionTask, tweaked for it to work with sqlite db.

## Important notes
--**test/EndPointTest.py**: Use this to test endpoints(Relates to Mordor2.0)
--**db.delete() in main.py** FOR TESTING ONLY, REMOVE OR COMMENT WHNE NEEDED(Mordor2.0 testing)
Some important notes related to specific functionalities are in few directories:
- **app/README.md**: This file contains examples and patterns for implementing routers, repositories, and models. You can follow them but it is not mandatory.
- **db/000-info.sql**: This file contains informations about working with postgres database and how to initalize it in some way.
- **scripts/connect-db.sh**: This script is used to connect to the database. It can be useful for debugging or manual database operations. It uses psql.

## Features
This template has these set up for you:
- static files serving
- CORS middleware
- Database in container
- Database connection
- Dockerfile
- Docker Compose
- jinja2 templates
- some health check example route


## Development
To run the application you can use docker-compose:
```bash
docker compose up --build -d
```
It will run the database and the FastAPI application. You can access the application at `http://localhost:8080`.
When you make any changes the application will automatically reload.

> IMPORTANT: If you change the requirements.txt file, you need to rebuild the Docker image:
> ```bash
> docker compose up --build -d
> ```
> or if you want to be more specific:
> ```bash
> docker compose up --build -d fastapi-template-app
> ```

### No docker :c
If you don't want to use Docker, you can run the application locally. 
You can search in FastAPI documentation how to do it, or look at the
'app/Dockerfile' it is a some kind of recipe for running the application locally.
