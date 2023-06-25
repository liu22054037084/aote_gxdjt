import requests
import feedparser
import re


def rss(url, proxies={'https': 'http://127.0.0.1:8889'}):
    querystring = {"bangumiId": "2967", "subgroupid": "615"}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url=url, params=querystring, proxies=proxies, headers=headers, timeout=5)

    # 解析RSS源
    feed = feedparser.parse(response.text)

    rss_dict = {}

    # 逆序遍历并显示解析后的RSS信息
    for i, entry in enumerate(reversed(feed.entries), start=1):
        # print(f"第{i}集的名字:", entry.title)
        # print(f"第{i}集的链接:", entry.link)

        if "www.dmhy.org" in url:
            # print(f"第{i}集torrent的特征码:", entry.links[1].href)
            rss_dict[entry.title] = entry.links[1].href

        elif "www.comicat.org" in url:
            # print(f"第{i}集torrent的特征码:", re.search(r"(?<=show-)[a-fA-F0-9]{40}", entry.link).group())
            rss_dict[entry.title] = re.search(r"(?<=show-)[a-fA-F0-9]{40}", entry.link).group()

        elif "mikanani.me" in url:
            # print(f"第{i}集torrent的特征码:", re.search(r"(?<=/)[a-fA-F0-9]{40}", entry.link).group())
            rss_dict[entry.title] = re.search(r"(?<=/)[a-fA-F0-9]{40}", entry.link).group()

        elif "bangumi.moe" in url:
            # print(f"第{i}集torrent链接:", entry.links[1].href)
            rss_dict[entry.title] = entry.links[1].href

        elif "nyaa.si" in url:
            # print(f"第{i}集torrent的特征码:", entry.nyaa_infohash)
            rss_dict[entry.title] = entry.nyaa_infohash

        elif "share.acgnx.se" in url:
            # print(f"第{i}集torrent的特征码:", re.search(r"(?<=show-)[a-fA-F0-9]{40}", entry.link).group())
            rss_dict[entry.title] = re.search(r"(?<=show-)[a-fA-F0-9]{40}", entry.link).group()

        elif "www.miobt.com" in url:
            # print(f"第{i}集torrent的特征码:", re.search(r"(?<=show-)[a-fA-F0-9]{40}", entry.link).group())
            rss_dict[entry.title] = re.search(r"(?<=show-)[a-fA-F0-9]{40}", entry.link).group()

        elif "acg.rip" in url:
            # print(f"第{i}集torrent链接:", entry.links[1].href)
            rss_dict[entry.title] = entry.links[1].href

    return rss_dict


# q = rss(url="")
# for i in q:
#     print(q[i])
