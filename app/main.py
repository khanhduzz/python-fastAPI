from fastapi import FastAPI
from routers import user_route
from routers import auth, task_route, company_route

app = FastAPI()

app.include_router(task_route.router)
app.include_router(user_route.router)
app.include_router(auth.router)
app.include_router(company_route.router)


@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"
