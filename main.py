from fastapi import FastAPI

from billing.router import router

app = FastAPI()
app.include_router(router)
