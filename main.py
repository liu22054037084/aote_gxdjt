import re
import os
import time
import shutil
import random
from pypinyin import lazy_pinyin
from dotenv import load_dotenv
from get_files.mp4_files import mp4_files
from sql_class.sql_ite import SQLiteDB
from sql_class.my_sql import MySQLDB


def main(FilesVideo, VideoUrl, GuaGen, DB, SQL, ReH, c=0, cs=30):
    while True:

        c = c + 1

        if c == cs:
            break

        DB.create_table('relay_table', 'key TEXT PRIMARY KEY ASC ON CONFLICT REPLACE, files TEXT')

        files, files_key = mp4_files(path=FilesVideo)

        data = [(file_key, files[file_key]) for file_key in files_key]

        DB.insert_many_rows("relay_table", data, "(key, files)")

        files_key = [ReH.sub('', item) for item in files_key]

        key_like = list(set(files_key))

        list_b = DB.query_target_table(tiao_jian=key_like, from_table="reserve_table", zd_table="like_l")

        if list_b is not None:

            list_c = DB.query_target_table(tiao_jian=key_like, from_table="relay_table", zd_table="key", like_l=True)

            q = 0

            if list_b[0][8] is None:
                vod_en = ''.join(lazy_pinyin(list_b[0][0]))
                vod_letter = vod_en[0].upper()
                q = q + 1

            if list_b[0][-2] is None:
                continue
            else:
                if not ("<p>" in list_b[0][-2] or "</p>" in list_b[0][-2]):
                    vod_blurb = '<p>' + list_b[0][-2].replace(' ', '').replace('。', '。</p><p>').replace('！', '！</p><p>').replace('？', '？</p><p>').replace('<p></p>', '</p>') + '</p>'
                    q = q + 1

            if q == 1:
                DB.update_rows('reserve_table', f"vod_en = '{vod_en}', vod_letter = '{vod_letter}'", f"name = '{list_b[0][0]}'")
            elif q == 2:
                DB.update_rows('reserve_table', f"vod_en = '{vod_en}', vod_letter = '{vod_letter}', vod_blurb = '{vod_blurb}' ", f"name = '{list_b[0][0]}'")

            cp1 = ''

            for i in range(len(list_c)):

                cp = f"{list_b[0][2]}/{list_b[0][3]}/{list_c[i][0]}"

                if list_b[0][4] is None:
                    ys = '#'
                else:
                    ys = list_b[0][4]

                if cp1 == '':
                    cp1 = VideoUrl + cp
                else:
                    cp1 = cp1 + '#' + VideoUrl + cp

                if cp not in ys:
                    shutil.copy(f'{list_c[i][1]}', f'{GuaGen}/{list_b[0][2]}/{list_b[0][3]}/')
                    DB.update_rows('reserve_table', f"url_video_path = '{cp1}'", f"name = '{list_b[0][0]}'")

            qtb = SQL.select_rows(table_name='mac_vod', condition=f"vod_name='{list_b[0][0]}'")
            if not qtb:
                l_b = DB.query_target_table(tiao_jian=key_like, from_table="reserve_table", zd_table="like_l")
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
                SQL.insert_row(table_name='mac_vod', headers=["type_id", "vod_name", "vod_sub", "vod_en", "vod_pic", "vod_pic_thumb", "vod_pic_slide", "vod_pic_screenshot", "vod_letter", "vod_class", "vod_content", "vod_pubdate", "vod_area", "vod_lang", "vod_year", "vod_state", "vod_time", "vod_time_add", "vod_time_hits", "vod_play_url", "vod_trysee", "vod_play_from", "vod_play_server", "vod_status"],
                               values=[q, f"'{l_b[0][0]}'", f"'{l_b[0][7]}'", f"'{l_b[0][8]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][10]}'", f"'{l_b[0][9]}'", f"'{l_b[0][3]}月'", f"'{l_b[0][11]}'", tm, type_id, type_id, l_b[0][2], f"'{l_b[0][4]}'", l_b[0][12], l_b[0][12], l_b[0][12], f"'{cp1}'", 1, "'dplayer'", "'no'", 1])
            elif qtb[0][4] == list_b[0][0]:
                SQL.update_field(table_name='mac_vod', field_name="vod_play_url", new_value=f"'{cp1}'", conditions=[f"vod_name = '{list_b[0][0]}'"])
            DB.drop_table('relay_table')
        time.sleep(30)


def main_run():
    # 加载 .env 文件中的环境变量
    load_dotenv()

    # 从 .env 文件中获取 BD 配置
    files_video = os.getenv('files_video')
    video_url = os.getenv('video_url')
    gua_gen = os.getenv('gua_gen')

    # 从 .env 文件中获取 MySQLDB 配置
    mysql_host = os.getenv('host')
    mysql_user = os.getenv('user')
    mysql_password = os.getenv('password')
    mysql_database = os.getenv('database')

    # 从 .env 文件中获取 SQLiteDB 配置
    sqlite_db_file = os.getenv('db_file')

    try:

        while True:
            re_h = re.compile(r'(?:\[|\(|\{|\s)(\d+)(?:\s*v\s*\d+)?(?:]|\)|}|\s)(\[\d*v\d]|\(\d*v\d\)|\[V\d]|\(V\d\))?.*')
            db = SQLiteDB(db_file=sqlite_db_file)
            sql = MySQLDB(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)

            main(files_video, video_url, gua_gen, db, sql, re_h)
    finally:

        db = SQLiteDB(db_file=sqlite_db_file)

        db.drop_table('relay_table')


if __name__ == "__main__":
    main_run()
