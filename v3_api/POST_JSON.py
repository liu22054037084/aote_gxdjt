import requests
import json


def v3_post(cookies, hash_id, url):
    """
    :param url: 填写调用api地址 域名/api/v3/file/source
    :param cookies: 登录信息
    :param hash_id:  hashid数组对
    :return: 返回josn分拣后的值形成字典对以名字为key
    不安全太慢，一样的缺点
    """

    payload = {"items": hash_id}
    headers = {
        "cookie": cookies,
        "content-type": "application/json;charset=UTF-8"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    json_data = response.text

    # 解析JSON数据
    data = json.loads(json_data)

    # 遍历data列表中的字典

    name_url_dict = {}

    for item in data['data']:
        # 提取name和url信息，并将其保存到字典中

        name_url_dict[item['name']] = item['url']

    # 打印结果

    print(name_url_dict)
