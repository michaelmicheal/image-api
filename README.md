### About the Project

This purpose of this project is to create an image repository API. It uses the Flask web framework to handle requests, along with a PostgreSQL database to store users and image information.

### Use & Setup

To set up this project,

1. Install dependencies by executing `pip install -r requirements.txt` in the terminal from the main project directory.
2. Rename the '.sample_env' file to '.env' and update the environment variables in the file according to your PostgreSQL database.
3. Run the 'database_setup.py' file
4. Run the 'image_api.py' file by executing `python api/image_api.py` in the terminal from the main project directory.

To use the project, you can make GET and POST requests to the api endpoints defined in the image_api.py file.
