DROP FUNCTION IF EXISTS find_images;

CREATE
OR REPLACE FUNCTION find_images(
    p_name_search VARCHAR (255),
    p_username VARCHAR (255) DEFAULT NULL,
    p_is_public BOOLEAN DEFAULT NULL
) RETURNS TABLE (
    username VARCHAR(255),
    image_name VARCHAR(255),
    is_public BOOLEAN,
    added_date TIMESTAMP
) AS $$ BEGIN
    RETURN QUERY
    SELECT
        image_user.username,
        image.image_name,
        image.is_public,
        image.added_date
    FROM
        image
        INNER JOIN image_user ON image.user_id = image_user.user_id
    WHERE
        image.image_name LIKE '%' || p_name_search || '%'
        AND (
            p_username IS NULL
            OR image_user.username = p_username
        )
        AND (
            p_is_public IS NULL
            OR image.is_public = p_is_public
        )
        AND (
            (
                p_username IS NULL
                AND image.is_public
            )
            OR (
                p_username IS NOT NULL
            )
        );

END;

$$ LANGUAGE 'plpgsql';