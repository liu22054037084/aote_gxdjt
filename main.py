import re
import os
import time
import shutil
import random
import logging
import filecmp
import logging.handlers
from pypinyin import lazy_pinyin
from dotenv import load_dotenv
from get_files.mp4_files import mp4_files
from sql_class.sql_ite import SQLiteDB
from sql_class.my_sql import MySQLDB


def main(FilesVideo, VideoUrl, GuaGen, DB, SQL, ReH, logger, vod_dplayer, c=0, cs=30):
    while True:

        c = c + 1

        if c == cs:
            break
        logger.info(f'新处理第{c}数据relay_table表创建！')

        DB.create_table('relay_table', 'key TEXT PRIMARY KEY ASC ON CONFLICT REPLACE, files TEXT')

        logger.info('处理开始执行了！')

        files, files_key = mp4_files(path=FilesVideo)

        data = [(file_key, files[file_key]) for file_key in files_key]

        DB.insert_many_rows("relay_table", data, "(key, files)")

        files_key = [ReH.sub('', item) for item in files_key]

        my_list = [key for key in list(set(files_key)) if key is not None and key.strip() != '']

        for key in my_list:

            list_b = DB.query_target_table(tiao_jian=key, from_table="reserve_table", zd_table="like_l")

            if list_b is not None:

                list_c = DB.query_target_table(tiao_jian=key, from_table="relay_table", zd_table="key", like_l=True)

                q = 0

                if list_b[0][8] is None:
                    vod_en = ''.join(lazy_pinyin(list_b[0][0]))
                    vod_letter = vod_en[0].upper()
                    q = q + 1

                if list_b[0][-2] is None:
                    continue
                else:
                    if not ("<p>" in list_b[0][-2] or "</p>" in list_b[0][-2]):
                        vod_blurb = '<p>' + list_b[0][-2].replace('\t', '').replace('\n', '').replace(' ', '').replace('。', '。</p><p>').replace('！', '！</p><p>').replace('？', '？</p><p>').replace('<p></p>', '</p>') + '</p>'
                        q = q + 1

                if q == 1:
                    DB.update_rows('reserve_table', f"vod_en = '{vod_en}', vod_letter = '{vod_letter}'", f"name = '{list_b[0][0]}'")
                elif q == 2:
                    DB.update_rows('reserve_table', f"vod_en = '{vod_en}', vod_letter = '{vod_letter}', vod_blurb = '{vod_blurb}' ", f"name = '{list_b[0][0]}'")

                cp1 = ''

                for i in range(len(list_c)):

                    cp = f"{list_b[0][2]}/{list_b[0][3]}/{list_b[0][0]}/{list_c[i][0]}"
                    gen_cp = f"{GuaGen}/{list_b[0][2]}/{list_b[0][3]}/{list_b[0][0]}/"
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
                        if not os.path.exists(gen_cp):  # 检查源文件是否存在
                            logger.info(f'路径不存在创建属于《{list_b[0][0]}》路径')
                            os.makedirs(gen_cp)

                        destination_file = os.path.join(gen_fil, f'{list_c[i][1]}')
                        if os.path.exists(destination_file):
                            # 比较源文件和目标文件是否相同
                            if filecmp.cmp(f'{list_c[i][1]}', gen_fil):
                                logger.info(f'文件已存在且相同,跳过')
                            else:
                                logger.info(f'文件已存在且且不同进行覆盖！')
                                logger.info(f'f"正在执行》》 {list_c[i][1]} 到 {gen_cp} 》》的视频转移！')
                                shutil.copy2(f'{list_c[i][1]}', gen_cp)
                                logger.info(f'执行把组装链接写入数据库')
                                DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")
                                logger.info(f'组装链接写入完成')
                        else:
                            logger.info(f'f"正在执行》》 {list_c[i][1]} 到 {gen_cp} 》》的视频转移！')
                            shutil.copy2(f'{list_c[i][1]}', gen_cp)
                            logger.info(f'执行把组装链接写入数据库')
                            DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")  # 每拷贝一次，就把组成的链接进行写入数据库
                            logger.info(f'组装链接写入完成')
                    else:
                        logger.info(f'视频已经存在链接当中')

                logger.info(f'链接已经存在，但是需要更新一下，以防止链接出现问题需要手动更改！')
                DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")  # 每拷贝一次，就把组成的链接进行写入数据库
                logger.info(f'链接保险写入已完成！')

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
                    SQL.insert_row(table_name='mac_vod', headers=["type_id", "vod_name", "vod_sub", "vod_en", "vod_pic", "vod_pic_thumb", "vod_pic_slide", "vod_pic_screenshot", "vod_letter", "vod_class", "vod_content", "vod_pubdate", "vod_area", "vod_lang", "vod_year", "vod_state", "vod_time", "vod_time_add", "vod_time_hits", "vod_play_url", "vod_trysee", "vod_play_from", "vod_play_server", "vod_status"],
                                   values=[q, f"'{l_b[0][0]}'", f"'{l_b[0][7]}'", f"'{l_b[0][8]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][9]}'", f"'{l_b[0][3]}月'", f"'{l_b[0][11]}'", tm, type_id, type_id, l_b[0][2], f"'{l_b[0][4]}'", l_b[0][12], l_b[0][12], l_b[0][12], f"'{cp1}'", 1, f"'{vod_dplayer}'", "'no'", 1])
                elif qtb[0][4] == list_b[0][0]:

                    logger.info(f"笑死了这次只更新了一下《{list_b[0][0]}》的视频链接！")

                    SQL.update_field(table_name='mac_vod', field_name="vod_play_url", new_value=f"'{cp1}'", conditions=[f"vod_name = '{list_b[0][0]}'"])
        DB.drop_table('relay_table')
        logger.info(f'完成新处理第{c}数据relay_table表删除！')
        logger.info(f'新处理的一次操作完成！')
        logger.info('进入三十秒沉默！')

        time.sleep(30)


def main_run():
    # 检测是否存在 .env 文件
    if not os.path.exists('.env'):
        # 创建 .env 文件
        with open('.env', 'w') as file:
            # 写入内容到 .env 文件
            file.write("""
            [BD]
            # 用来添加获取视频的地址(最后要有/)
            files_video=
            
            # 这是直连的前分享地址(最后要有/)
            video_url=
            
            # 根目录到达要转移的地址或者是相对地址(最后不要有/)
            gua_gen=
            
            # 选择使用的播放器默认dplayer
            vod_dplayer=dplayer
            
            # log保留天数默认为七天
            LOG_RETENTION_DAYS=
            
            [MySQLDB]
            # mysql数据库地址
            host=
            
            # mysql数据库账户
            user=
            
            # mysql数据库密码
            password=
            
            # mysql数据库名
            database=
            
            [SQLiteDB]
            # 本地数据库地址
            db_file=
            """)

        # 停止运行
        raise SystemExit('已创建 .env 文件')

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
            main(files_video, video_url, gua_gen, db, sql, re_h, logger, vod_dplayer)
            logger.info(f'完成{cs_z}次完循环处理！')
    finally:

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

        db = SQLiteDB(db_file=sqlite_db_file)
        db.drop_table('relay_table')
        logger.info(f'错误或者强制退出')


if __name__ == "__main__":
    main_run()
