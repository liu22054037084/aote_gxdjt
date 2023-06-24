import os
import Levenshtein


def mp4_files(path):
    """
    :param path:获取文件的地址
    :return: 一个是含有路径的字典，一个是字典的建值，一个是文件字节大小
    """
    # file_list = [(file, os.path.join(root, file).replace("\\", "/"), os.path.getsize(os.path.join(root, file)))\
    #           for root, dirs, files in os.walk(path) for file in files if file.endswith(".mp4")]

    file_list = []
    allowed_extensions = [".mp4"]
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file).replace("\\", "/")
            if any(file_path.endswith(ext) for ext in allowed_extensions):
                file_stitching = file, file_path
                file_list.append(file_stitching)
            else:
                pass

    get_files = {file[0]: file[1] for file in file_list}  # 获取文件路径
    get_files_key = [file[0] for file in file_list]  # 获取文件
    return get_files, get_files_key


def group_similar_items(lst):
    groups = []
    for i in lst:
        added = False
        for group in groups:
            if any(similarity(i, existing_item) > 0.75 for existing_item in group):
                group.append(i)
                added = True
                break
        if not added:
            groups.append([i])

    # 构建二维数组
    r = []
    for group in groups:
        r.append(group)

    return r


def similarity(item1, item2):
    # 计算编辑距离相似度
    distance = Levenshtein.distance(item1, item2)
    max_length = max(len(item1), len(item2))
    similarity_score = 1 - distance / max_length
    return similarity_score


a, b = mp4_files("C:/Users/azxt/OneDrive - LAPT0")
result = group_similar_items(b)
for item in result:
    print(item)
