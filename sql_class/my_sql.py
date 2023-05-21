import mysql.connector
# pip install mysql-connector进行安装


class MySQLDB:

    def __init__(self, host, user, password, database):
        # 初始化MySQLDB类，连接到指定的MySQL数据库，并创建游标对象
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def execute(self, query):
        # 执行给定的SQL查询，并提交到数据库
        self.cursor.execute(query)
        self.conn.commit()

    def fetch(self, query):
        # 执行给定的SQL查询，并返回所有结果
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

    def insert_row(self, table_name, headers, values, conditions=None):
        # 插入一行数据到指定的表中，指定表名、表头、要插入的值和条件（可选）
        headers_str = ", ".join(headers)
        values_str = ", ".join(str(value) for value in values)

        query = f"INSERT INTO {table_name} ({headers_str}) VALUES ({values_str})"

        if conditions:
            conditions_str = " AND ".join(conditions)
            query += f" WHERE {conditions_str}"

        self.execute(query)

    def select_rows(self, table_name, condition=None):
        # 查询指定表中的所有行，可以指定一个条件过滤结果
        if condition:
            query = f"SELECT * FROM {table_name} WHERE {condition}"
        else:
            query = f"SELECT * FROM {table_name}"
        return self.fetch(query)

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

    def update_field(self, table_name, field_name, new_value, conditions=None):
        # 更新指定表中指定字段的数值，可指定条件
        query = f"UPDATE {table_name} SET {field_name} = {new_value}"

        if conditions:
            conditions_str = " AND ".join(conditions)
            query += f" WHERE {conditions_str}"

        self.execute(query)

# DB = MySQLDB('localhost', 'root', 'password', 'example')
# DB.create_table('students', 'name TEXT, age INTEGER')
# DB.insert_row('students', "'Alice', 25")
# DB.insert_row('students', "'Bob', 30")
# DB.update_rows('students', "age = 26", "name = 'Alice'")
# rows = DB.select_rows('students', "age > 25")
# for row in rows:
#     print(row)
# DB.delete_rows('students', "name = 'Bob'")
# DB.drop_table('students')
