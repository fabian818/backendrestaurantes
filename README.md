# Backend Restaurantes

Backend part of the restaurant system project.

## Getting Started

```
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web sh fixtures/create_metadata.sh
```

### Prerequisites

```
docker
docker-compose
```

### Installing

For docker use: [Docker Install Script](https://github.com/docker/docker-install)

For docker-compose use: [Docker Compose Install](https://docs.docker.com/compose/install/)


## Running the tests

```
docker-compose exec web python manage.py test api.tests
```

## Built With

* [Docker](https://www.docker.com/) - The container platform
* [Docker Compose](https://docs.docker.com/compose/) - Container execution library
* [Django](https://www.djangoproject.com/) - The web framework
* [Django Rest Framework](https://www.django-rest-framework.org/) - The rest api web framework
* [PostgreSQL](https://www.postgresql.org/) - The principal database

## Contributing

You need to be on the hotdevelopers backend team.

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Hotdevelopers** - *Initial work* - [fabian818](https://github.com/fabian818)

See also the list of [contributors](https://github.com/fabian818/backendrestaurantes/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
