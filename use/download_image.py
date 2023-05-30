import os
import requests


def download_image(url, file_name, download_path):  # 下载图片的函数
    """
    :param url: 下载链接
    :param file_name: 下载后重新的命名包括后缀
    :param download_path: 下载指定的地址
    :return:
    """
    try:
        response = requests.get(url)  # 发起GET请求获取图片内容
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)  # 将图片内容写入文件
        print("图片下载成功！")
        return '成功'
    except requests.exceptions.RequestException as e:
        print("下载失败:", e)