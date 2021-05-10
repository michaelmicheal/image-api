DROP FUNCTION IF EXISTS get_image;

CREATE
OR REPLACE FUNCTION get_image(
    p_image_name VARCHAR (255),
    p_username VARCHAR (255)
) RETURNS TABLE (
    image_name VARCHAR(255),
    username VARCHAR(255),
    is_public BOOLEAN,
    added_date TIMESTAMP
) AS $$ BEGIN
    RETURN QUERY
    SELECT
        image.image_name,
        image_user.username,
        image.is_public,
        image.added_date
    FROM
        image
        INNER JOIN image_user ON image.user_id = image_user.user_id
    WHERE
        image.image_name = p_image_name
        AND image_user.username = p_username;

END;

$$ LANGUAGE 'plpgsql';