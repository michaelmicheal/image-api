CREATE
OR REPLACE FUNCTION get_image(p_image_name VARCHAR (255), p_user_id INT) RETURNS VARCHAR (255) AS $$
DECLARE
    file_location VARCHAR (255);

BEGIN
    SELECT
        image.file_location INTO file_location
    FROM
        image
    WHERE
        image.image_name = p_image_name
        AND image.user_id = p_user_id;

RETURN file_location;

END;

$$ LANGUAGE 'plpgsql';