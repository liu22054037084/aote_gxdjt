import os


def mp4_files(logger, path):
    """
    :param path:获取文件的地址
    :return: 一个是含有路径的字典，一个是字典的建值，一个是文件字节大小
    """
    # file_list = [(file, os.path.join(root, file).replace("\\", "/"), os.path.getsize(os.path.join(root, file)))\
    #           for root, dirs, files in os.walk(path) for file in files if file.endswith(".mp4")]

    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file).replace("\\", "/")
            if file_path.endswith(".mp4"):
                file_stitching = file, file_path
                file_list.append(file_stitching)
                logger.info("成功读取文件: %s", file)
            else:
                logger.error("错误的文件类型(已忽略): %s", file)

    get_files = {file[0]: file[1] for file in file_list} #获取文件路径
    get_files_key = [file[0] for file in file_list]      #获取文件
    return get_files, get_files_key
