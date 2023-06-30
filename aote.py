import datetime
import filecmp
import os
import os.path
import random
import re
import shutil
import time

from pypinyin import lazy_pinyin

from get_files.mp4_files import mp4_files
from sql_class.my_sql import MySQLDB
from sql_class.sql_ite import SQLiteDB
from use import check_env
from use.download_image import download_image


def filter_video(files, files_key, DB, ReH):  # 这个是处理获取的视频地址与名称，并且把名称用集合进行去重
    """
    :param files_key:
    :param files:
    :param DB: 本地数据的调用对象
    :param ReH: 正则的加载调用
    :return: 返回集合进行去重列表
    """
    data = [(file_key, files[file_key]) for file_key in files_key]

    DB.insert_many_rows("relay_table", data, "(key, files)")

    files_key = [ReH.sub('', item) for item in files_key]

    my_list = [key for key in list(set(files_key)) if key is not None and key.strip() != '']

    return my_list


def information_handling(gen_cp, logger, list_b, DB, VideoUrl, cp_up):
    if not os.path.exists(gen_cp):
        logger.info(f'{gen_cp}路径不存在创建属于《{list_b[0][0]}》路径')
        os.makedirs(gen_cp)

    if all(value is None for value in [list_b[0][8], list_b[0][9]]):
        vod_en = ''.join(lazy_pinyin(list_b[0][0]))
        vod_letter = vod_en[0].upper()
        DB.update_rows(f'reserve_table', f"vod_en = '{vod_en}', vod_letter = '{vod_letter}'", f"name = '{list_b[0][0]}'")

    if list_b[0][10] is not None and 'gxdjt.cf' not in list_b[0][10]:
        cg = download_image(list_b[0][10], 'img.jpg', gen_cp)
        if cg == '成功':
            image_url = f"{VideoUrl}{cp_up}img.jpg"
            DB.update_rows('reserve_table', f"vod_pic = '{image_url}'", f"name = '{list_b[0][0]}'")
            logger.info('图片下载转换成功img.jpg并储存在OneDrive上，然后保存现在的链接，方便后面调用！')

    if list_b[0][-2] and ("<p>" not in list_b[0][-2] and "</p>" not in list_b[0][-2]):
        vod_blurb = '<p>' + list_b[0][-2].replace('\t', '').replace('\n', '').replace(' ', '').replace('。', '。</p><p>').replace('！', '！</p><p>').replace('？', '？</p><p>').replace('<p></p>', '</p>') + '</p>'
        DB.update_rows('reserve_table', f"vod_blurb = '{vod_blurb}'", f"name = '{list_b[0][0]}'")


def url_handling_write(list_c, cp_up, gen_cp, list_b, VideoUrl, logger, DB):
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

        ys = list_b[0][5] if list_b[0][5] is not None else '#'

        if ys == '#' and i == 0:
            cp1 = ys + '#' + VideoUrl + cp
        else:
            cp1 = cp1 + '#' + VideoUrl + cp

        cp1 = "#".join(filter(None, set(cp1.split("#"))))
        cp1 = "#".join(sorted(cp1.split("#")))

        if list_c[i][0] not in ys:
            if os.path.exists(gen_fil):
                if filecmp.cmp(f'{list_c[i][1]}', gen_fil):
                    logger.info(f'{list_c[i][0]}的文件已存在且相同，跳过')
                else:
                    logger.info(f'{list_c[i][0]}的文件已存在但不同，进行覆盖！')
                    logger.info(f'正在删除未完全转移的文件: {gen_fil}')
                    os.remove(gen_fil)
                    logger.info(f'已删除未完全转移的文件')
                    logger.info(f'正在执行》》 {list_c[i][1]} 到 {gen_cp} 》》的视频转移！')
                    shutil.copy2(list_c[i][1], gen_cp)
                    logger.info(f'执行把组装链接写入数据库')
                    logger.info(f'组装链接写入完成')
            else:
                logger.info(f'正在执行》》 {list_c[i][1]} 到 {gen_cp} 》》的视频转移！')
                shutil.copy2(list_c[i][1], gen_cp)
                logger.info(f'{list_c[i][0]}转移完成！')
        else:
            logger.info(f'{list_c[i][0]}的视频已经存在链接当中')

        logger.info(f'最后更新链接')
        DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")
        logger.info(f'组装链接写入完成')

    return cp1


