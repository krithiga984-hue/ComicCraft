from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI()

# Static files mount panrom (Images display aagurathuku ithu romba mukkiyam)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routes-ah include panrom
app.include_router(router)