import hashids


def hashid(file_id):
    """
    :param file_id: 这个是文件的唯一id
    :return: 返回对文件id进行hash加密后变成hashid
    """

    # 初始化hashids对象

    hashids_salt = 'something really hard to guss'

    hashids_object = hashids.Hashids(salt=hashids_salt)
    # 生成Hash ID

    number = 2 # 可以指定，这个看自己的需求

    hash_id = hashids_object.encode(file_id, number)

    return hash_id
