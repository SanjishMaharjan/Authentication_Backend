from fastapi import FastAPI
from users import models
from db.config import engine
import uvicorn


from users.routers import fileuploader, user, authentication

app = FastAPI()

PORT = 8000
models.Base.metadata.create_all(engine)

app.include_router(fileuploader.router)
# app.include_router(user.router)
# app.include_router(authentication.router)

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=PORT, reload=True)
    server = uvicorn.Server(config)
    server.run()
