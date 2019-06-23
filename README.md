<h1 align="center">RESTful API for our Human Resources Database 🕘 - 🕔</h1>
<p>
  <img src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/wanderindev/hr-rest-api/blob/master/README.md">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://github.com/wanderindev/hr-rest-api/graphs/commit-activity">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://htmlpreview.github.io/?https://github.com/wanderindev/hr-rest-api/blob/master/coverage/index.html">
    <img alt="Coverage" src="https://img.shields.io/badge/coverage-99%25-yellowgreen.svg" target="_blank" />
  </a>  
  <a href="https://github.com/wanderindev/hr-rest-api/blob/master/LICENSE.md">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://twitter.com/JavierFeliuA">
    <img alt="Twitter: JavierFeliuA" src="https://img.shields.io/twitter/follow/JavierFeliuA.svg?style=social" target="_blank" />
  </a>
</p>

>RESTful API for performing CRUD operations in our Human Resources database.  The API was coded in Python
using Flask, Flask-RESTful, SQLAlchemy, and Flask-JWT.  For testing, I used UnitTest.

## How to use in development
Clone the repository:
```sh
git clone https://github.com/wanderindev/hr-rest-api.git
cd hr-rest-api
``` 
Start the application with docker-compose:
```sh
docker-compose up --build
```
This will create a database container, a RESTful API container, a backend network, and a volume
mapping the ./rest directory in the repository with the working directory in the container.

## Running tests
From PyCharm, right-click in the `tests/system` or `tests/unit` directory and select 
"Run tests with Coverage" to run either system or unit tests.

## Testing with Postman

Clone the [postman-hr-rest-api](https://github.com/wanderindev/postman-hr-rest-api)
repository:
```sh
git clone https://github.com/wanderindev/postman-hr-rest-api.git
``` 
Open Postman and import `hr-rest-api.json` and `hr-rest-api-environment.json`.

Click on Runner.

In the window that pops open, select the `hr-rest-api` collection and the `hr-rest-api`
environment.

Click on Run.

## Deployment
Modify `rest/Dockerfile_prod`, adding the correct values for the environment variables.

Build the container image and push to Docker Hub:
```sh
cd rest
docker build -t wanderindev/hr-rest -f Dockerfile_prod .
docker push wanderindev/hr-rest
``` 
 
 Go to the [do-managed-kubernetes](https://github.com/wanderindev/do-managed-kubernetes) 
 repository and re-deploy the pod.
 ```sh
kubectl delete deployment hr-rest
kubectl apply -f ./sites/hr-rest.yml
``` 

 ## Author

👤 **Javier Feliu**

* Twitter: [@JavierFeliuA](https://twitter.com/JavierFeliuA)
* Github: [@wanderindev](https://github.com/wanderindev)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [Javier Feliu](https://github.com/wanderindev).<br />

This project is [MIT](https://github.com/wanderindev/hr-rest-api/blob/master/LICENSE.md) licensed.

***
_I based this README on a template generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
 