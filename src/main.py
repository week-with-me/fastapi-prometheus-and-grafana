import time
import asyncio
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    start_http_server
)

app = FastAPI()

graphs = {}
graphs["counter"] = Counter(
    "app_http_request_count",
    "The Total number of HTTP Application request"
)
graphs["histogram"] = Histogram(
    "app_http_response_time",
    "The time of HTTP Application response",
    buckets=(1, 2, 5, 6, 10, float("inf")) # Positive Infinity
)

@app.get("/ping")
async def health_check():
    start_time = time.time()
    graphs["counter"].inc()
    
    await asyncio.sleep(3)
    
    end_time = time.time()
    graphs["histogram"].observe(end_time - start_time)
    
    print(graphs)
        
    return JSONResponse(status_code=status.HTTP_200_OK, content="pong")


@app.on_event("startup")
def startup_event():
    start_http_server(port=8001)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
