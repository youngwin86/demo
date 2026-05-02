"""
热搜抓取脚本 - 抓取百度、微博、抖音热搜数据
"""
import sys
import io

# 在 Windows 上强制 UTF-8 输出，避免乱码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

def fetch_weibo_hot():
    """抓取微博热搜"""
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://weibo.com/"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        hot_list = []
        for item in data.get("data", {}).get("realtime", [])[:50]:
            hot_list.append({
                "rank": item.get("rank", 0),
                "title": item.get("word", ""),
                "hot": item.get("raw_hot", 0),
                "category": item.get("category", ""),
                "label": item.get("label", "")
            })
        return {"platform": "weibo", "data": hot_list}
    except Exception as e:
        return {"platform": "weibo", "error": str(e)}

def fetch_baidu_hot():
    """抓取百度热搜 - 使用百度官方API"""
    
    # 使用百度PC端API
    url = "https://top.baidu.com/board?tab=realtime"
    api_url = "https://top.baidu.com/api/board?platform=pc&tab=realtime"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://top.baidu.com/board?tab=realtime"
    }
    
    try:
        # 先访问主页获取cookie
        session = requests.Session()
        session.get(url, headers=headers, timeout=10)
        
        # 再请求API
        resp = session.get(api_url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        hot_list = []
        cards = data.get("data", {}).get("cards", [])
        if cards and len(cards) > 0:
            content = cards[0].get("content", [])
            for i, item in enumerate(content[:50]):
                hot_list.append({
                    "rank": i + 1,
                    "title": item.get("word", ""),
                    "hot": item.get("hotScore", 0),
                    "desc": item.get("desc", "")
                })
        
        if hot_list:
            return {"platform": "baidu", "data": hot_list}
        else:
            return {"platform": "baidu", "data": [], "error": "未获取到数据"}
            
    except Exception as e:
        return {"platform": "baidu", "data": [], "error": str(e)}

def fetch_douyin_hot():
    """抓取抖音热搜"""
    url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.douyin.com/"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        hot_list = []
        for i, item in enumerate(data.get("word_list", [])[:50]):
            hot_list.append({
                "rank": i + 1,
                "title": item.get("word", ""),
                "hot": item.get("hot_value", 0)
            })
        return {"platform": "douyin", "data": hot_list}
    except Exception as e:
        return {"platform": "douyin", "error": str(e)}

def main():
    platform = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    result = {}
    if platform in ["all", "weibo"]:
        result["weibo"] = fetch_weibo_hot()
    if platform in ["all", "baidu"]:
        result["baidu"] = fetch_baidu_hot()
    if platform in ["all", "douyin"]:
        result["douyin"] = fetch_douyin_hot()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()