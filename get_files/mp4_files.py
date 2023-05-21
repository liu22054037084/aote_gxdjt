import os


def mp4_files(path):
    """
    :param path:获取文件的地址
    :return: 一个是含有路径的字典，一个是字典的建值，一个是文件字节大小
    """
    files = [(file, os.path.join(root, file).replace("\\", "/"), os.path.getsize(os.path.join(root, file))) for root, dirs, files in os.walk(path) for file in files if file.endswith(".mp4")]
    get_files = {file[0]: file[1] for file in files}
    get_files_key = [file[0] for file in files]
    return get_files, get_files_key