def sql_decide_handling_write(SQL, list_b, DB, key, logger, cp1, vod_dplayer):
    qtb = SQL.select_rows(table_name='mac_vod', condition=f"vod_name='{list_b[0][0]}'")

    if not qtb:
        l_b = DB.query_target_table(tiao_jian=key, from_table="reserve_table", zd_table="like_l")
        l_b_values = l_b[0]

        startq_mapping = {1: 1, 4: 4, 7: 7, 10: 10}
        type_id_mapping = {1: "'大陆'", 2: "'日韩'", 3: "'欧美'", 4: "'大陆'", 5: "'日韩'", 6: "'欧美'"}

        startq = startq_mapping.get(l_b_values[3], '')
        endq = startq + 3 if startq else ''
        type_id = type_id_mapping.get(l_b_values[6], '')
        q = 1 if startq and type_id else ''

        randomq = random.randint(startq, endq) if startq and endq else ''
        random_day = random.randint(1, 28) if startq and endq else ''
        tm = f"'{l_b_values[2]}-{randomq:02d}-{random_day:02d}'" if randomq and random_day else ''

        logger.info(f"开始添加《{list_b[0][0]}》的视频数据！")

        headers = [
            "type_id", "vod_name", "vod_sub", "vod_en", "vod_pic", "vod_pic_thumb", "vod_pic_slide",
            "vod_pic_screenshot", "vod_letter", "vod_class", "vod_content", "vod_pubdate", "vod_area",
            "vod_lang", "vod_year", "vod_state", "vod_time", "vod_time_add", "vod_time_hits", "vod_play_url",
            "vod_trysee", "vod_play_from", "vod_play_server", "vod_status", "vod_level"
        ]

        values = [
            q, f"'{l_b_values[0]}'", f"'{l_b_values[7]}'", f"'{l_b_values[8]}'", f"'{l_b_values[10]}'",
            f"'{l_b_values[10]}'", f"'{l_b_values[10]}'", f"'{l_b_values[10]}'", f"'{l_b_values[9]}'",
            f"'{l_b_values[3]}月'", f"'{l_b_values[11]}'", tm, type_id, type_id, l_b_values[2],
            f"'{l_b_values[4]}'", l_b_values[12], l_b_values[12], l_b_values[12], f"'{cp1}'", 1,
            f"'{vod_dplayer}'", "'no'", 1, 1
        ]

        SQL.insert_row(table_name='mac_vod', headers=headers, values=values)
    elif qtb[0][4] == list_b[0][0]:
        logger.info(f"更新了一下《{list_b[0][0]}》的视频链接！")
        SQL.update_field(table_name='mac_vod', field_name="vod_play_url", new_value=f"'{cp1}'",
                         conditions=[f"vod_name = '{list_b[0][0]}'"])


def process_files(logger, DB, FilesVideo, ReH, GuaGen, VideoUrl, SQL, vod_dplayer):
    """
    处理文件
    """
    DB.create_table('relay_table', 'key TEXT PRIMARY KEY ASC ON CONFLICT REPLACE, files TEXT')

    modified_time_Z = ''
    xh = 0

    while True:
        timestamp = os.path.getmtime(FilesVideo)
        modified_time_A = datetime.datetime.fromtimestamp(timestamp)

        if modified_time_A != modified_time_Z:
            files, files_key = mp4_files(logger=logger, path=FilesVideo)
            modified_time_Z = modified_time_A
        else:
            logger.info(f"摆烂三十秒！")
            time.sleep(30)
            break

        my_list = filter_video(files=files, files_key=files_key, DB=DB, ReH=ReH)

        if my_list is None:
            break

        process_list(logger=logger, DB=DB, my_list=my_list, GuaGen=GuaGen, VideoUrl=VideoUrl, SQL=SQL, vod_dplayer=vod_dplayer)
        DB.drop_table('relay_table')


