import pymysql
from pymysql.cursors import DictCursor


class DataBase():
    def __init__(self):
        self.conn = pymysql.Connection(
            host='120.55.37.36',
            # host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='qi_dian',
            charset='utf8'
        )

    def __enter__(self):
        return self.conn.cursor(cursor=DictCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        return True

    def close(self):
        self.conn.close()


class BaseDao():
    def __init__(self):
        self.db = DataBase()

    def save(self, table_name, **item):
        print('*' * 40)
        sql = 'insert into %s(%s) values (%s)'
        fields = ','.join(item.keys())
        print('fields=', fields)
        field_place_holds = ','.join(['%%(%s)s' % key for key in item])
        print(field_place_holds)
        with self.db as cursor:
            print(sql % (table_name, fields, field_place_holds))

            cursor.execute(sql % (table_name, fields, field_place_holds), item)

            if cursor.rowcount > 0:
                return True

        return False


if __name__ == '__main__':
    DataBase()
