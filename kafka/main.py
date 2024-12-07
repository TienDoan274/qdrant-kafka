from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
import routes

# Tạo ứng dụng FastAPI
app = FastAPI(title="Metrics Collector")

# Thêm router từ module routes
app.include_router(routes.router)

# Thêm middleware Prometheus và route /metrics
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
