import feedparser
import requests

# 设置请求头部信息，伪装为浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 发送HTTP请求获取RSS源的内容
response = requests.get('https://mikanani.me/RSS/Bangumi?bangumiId=3001&subgroupid=552', headers=headers)

# 解析RSS源
feed = feedparser.parse(response.text)

# 逆序遍历并显示解析后的RSS信息
for entry in reversed(feed.entries):
    print("每一集的名字:", entry.title)
    print("每一集的名字:", entry.link)
    print('-'*50)
