DROP FUNCTION IF EXISTS add_user;

CREATE
OR REPLACE FUNCTION add_user(username VARCHAR(50)) RETURNS VOID AS $$ BEGIN
    INSERT INTO
        image_user (username)
    VALUES
        (username);

END $$ LANGUAGE 'plpgsql';