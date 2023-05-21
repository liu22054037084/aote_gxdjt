import requests


def v3_get(data, url):
    """
    :param url: 填写调用api地址 域名/api/v3/site/config
    :param data: 组装账户信息 data = {'userName': '', 'Password': ''}
    :return: 返回cookies
    """

    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers, json=data)

    cookies = response.headers.get('Set-Cookie')

    return cookies
