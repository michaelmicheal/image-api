CREATE
OR REPLACE FUNCTION add_image(
    image_name VARCHAR (255),
    user_id INT,
    is_public BOOLEAN,
    file_location VARCHAR (255)
) RETURNS VOID AS $$ BEGIN
    INSERT INTO
        image (image_name, user_id, is_public, file_location)
    VALUES
        (image_name, user_id, is_public, file_location);

END $$ LANGUAGE 'plpgsql';