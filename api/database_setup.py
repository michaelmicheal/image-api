from os import listdir
from api.pg_manager import PGManager

FUNCTIONS_PATH = "sql/functions"


with PGManager() as pgm:

    pgm.execute("sql/create_tables.sql")
    for file_name in listdir(FUNCTIONS_PATH):
        pgm.execute("/".join((FUNCTIONS_PATH, file_name)))
