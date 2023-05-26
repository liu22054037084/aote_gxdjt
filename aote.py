import re
import os
import time
import shutil
import random
import logging
import filecmp
import logging.handlers
import requests
from pypinyin import lazy_pinyin
from dotenv import load_dotenv
from get_files.mp4_files import mp4_files
from sql_class.sql_ite import SQLiteDB
from sql_class.my_sql import MySQLDB


def my_lists(FilesVideo, DB, ReH):  # 这个是处理获取的视频地址与名称，并且把名称用集合进行去重
    """
    :param FilesVideo:
    :param DB: 本地数据的调用对象
    :param ReH: 正则的加载调用
    :return: 返回集合进行去重列表
    """
    files, files_key = mp4_files(path=FilesVideo)

    data = [(file_key, files[file_key]) for file_key in files_key]

    DB.insert_many_rows("relay_table", data, "(key, files)")

    files_key = [ReH.sub('', item) for item in files_key]

    my_list = [key for key in list(set(files_key)) if key is not None and key.strip() != '']

    return my_list


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


def information_handling(gen_cp, logger, list_b, DB, VideoUrl, cp_up):  # 对影视一些信息加工用来符合影视网站所储存的信息模式的函数
    """
    :param gen_cp: 这个是以服务器为根，到达已经储存在挂在网盘各个资源的准确地址(这个地址是可以直接调用到某个文件的绝对路径，注意是以服务器主目录为跟)
    :param logger: 日志的调用函数，不需要在意
    :param list_b: 这是获取的reserve_table数据库指定数据主键name的数据(是一个二维数组，注意所有的DB本地数据库输出的均为二维数组)
    :param DB: 本地数据的调用对象
    :param VideoUrl: 这是直链的前分享地址
    :param cp_up: 以服务器挂在的网盘为根目录，然后到达各个资源分类的路径
    :return:
    """
    if not os.path.exists(gen_cp):  # 检查源文件是否存在
        logger.info(f'路径不存在创建属于《{list_b[0][0]}》路径')
        os.makedirs(gen_cp)

    if (list_b[0][8] or list_b[0][9]) is None:
        vod_en = ''.join(lazy_pinyin(list_b[0][0]))  # 汉字转拼音
        vod_letter = vod_en[0].upper()  # 获取拼音大写
        DB.update_rows('reserve_table', f"vod_en = '{vod_en}', vod_letter = '{vod_letter}'", f"name = '{list_b[0][0]}'")  # 写入数据库

    if list_b[0][10] is not None:
        if 'gxdjt.cf' not in list_b[0][10]:
            cg = download_image(list_b[0][10], 'img.jpg', gen_cp)  # 下载图片，进行储蓄
            if cg == '成功':
                DB.update_rows('reserve_table', f"vod_pic = '{VideoUrl}{cp_up}img.jpg'", f"name = '{list_b[0][0]}'")  # 写入数据库，把获取调用链接重新写入数据库进行替换原来的链接数据，主要是为了随便获取的图片链接失效，把他保存后变成自己的调用
                logger.info(f'图片下载转换成功img.jpg并储存在OneDrive上，然后保存现在的链接，方便后面调用！')

    if list_b[0][-2]:
        if not ("<p>" in list_b[0][-2] or "</p>" in list_b[0][-2]):
            vod_blurb = '<p>' + list_b[0][-2].replace('\t', '').replace('\n', '').replace(' ', '').replace('。', '。</p><p>').replace('！', '！</p><p>').replace('？', '？</p><p>').replace('<p></p>', '</p>') + '</p>'  # 对简介进行html加p标签的处理
            DB.update_rows('reserve_table', f"vod_blurb = '{vod_blurb}' ", f"name = '{list_b[0][0]}'")  # 写入数据库


