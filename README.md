# pwp2020

## Running the API
Use Docker to run the API
`docker-compose up`
API is then accessible at localhost:5000


Docker also set ups a Postgres database container, and connects the API to the database automaticly.

## TESTS

`docker-compose -f docker-compose.test.yml build && docker-compose -f docker-compose.test.yml up`