def process_list(logger, DB, my_list, GuaGen, VideoUrl, SQL, vod_dplayer):
    """
    处理列表
    """
    for key in my_list:
        list_b = DB.query_target_table(tiao_jian=key, from_table="reserve_table", zd_table="like_l")

        if list_b is not None:
            list_c = DB.query_target_table(tiao_jian=key, from_table="relay_table", zd_table="key", like_l=True)

            cp_up = f"{list_b[0][2]}/{list_b[0][3]}/{list_b[0][0].strip()}/"
            gen_cp = f"{GuaGen}/{list_b[0][2]}/{list_b[0][3]}/{list_b[0][0].strip()}/"

            information_handling(gen_cp=gen_cp, logger=logger, list_b=list_b, DB=DB, VideoUrl=VideoUrl, cp_up=cp_up)

            cp1 = url_handling_write(list_c=list_c, cp_up=cp_up, gen_cp=gen_cp, list_b=list_b, VideoUrl=VideoUrl,
                                     logger=logger, DB=DB)

            sql_decide_handling_write(SQL=SQL, list_b=list_b, DB=DB, key=key, logger=logger, cp1=cp1,
                                      vod_dplayer=vod_dplayer)

            DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")
            logger.info(f'{list_b[0][0]}链接已经存在，但是需要更新一下，以防止链接出现问题需要手动更改！')
            logger.info(f'链接保险写入已完成！')


def main_loop(logger, DB, FilesVideo, ReH, GuaGen, VideoUrl, SQL, vod_dplayer, c=0, cs=30):
    """
    运行函数的主体函数
    """
    while True:
        c += 1

        if c == cs:
            break
        logger.info(f'开始处理第{c}次数据表！')
        process_files(logger=logger, DB=DB, FilesVideo=FilesVideo, ReH=ReH, GuaGen=GuaGen, VideoUrl=VideoUrl, SQL=SQL, vod_dplayer=vod_dplayer)
        logger.info(f'完成新处理第{c}数据relay_table表删除！')
        logger.info(f'新处理的一次操作完成！')
        logger.info('进入三十秒沉默！\n')
        time.sleep(30)


def main():
    check_env.chech_env_bool()  # check == true

    logger, files_video, video_url, gua_gen, vod_dplayer, mysql_host, mysql_user, mysql_password, mysql_database, sqlite_db_file = check_env.get_env_file()

    while True:
        try:
            logger.info('程序开始运行')

            cs_z = 0

            while True:
                re_h = re.compile(r'(?:\[|\(|\{|\s)(\d+)(?:\s*v\s*\d+)?(?:]|\)|}|\s)(\[\d*v\d]|\(\d*v\d\)|\[V\d]|\(V\d\))?.*')  # 匹配 {num}
                db = SQLiteDB(db_file=sqlite_db_file)
                sql = MySQLDB(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)
                logger.info('数据库全部连接成功')
                logger.info(f'第{cs_z}数据库更新')

                cs_z += 1
                main_loop(logger=logger, DB=db, FilesVideo=files_video, ReH=re_h, GuaGen=gua_gen, VideoUrl=video_url, SQL=sql, vod_dplayer=vod_dplayer)

                logger.info(f'完成{cs_z}次完循环处理！')
        except Exception as e:
            logger.exception(f'发生错误: {str(e)}')
        finally:
            db = SQLiteDB(db_file=sqlite_db_file)
            db.drop_table('relay_table')

            tc = 0
            for i in range(10, 0, -1):
                logger.exception(f"程序将在{i}秒后重启...\n\n请退出两次！")
                time.sleep(1)
                tc += 1

            if tc == 10:
                continue