def url_handling_write(list_c, cp_up, gen_cp, list_b, VideoUrl, logger, DB):  # 判断视频是否已经转移成功，然后组装所使用的视频外部的调用链接
    """
    :param list_c: 这是由relay_table列表的用模糊字段进行的模糊搜索返回的二维数组值(是一个二维数组，注意所有的DB本地数据库输出的均为二维数组)
    :param cp_up:  这个是以服务器为根，到达已经储存在挂在网盘各个资源的文件夹(非文件的具体的绝对地址)
    :param gen_cp: 这个是以服务器为根，到达已经储存在挂在网盘各个资源的准确地址(这个地址是可以直接调用到某个文件的绝对路径，注意是以服务器主目录为跟)
    :param list_b: 这是获取的reserve_table数据库指定数据主键name的数据
    :param VideoUrl: 这是直链的前分享地址
    :param logger: 日志的调用函数，不需要在意
    :param DB: 本地数据的调用对象
    :return:
    """
    cp1 = ''

    for i in range(len(list_c)):

        cp = f"{cp_up}{list_c[i][0]}"

        gen_fil = f'{gen_cp}{list_c[i][0]}'

        if list_b[0][5] is None:
            ys = '#'
        else:
            ys = list_b[0][5]

        if cp1 == '':
            cp1 = VideoUrl + cp
        else:
            cp1 = cp1 + '#' + VideoUrl + cp  # 保证两个视频链接直接存在一个#用于区分视频每个链接的独立性

        if list_c[i][0] not in ys:

            if os.path.exists(gen_fil):
                # 比较源文件和目标文件是否相同
                if filecmp.cmp(f'{list_c[i][1]}', gen_fil):
                    logger.info(f'{list_c[i][0]}的文件已存在且相同,跳过')
                else:
                    logger.info(f'{list_c[i][0]}的文件已存在且且不同进行覆盖！')
                    logger.info(f'f"正在执行》》 {gen_cp} 到 {list_c[i][1]} 》》的视频转移！')
                    shutil.copy2(f'{list_c[i][1]}', gen_cp)
                    logger.info(f'执行把组装链接写入数据库')
                    DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")
                    logger.info(f'组装链接写入完成')
            else:
                logger.info(f'f"正在执行》》 {gen_cp} 到 {list_c[i][1]} 》》的视频转移！')
                shutil.copy2(f'{list_c[i][1]}', gen_cp)
                logger.info(f'执行把组装链接写入数据库')
                DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")  # 每拷贝一次，就把组成的链接进行写入数据库
                logger.info(f'组装链接写入完成')
        else:
            logger.info(f'{list_c[i][0]}的视频已经存在链接当中')

    return cp1


def sql_decide_handling_write(SQL, list_b, DB, key, logger, cp1, vod_dplayer):  # 对远程mysql数据库进行确认数据是否存在，存在则只会更新链接数据，不存在则重新组装写入写入一条新的数据(也就是影视网站当中会显示的内容)
    """
    :param SQL: 远程MySQL数据对象
    :param list_b: 这是获取的reserve_table数据库指定数据主键name的数据(是一个二维数组，注意所有的DB本地数据库输出的均为二维数组)
    :param DB: 本地数据的调用对象
    :param key: 这是由集合去重后用for迭代的一个值
    :param logger: 日志的调用函数，不需要在意
    :param cp1: 组装的成品链接，每个链接是可以直接外部调用的，并且每个独立链接之间用#隔开(符合视频视频数据库链接储存方式)
    :param vod_dplayer: 视频所需要播放器的调用id名称
    :return:
    """
    qtb = SQL.select_rows(table_name='mac_vod', condition=f"vod_name='{list_b[0][0]}'")
    if not qtb:
        l_b = DB.query_target_table(tiao_jian=key, from_table="reserve_table", zd_table="like_l")
        if l_b[0][3] == 1:
            startq = 1
            endq = 4
        elif l_b[0][3] == 4:
            startq = 4
            endq = 7
        elif l_b[0][3] == 7:
            startq = 7
            endq = 10
        elif l_b[0][3] == 10:
            startq = 10
            endq = 12
        if l_b[0][6] == 1:
            type_id = "'大陆'"
            q = 2
        elif l_b[0][6] == 2:
            type_id = "'日韩'"
            q = 3
        elif l_b[0][6] == 3:
            type_id = "'欧美'"
            q = 4
        elif l_b[0][6] == 4:
            type_id = "'大陆'"
            q = 1
        elif l_b[0][6] == 5:
            type_id = "'日韩'"
            q = 1
        elif l_b[0][6] == 6:
            type_id = "'欧美'"
            q = 1
        randomq = random.randint(startq, endq)
        random_day = random.randint(1, 28)  # 假设每个月都是28天
        tm = f"'{l_b[0][2]}-{randomq:02d}-{random_day:02d}'"
        logger.info(f"笑死了开始第一次添加《{list_b[0][0]}》的视频数据！")
        SQL.insert_row(table_name='mac_vod', headers=["type_id", "vod_name", "vod_sub", "vod_en", "vod_pic", "vod_pic_thumb", "vod_pic_slide", "vod_pic_screenshot", "vod_letter", "vod_class", "vod_content", "vod_pubdate", "vod_area", "vod_lang", "vod_year", "vod_state", "vod_time", "vod_time_add", "vod_time_hits", "vod_play_url", "vod_trysee", "vod_play_from", "vod_play_server", "vod_status", "vod_level"],
                       values=[q, f"'{l_b[0][0]}'", f"'{l_b[0][7]}'", f"'{l_b[0][8]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][9]}'", f"'{l_b[0][3]}月'", f"'{l_b[0][11]}'", tm, type_id, type_id, l_b[0][2], f"'{l_b[0][4]}'", l_b[0][12], l_b[0][12], l_b[0][12], f"'{cp1}'", 1, f"'{vod_dplayer}'", "'no'", 1, 1])
    elif qtb[0][4] == list_b[0][0]:

        logger.info(f"笑死了这次只更新了一下《{list_b[0][0]}》的视频链接！")

        SQL.update_field(table_name='mac_vod', field_name="vod_play_url", new_value=f"'{cp1}'", conditions=[f"vod_name = '{list_b[0][0]}'"])


