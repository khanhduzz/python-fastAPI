from fastapi import FastAPI
from routers import staffRoute, taskRoute, userRoute
from routers import auth


app = FastAPI()

app.include_router(staffRoute.router)
app.include_router(taskRoute.router)
app.include_router(userRoute.router)
app.include_router(auth.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"
