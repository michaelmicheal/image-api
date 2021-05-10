import psycopg2
from api.constants import HOST, DATABASE, USER, PASSWORD
from api.api_exceptions import (
    ImageDoesNotExistError,
    ImageAlreadyExistsError,
    DatabaseAuthenticationError,
    UserDoesNotExistError,
)


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
            if exc_type == None:
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

    def get_image_info(self, username, image_name):
        user_id = self.get_user_id(username)
        if user_id is None:
            raise UserDoesNotExistError
        self.execute(
            "SELECT username, image_name, is_public, added_date FROM get_image(%s, %s)",
            (image_name, username),
        )
        image_info = self.cur.fetchone()
        if image_info is None:
            raise ImageDoesNotExistError()
        return image_info

    def get_user_id(self, username):
        self.execute("SELECT get_user_id FROM get_user_id(%s)", (username,))
        return self.cur.fetchone()[0]

    def add_user(self, username):
        self.execute("INSERT INTO image_user(username) VALUES(%s)", (username,))

    def add_image(self, username, image_name, is_public):
        try:
            self.execute(
                "INSERT INTO image(image_name, user_id, is_public)"
                f"VALUES(%s, (SELECT get_user_id(%s)), %s)",
                (image_name, username, is_public),
            )
        except psycopg2.errors.UniqueViolation:
            raise ImageAlreadyExistsError

    def find_images(self, name_search, username, is_public):
        self.execute(
            "SELECT username, image_name, is_public, added_date FROM find_images(%s, %s, %s)",
            (name_search, username, is_public),
        )
        return self.cur.fetchall()