def main_major(logger, DB, FilesVideo, ReH, GuaGen, VideoUrl, SQL, vod_dplayer, c=0, cs=30):  # 这个是运行函数的主体函数

    """
    :param logger: 日志的调用函数，不需要在意
    :param DB: 本地数据的调用对象
    :param FilesVideo:
    :param ReH: 正则的加载调用
    :param GuaGen: 目标路径
    :param VideoUrl: 这是直链的前分享地址
    :param SQL: 远程MySQL数据对象
    :param vod_dplayer: 视频所需要播放器的调用id名称
    :param c: 简单的集数函数，用来确认当前已经循环多少次了
    :param cs: 每一次获取数据库对象后循环的次数(防止数据库对象访问失效，当一次数据库对象已经循环cs次数后用于判断跳出此次循环，以达到重新获取数据库对象的过程)
    :return:
    """

    while True:

        c = c + 1

        if c == cs:
            break
        logger.info(f'新处理第{c}数据relay_table表创建！')

        DB.create_table('relay_table', 'key TEXT PRIMARY KEY ASC ON CONFLICT REPLACE, files TEXT')

        logger.info('处理开始执行了！')

        my_list = my_lists(FilesVideo=FilesVideo, DB=DB, ReH=ReH)

        for key in my_list:

            list_b = DB.query_target_table(tiao_jian=key, from_table="reserve_table", zd_table="like_l")

            if list_b is not None:
                list_c = DB.query_target_table(tiao_jian=key, from_table="relay_table", zd_table="key", like_l=True)

                cp_up = f"{list_b[0][2]}/{list_b[0][3]}/{list_b[0][0].strip()}/"

                gen_cp = f"{GuaGen}/{list_b[0][2]}/{list_b[0][3]}/{list_b[0][0].strip()}/"

                information_handling(gen_cp=gen_cp, logger=logger, list_b=list_b, DB=DB, VideoUrl=VideoUrl, cp_up=cp_up)

                cp1 = url_handling_write(list_c=list_c, cp_up=cp_up, gen_cp=gen_cp, list_b=list_b, VideoUrl=VideoUrl, logger=logger, DB=DB)

                sql_decide_handling_write(SQL=SQL, list_b=list_b, DB=DB, key=key, logger=logger, cp1=cp1, vod_dplayer=vod_dplayer)

                logger.info(f'{list_b[0][0]}链接已经存在，但是需要更新一下，以防止链接出现问题需要手动更改！')

                DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")  # 每拷贝一次，就把组成的链接进行写入数据库

                logger.info(f'链接保险写入已完成！')

        DB.drop_table('relay_table')
        logger.info(f'完成新处理第{c}数据relay_table表删除！')
        logger.info(f'新处理的一次操作完成！')
        logger.info('进入三十秒沉默！')

        time.sleep(30)


