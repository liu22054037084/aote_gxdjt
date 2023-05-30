import os
import logging
import logging.handlers
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler


def chech_env_bool():  # main第一次运行函数，用来确认配置文件是否存在，不存在创建配置函数

    """
    :return:
    """

    # 检测是否存在 .env 文件
    if not os.path.exists('.env'):
        # 创建 .env 文件
        with open('.env', 'w') as file:
            # 写入内容到 .env 文件
            file.write("""
                [log_l]
                #日志等级(目前拥有ERROR/INFO)              例如:ERROR
                log_level=error
                
                #日志名称                                 例如:error.log
                log_name=error.log
                
                # log保留天数默认为七天
                LOG_RETENTION_DAYS=7                
                
                # log分割防止一个logo文件过大以天为单位默认7
                LOG_INTERVAL_DAYS=7

                [BD]
                # 需转移的目录                             例如:/store/temp/download
                files_video=
                
                # 这是直链的前分享地址                      例如:https://video.example.com/file
                video_url=
                
                # 目标路径                                 例如/store/void
                gua_gen=
                
                # 选择使用的播放器默认dplayer
                vod_dplayer=dplayer
                
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
                # 本地数据库地址(缓存,记录状态)               例如:./assets/DS.db
                db_file=

            """)

        # 停止运行
        raise SystemExit('已创建 .env 文件，请写入相关配置！')


def get_env_file():  # 获取运行所需要的.env所储存的各种变量以及log变量定义

    """
    :return:
    """

    # 加载 .env 文件中的环境变量
    load_dotenv()

    # 获取用户输入的日志级别和文件名
    log_name = os.getenv('log_level')
    user_log_level = os.getenv('log_level')

    # 转换日志级别为相应的常量
    log_level = getattr(logging, user_log_level.upper(), None)
    if not isinstance(log_level, int):
        raise ValueError(f"无效的日志级别：{user_log_level}")

    # 创建日志记录器
    logger = logging.getLogger('my_logger')
    logger.setLevel(log_level)

    # 创建 TimedRotatingFileHandler 处理器
    handler = TimedRotatingFileHandler(filename=log_name, when='midnight', interval=int(os.getenv('LOG_RETENTION_DAYS')), backupCount=int(os.getenv('LOG_RETENTION_DAYS')))
    handler.setLevel(log_level)

    # 创建 StreamHandler 处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    # 配置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(handler)
    logger.addHandler(stream_handler)

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
