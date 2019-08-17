from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import json
from Singleton import Singleton


class MysqlDB(Singleton):
    def __init__(self, config_file='./db_config.json'):
        self.connect_str = None
        self.engine = self.init_db_engine_from_config(config_file)
        self.session_maker = None

    def init_db_connection(self, address, port, username, password, db_name):
        values = dict()
        values['address'] = address
        values['port'] = port
        values['username'] = username
        values['password'] = password
        values['db_name'] = db_name

        # 字典格式化
        template_conn_str = 'mysql+pymysql://{username}:{password}@{address}:{port}/{db_name}?charset=utf8'
        conn_str = template_conn_str.format(**values)

        # 参数说明connect_args直接传入connect pool创建
        # max_overflow：可以超过连接池总数的连接，默认是10个
        # pool_size： 连接池中连接的个数，默认是5
        # pool_recycle：连接回收的时间，默认是-1，不回收
        # echo_pool：是否打印日志
        engine = create_engine(conn_str,
                               connect_args={'charset': 'utf8'},
                               encoding='utf-8',
                               max_overflow=5,
                               pool_size=5,
                               pool_recycle=-1,
                               echo_pool=True)

        self.connect_str = conn_str

        return engine

    def init_db_engine_from_config(self, config_file):
        with open(config_file) as f:
            db_conf = json.load(f)['db']
        return self.init_db_connection(**db_conf)

    def create_session(self):
        if self.session_maker is None:
            # session_maker是一个类
            self.session_maker = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=self.engine))
        return self.session_maker

    def __repr__(self):
        return 'MysqlDB({})'.format(self.connect_str)
