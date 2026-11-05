from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(prefix="/api/upmedia", tags=["上报新闻模块"])


@router.get("/headlines")
def get_upmedia_headlines():
    url = "https://www.upmedia.mg/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    # 本地代理（已确认 7983 端口可用）
    proxies = {
        "http": "http://127.0.0.1:7983",
        "https": "http://127.0.0.1:7983",
    }

    try:
        response = requests.get(
            url, headers=headers, proxies=proxies, timeout=20
        )
        response.encoding = "utf-8"

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"抓取失败，状态码: {response.status_code}",
            )

        soup = BeautifulSoup(response.text, "html.parser")
        news_flash = soup.find("div", class_="news-flash")

        if not news_flash:
            return {
                "code": 404,
                "msg": "未找到快讯容器组件",
                "data": [],
            }

        items = news_flash.find_all("li")
        news_list = []

        for item in items:
            a_tag = item.find("a", class_="news-flash-text")
            date_tag = item.find("div", class_="news-flash-date")

            if a_tag and date_tag:
                title = a_tag.get_text(strip=True)
                href = a_tag.get("href", "")
                link = (
                    href
                    if href.startswith("http")
                    else "https://www.upmedia.mg" + href
                )
                date = date_tag.get_text(strip=True)
                news_list.append({"title": title, "link": link, "date": date})

        return {"code": 200, "msg": "success", "data": news_list}

    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=502, detail=f"网络请求异常: {str(req_err)}")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
