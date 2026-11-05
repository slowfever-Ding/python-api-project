from fastapi import FastAPI
from python_api_project.routers import upmedia_api, weather_api

app = FastAPI(
    title="Modular FastAPI Project",
    version="1.0.0",
    description="基于 Poetry 与 APIRouter 构建的工程化后端服务",
)

# 挂载各个业务路由模块
app.include_router(weather_api.router)
app.include_router(upmedia_api.router)


@app.get("/")
def root():
  return {
      "msg": "API 服务运行正常",
      "docs_url": "/docs",
      "redoc_url": "/redoc",
  }