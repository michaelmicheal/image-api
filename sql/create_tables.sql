CREATE TABLE IF NOT EXISTS image_user (
    user_id serial PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS image (
    image_name VARCHAR (255) NOT NULL,
    user_id INT NOT NULL,
    is_public BOOLEAN NOT NULL,
    added_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    file_location VARCHAR (255) NOT NULL,
    PRIMARY KEY (image_name, user_id),
    FOREIGN KEY (user_id) REFERENCES image_user (user_id)
);