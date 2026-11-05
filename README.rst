my_api_demo
===========

基于 Poetry + FastAPI + APIRouter 的模块化后端演示项目。

功能
----

- ``GET /`` : 服务健康检查
- ``GET /api/weather/current`` : 根据当前 IP 地理位置返回实时天气（Open-Meteo）
- ``GET /api/upmedia/headlines`` : 抓取 upmedia.mg 快讯标题列表

快速开始
--------

.. code-block:: bash

   poetry install
   poetry run uvicorn python_api_project.main:app --reload --host 0.0.0.0 --port 8000

然后访问 http://127.0.0.1:8000/docs 查看交互式文档。

代理说明
--------

如需通过代理访问外部网站，可设置环境变量 ``HTTP_PROXY`` / ``HTTPS_PROXY``，
或在 ``routers/upmedia_api.py`` 中取消代理相关注释。