def get_run():  # 获取运行所需要的.env所储存的各种变量以及log变量定义

    """
    :return:
    """

    # 加载 .env 文件中的环境变量
    load_dotenv()

    # 添加日志配置
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('main_run')
    logger.setLevel(logging.DEBUG)

    # 从环境变量获取保留日期，如果未定义，则默认为七天
    log_retention_days = int(os.getenv('LOG_RETENTION_DAYS', 7))

    # 创建FileHandler，并设置日志文件名和保留时间
    log_file = 'auto_delete_log_date.log'
    file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=log_retention_days)
    file_handler.setLevel(logging.DEBUG)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将FileHandler添加到Logger中
    logger.addHandler(file_handler)

    # 从 .env 文件中获取 BD 配置
    files_video = os.getenv('files_video')
    video_url = os.getenv('video_url')
    gua_gen = os.getenv('gua_gen')
    vod_dplayer = os.getenv('vod_dplayer')

    # 从 .env 文件中获取 MySQLDB 配置
    mysql_host = os.getenv('host')
    mysql_user = os.getenv('user')
    mysql_password = os.getenv('password')
    mysql_database = os.getenv('database')

    # 从 .env 文件中获取 SQLiteDB 配置
    sqlite_db_file = os.getenv('db_file')

    return logger, files_video, video_url, gua_gen, vod_dplayer, mysql_host, mysql_user, mysql_password, mysql_database, sqlite_db_file


def main_run():  # main第一次运行函数，用来确认配置文件是否存在，不存在创建配置函数

    """
    :return:
    """

    # 检测是否存在 .env 文件
    if not os.path.exists('.env'):
        # 创建 .env 文件
        with open('.env', 'w') as file:
            # 写入内容到 .env 文件
            file.write("""
                [BD]
                # 需转移的目录                             例如:/store/temp/download
                files_video=
                
                # 这是直链的前分享地址                      例如:https://video.example.com/file
                video_url=
                
                # 目标路径                                 例如/store/void
                gua_gen=
                
                # 选择使用的播放器默认dplayer
                vod_dplayer=dplayer
                
                # log保留天数默认为七天
                LOG_RETENTION_DAYS=7
                
                [MySQLDB]
                # mysql数据库地址                          例如:https://mysql.example.com/
                host=
                
                # mysql数据库账户                          例如:admin
                user=
                
                # mysql数据库密码                          例如:password
                password=
                
                # mysql数据库名                            例如:my_void
                database=
                
                [SQLiteDB]
                # 本地数据库地址(缓存,记录状态)              例如:./date/DS.db
                db_file=

            """)

        # 停止运行
        raise SystemExit('已创建 .env 文件，请写入相关配置！')


def main():  # 运行函数
    """
    :return:
    """

    main_run()

    logger, files_video, video_url, gua_gen, vod_dplayer, mysql_host, mysql_user, mysql_password, mysql_database, sqlite_db_file = get_run()

    try:

        logger.info('程序开始运行')

        cs_z = 0

        while True:
            re_h = re.compile(r'(?:\[|\(|\{|\s)(\d+)(?:\s*v\s*\d+)?(?:]|\)|}|\s)(\[\d*v\d]|\(\d*v\d\)|\[V\d]|\(V\d\))?.*')
            db = SQLiteDB(db_file=sqlite_db_file)
            sql = MySQLDB(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)
            logger.info('数据库全部连接成功')
            logger.info(f'第{cs_z}数据库更新')

            cs_z += 1
            main_major(logger=logger, DB=db, FilesVideo=files_video, ReH=re_h, GuaGen=gua_gen, VideoUrl=video_url, SQL=sql, vod_dplayer=vod_dplayer)
            logger.info(f'完成{cs_z}次完循环处理！')
    finally:

        db = SQLiteDB(db_file=sqlite_db_file)
        db.drop_table('relay_table')
        logger.info(f'错误或者强制退出')
