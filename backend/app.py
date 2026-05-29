#app.py 

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.upload import router as upload_router
from routes.processing import router as processing_router
from routes.results import router as results_router

from core.logging import setup_logging
import config

logger = setup_logging()
logger.info("Logging has been successfully set up.")

app = FastAPI()

# Enable CORS
# middleware - code that runs before and after every request
# CORS - Cross Origin Resource Sharing - Is a mechanism that allows to specify which other origins(domains, ports, protocols) are permitted to access their resources.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(processing_router)
app.include_router(results_router)

@app.get("/")
def root():
    return{"message":"Smoke Detection Backend Running"}

@app.get("/api/health")
def health():
    return {"status": "ok"}


from fastapi.staticfiles import StaticFiles

app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs"
)