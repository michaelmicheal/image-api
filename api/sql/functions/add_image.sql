DROP FUNCTION IF EXISTS add_image;

CREATE
OR REPLACE FUNCTION add_image(
    image_name VARCHAR (255),
    user_id INT,
    is_public BOOLEAN
) RETURNS VOID AS $$ BEGIN
    INSERT INTO
        image (image_name, user_id, is_public)
    VALUES
        (image_name, user_id, is_public);

END $$ LANGUAGE 'plpgsql';