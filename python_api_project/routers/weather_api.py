from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(prefix="/api/weather", tags=["天气模块"])

# 定义 WMO 官方天气代码映射字典
WMO_WEATHER_CODES = {
    0: "晴朗",
    1: "大部晴朗",
    2: "多云",
    3: "阴天",
    45: "有雾",
    48: "雾凇/沉积雾",
    51: "轻度毛毛雨",
    53: "中度毛毛雨",
    55: "密集毛毛雨",
    56: "轻度冻毛毛雨",
    57: "密集冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "轻度冻雨",
    67: "重度冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "中阵雨",
    82: "剧烈阵雨",
    85: "小阵雪",
    86: "大阵雪",
    95: "雷暴",
    96: "雷暴伴有轻度冰雹",
    99: "雷暴伴有重度冰雹",
}


@router.get("/current")
def get_current_weather():
    try:
        # 通过免费的 IP 定位服务获取当前服务器所在位置（经纬度与城市名称）
        # 注：如果在本地运行，获取的是你当前网络出口公网 IP 对应的位置
        ip_res = requests.get("http://ip-api.com/json/?lang=zh-CN", timeout=5)
        ip_res.raise_for_status()
        ip_data = ip_res.json()

        if ip_data.get("status") != "success":
            raise HTTPException(status_code=500, detail="无法自动解析当前地理位置")

        lat = ip_data.get("lat")
        lon = ip_data.get("lon")
        city = ip_data.get("city", "未知城市")
        region = ip_data.get("regionName", "")
        country = ip_data.get("country", "未知国家")

        # 使用 Open-Meteo 免费天气 API（完全免费，不需要申请复杂的 API Key）
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current_weather=true"
        )
        weather_res = requests.get(weather_url, timeout=5)
        weather_res.raise_for_status()
        weather_data = weather_res.json()

        current = weather_data.get("current_weather") or {}
        weather_code = current.get("weathercode")
        weather_desc = WMO_WEATHER_CODES.get(weather_code, "未知天气")
        temp = current.get("temperature")
        windspeed = current.get("windspeed")

        return {
            "code": 200,
            "msg": "success",
            "data": {
                "location": {
                    "country": country,
                    "region": region,
                    "city": city,
                    "latitude": lat,
                    "longitude": lon,
                },
                "weather": {
                    "temperature": f"{temp} °C" if temp is not None else "未知",
                    "windspeed": f"{windspeed} km/h" if windspeed is not None else "未知",
                    "winddirection": current.get("winddirection"),
                    "weather_code": weather_code,
                    "weather_text": weather_desc,
                    "update_time": current.get("time"),
                },
            },
        }

    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=502, detail=f"网络请求异常: {str(req_err)}")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
