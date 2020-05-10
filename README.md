# pwp2020

## Running the API
Use Docker to run the API:
`docker-compose up`



API is then accessible at localhost:5000/api.
Docker also set ups a Postgres database container, and connects the API to the database automaticly.

## Dependencies

To run the project there are two main dependencies, Docker and the Docker compose. To install Docker compose please refer to the official [documentation](https://docs.docker.com/compose/install/) and documentation and guides to install Docker can be found [here](https://www.docker.com/get-started)

## TESTS

The tests uses similar environment than the api itself, however separate databases and api are created to avoid conflict between test containers and deployment containers. Sometimes `docker system prune --volumes` command might be needed alongside `docker-compose build --no-cache` to clean build caches and layers that docker uses. 

`docker-compose -f docker-compose.test.yml build && docker-compose -f docker-compose.test.yml up`
