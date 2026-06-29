from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import uuid
import time

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-p1kf4h.example.com"
EMAIL = "24f1000625@ds.study.iitm.ac.in"  # <-- REPLACE WITH YOUR EMAIL

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())

    # Handle CORS preflight
    origin = request.headers.get("origin", "")
    if request.method == "OPTIONS":
        if origin == ALLOWED_ORIGIN:
            return Response(
                status_code=204,
                headers={
                    "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "X-Request-ID": request_id,
                    "X-Process-Time": "0.000001",
                },
            )
        else:
            return Response(status_code=403, headers={"X-Request-ID": request_id, "X-Process-Time": "0.000001"})

    response = await call_next(request)
    elapsed = time.perf_counter() - start

    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response


@app.get("/stats")
def stats(values: str, request: Request):
    nums = [int(v) for v in values.split(",")]
    n = len(nums)
    s = sum(nums)
    return {
        "email": EMAIL,
        "count": n,
        "sum": s,
        "min": min(nums),
        "max": max(nums),
        "mean": round(s / n, 6),
    }
