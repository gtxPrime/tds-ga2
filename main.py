from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import uuid, time

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-p1kf4h.example.com"

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        request_id = str(uuid.uuid4())
        response = await call_next(request)
        process_time = time.time() - start
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(round(process_time, 6))
        return response

app.add_middleware(CustomMiddleware)

@app.options("/stats")
async def stats_preflight(request: Request):
    origin = request.headers.get("origin", "")
    headers = {
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "X-Request-ID": str(uuid.uuid4()),
        "X-Process-Time": "0.000001",
    }
    if origin == ALLOWED_ORIGIN:
        headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    return Response(status_code=200, headers=headers)

@app.get("/stats")
async def stats(request: Request, values: str = ""):
    origin = request.headers.get("origin", "")
    nums = [int(x) for x in values.split(",") if x.strip()]
    count = len(nums)
    total = sum(nums)
    mn = min(nums)
    mx = max(nums)
    mean = total / count if count else 0.0

    result = {
        "email": "24f1000625@ds.study.iitm.ac.in",
        "count": count,
        "sum": total,
        "min": mn,
        "max": mx,
        "mean": round(mean, 6),
    }

    from fastapi.responses import JSONResponse
    response = JSONResponse(content=result)
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    return response
