CREATE
OR REPLACE FUNCTION get_user_id(p_username VARCHAR (255)) RETURNS INT AS $$
DECLARE
    user_id INT;

BEGIN
    SELECT
        image_user.user_id INTO user_id
    FROM
        image_user
    WHERE
        image_user.username = p_username;

RETURN user_id;

END;

$$ LANGUAGE 'plpgsql';