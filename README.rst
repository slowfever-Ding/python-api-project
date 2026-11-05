python_api_project
==================

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

如需通过代理访问外部网站，可设置环境变量：

.. code-block:: bash

   # Windows PowerShell
   $env:HTTP_PROXY="http://127.0.0.1:7983"
   $env:HTTPS_PROXY="http://127.0.0.1:7983"

   # Linux / macOS
   export HTTP_PROXY=http://127.0.0.1:7983
   export HTTPS_PROXY=http://127.0.0.1:7983

不设置环境变量时，将直接访问目标网站（云服务器部署推荐不设置代理）。

部署说明
--------

已支持部署到 Railway / Render 等平台。

启动命令示例：

.. code-block:: bash

   poetry run uvicorn python_api_project.main:app --host 0.0.0.0 --port $PORT