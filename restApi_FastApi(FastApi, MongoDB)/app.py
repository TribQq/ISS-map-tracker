# convenient automatic documentation
# uvicorn app:app --reload # automatic update without restarting the server

from fastapi import FastAPI
from routes.users import user
from docs import tags_metadata

app = FastAPI(
   title='REST API, FastApi+MongoDB',
   description='This is simple REST API, realize CRUD operations with FastApi and MongoDB',
   version='0.0.1.1.1',
   openapi_tags=tags_metadata,
)

app.include_router(user)