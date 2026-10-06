from fastapi import FastAPI
import uvicorn

from api.__init__ import main_router
from core.handlers import register_exception_handlers
from core.container import AppContainer


app: FastAPI = FastAPI()

app.state.container = AppContainer()

register_exception_handlers(app)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app")