# Test Tasks
The Test Tasks project is a module of test, a backend service developed by dadadamizhou.

## API Documentation

### Swagger UI

The OpenAPIv3 documentation can be parsed to SwaggerUI embedded in the application:

http://localhost:8000/docs

### ReDoc

The OpenAPIv3 documentation can be parsed to ReDoc embedded in the application:

http://localhost:8000/redoc

## Dependency
* python 3.10
* FastAPI
* ORM: `SQLAlchemy`
* migrations: `Alembic`

## Local development

### test
```
/app/test/test_api.py
```

### DB
```
docker-compose up -d
```

### Python
```bash
pip install poety
poetry install
python3 app/main.py
```
### Uvicorn
```bash
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000 --log-level info
```

### Migrations

```bash
alembic revision --autogenerate -m "xxxx"
alembic upgrade head
```



## Environment variables

### Database configuration
`Required.`

- DB_NAME: database name
- DB_USER: database username
- DB_PASSWORD: database user's password
- DB_HOST: database host
- DB_PORT: database port


### Common configuration
- HOST: Required, api host
- BACKEND_CORS_ORIGINS: ["http://127.0.0.1:8000"]
- OPENAPI_URL: Optional, default: `/openapi.json`, when set to blank, doc feature will be disabled.
