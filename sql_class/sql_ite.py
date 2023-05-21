import sqlite3


class SQLiteDB:

    def __init__(self, db_file):
        # 初始化SQLiteDB类，连接到指定的数据库文件，并创建游标对象
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        # 执行给定的SQL查询，可传入参数，参数用于防止SQL注入，并提交到数据库
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def executemany(self, query, data):
        # 执行给定的SQL查询，可传入多个参数列表，参数用于防止SQL注入，并提交到数据库
        self.cursor.executemany(query, data)
        self.conn.commit()

    def fetch(self, query, params=None):
        # 执行给定的SQL查询，可传入参数，参数用于防止SQL注入，并返回所有结果
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_table(self, table_name, columns):
        # 创建一个新的表，指定表名和列名
        query = f"CREATE TABLE {table_name} ({columns})"
        self.execute(query)

    def drop_table(self, table_name):
        # 删除指定的表
        query = f"DROP TABLE {table_name}"
        self.execute(query)

    def insert_row(self, table_name, values, table_form=None):
        # 插入一行数据到指定的表中，指定表名和要插入的值(可以指定那些表格可以写入)
        query = f"INSERT INTO {table_name} {table_form} VALUES {values}"
        self.execute(query)

    def insert_many_rows(self, table_name, values_list, table_form=None):
        # 插入多行数据到指定的表中，指定表名和要插入的多行值(可以指定那些表格可以写入)
        placeholders = ','.join(['?' for _ in range(len(values_list[0]))])
        query = f"INSERT INTO {table_name} {table_form} VALUES ({placeholders})"
        self.executemany(query, values_list)

    def select_rows(self, table_name, condition=None):
        # 查询指定表中的所有行，可以指定一个条件过滤结果
        if condition:
            query = f"SELECT * FROM {table_name} WHERE {condition}"
        else:
            query = f"SELECT * FROM {table_name}"
        return self.fetch(query)

    def query_target_table(self, tiao_jian, zd_table, from_table, like_l=False):
        # 从集合表(collection_table)获取所有like_l的值
        if isinstance(tiao_jian, str):

            tiao_jianl = [tiao_jian]

        else:

            tiao_jianl = tiao_jian

        if not like_l:
            tiao_jianl = tuple(tiao_jianl)
            if len(tiao_jianl) > 2:
                tiao_jianl = tuple(tiao_jianl)
            else:
                tiao_jianl = f"('{tiao_jianl[0]}')"
            query = f"SELECT * FROM {from_table} WHERE {zd_table} IN {tiao_jianl}"
        else:
            condition = " OR ".join([f"{zd_table} LIKE '%{i.replace(r' ', '%').replace(r'_', '%')}%'" for i in tiao_jianl])
            query = f"SELECT * FROM {from_table} WHERE {condition}"

        result = self.fetch(query)

        if len(result) == 0:

            return None

        else:

            # 将结果构建成二维列表
            result_list = []

            for row in result:
                result_list.append(list(row))

            return result_list

    def update_rows(self, table_name, values, condition=None):
        # 更新指定表中的行，可以指定一个条件过滤要更新的行
        if condition:
            query = f"UPDATE {table_name} SET {values} WHERE {condition}"
        else:
            query = f"UPDATE {table_name} SET {values}"
        self.execute(query)

    def delete_rows(self, table_name, condition=None):
        # 删除指定表中的行，可以指定一个条件过滤要删除的行
        if condition:
            query = f"DELETE FROM {table_name} WHERE {condition}"
        else:
            query = f"DELETE FROM {table_name}"
        self.execute(query)

    def update_row(self, table_name, row_id, values, column_names=None):
        # 更新指定表中的一行，可以指定要更新的列和列值
        # 如果未指定列名，则默认按照原有列名的顺序进行更新
        if column_names:
            set_clause = ', '.join([f"{name} = ?" for name in column_names])
        else:
            set_clause = ', '.join([f"{name} = ?" for name in self.get_column_names(table_name)])
        query = f"UPDATE {table_name} SET {set_clause} WHERE ROWID = ?"
        self.execute(query, tuple(values) + (row_id,))

    def get_column_names(self, table_name):
        # 获取指定表的所有列名
        query = f"PRAGMA table_info({table_name})"
        result = self.fetch(query)
        return [row[1] for row in result]
