import uvicorn
from fastapi import FastAPI
from restaurant_app.api.restaurant import router
from restaurant_app.core.config import settings

app = FastAPI(title=settings.app_title)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, env_file="./.env") 
