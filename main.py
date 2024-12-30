from fastapi import FastAPI
import uvicorn
import yaml
from logging import getLogger
logger = getLogger(__name__)

app = FastAPI()

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome!"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    with open('config.yaml', 'r') as yml:
        config = yaml.safe_load(yml)
    
    PORT = config['PORT']
    
    if(PORT):
        uvicorn.run(app, port=PORT)
    else:
        logger.warning("PORT not found in environment variables.")
        logger.warning("Starting server on default port 8000")
        uvicorn.run(app, port=8000)