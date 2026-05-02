---
name: hotspot
description: 抓取百度、微博、抖音热搜数据。当用户需要获取热搜榜单、热点话题、实时热点时使用此技能。支持抓取百度热搜、微博热搜、抖音热搜，可单独获取某一平台或同时获取全部平台数据。
triggers:
  - 热搜
  - 热点
  - 今日热搜
  - 微博热搜
  - 百度热搜
  - 抖音热搜
---

# Hotspot - 热搜抓取

## 功能概述

本技能用于抓取国内主流平台的热搜榜单数据：
- **微博热搜** - 实时热点话题
- **百度热搜** - 百度搜索热点
- **抖音热搜** - 抖音热点榜单

## 触发词

当用户发送以下关键词时自动触发：
- `热搜` / `热点` / `今日热搜`
- `微博热搜` / `百度热搜` / `抖音热搜`

## 使用方法

### 命令行调用

```bash
# 抓取所有平台
python scripts/fetch_hotspot.py all

# 单独抓取某一平台
python scripts/fetch_hotspot.py weibo
python scripts/fetch_hotspot.py baidu
python scripts/fetch_hotspot.py douyin
```

### 返回数据格式

```json
{
  "weibo": {
    "platform": "weibo",
    "data": [
      {"rank": 1, "title": "热搜标题", "hot": 1234567, "category": "娱乐", "label": "爆"}
    ]
  },
  "baidu": {
    "platform": "baidu",
    "data": [
      {"rank": 1, "title": "热搜标题", "hot": 9876543, "desc": "描述"}
    ]
  },
  "douyin": {
    "platform": "douyin",
    "data": [
      {"rank": 1, "title": "热搜标题", "hot": 4567890, "url": "链接"}
    ]
  }
}
```

## 数据源说明

| 平台 | 数据源 | 更新频率 | 备注 |
|------|--------|----------|------|
| 微博 | https://weibo.com/ajax/side/hotSearch | 实时 | 官方公开接口，稳定性高 |
| 百度 | https://top.baidu.com/api/board | 实时 | 公开JSON接口 |
| 抖音 | https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/ | 实时 | 官方公开接口 |

## 注意事项

1. **网络依赖** - 需要网络连接才能获取数据
2. **接口稳定性** - 公开接口可能随时变更，建议添加异常处理
3. **频率限制** - 避免高频调用，建议缓存结果
4. **User-Agent** - 脚本已内置浏览器User-Agent

## 脚本位置

- 主脚本: `scripts/fetch_hotspot.py`