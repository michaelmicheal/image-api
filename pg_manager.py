import psycopg2
from constants import HOST, DATABASE, USER, PASSWORD


class DatabaseAuthenticationError(Exception):
    pass


class PGManager:
    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                database=DATABASE,
            )
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError:
            raise DatabaseAuthenticationError
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):

        try:
            self.conn.commit()
            self.cur.close()

        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def execute(self, sql, args=None):
        if ".sql" in sql:
            query = open(sql, "r").read()
        else:
            query = sql
        self.cur.execute(query, args)

    def get_image(self, image_name, user_id):
        self.execute(f"SELECT get_image(%s, %s)")
        return self.cur.fetchone()[0]

    def get_user_id(self, username):
        self.execute(f"SELECT get_user_id(%s)", (username,))
        return self.cur.fetchone()[0]

    def add_user(self, username):
        self.execute(f"INSERT INTO image_user(username) VALUES(%s)", (username,))

    def add_image(self, image_name, user_id, is_public, file_location):
        self.execute(
            "INSERT INTO image(image_name, user_id, is_public, file_location)"
            f"VALUES(%s, %s, %s, %s)",
            (image_name, user_id, is_public, file_location),
        )
