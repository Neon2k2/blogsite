# Blogsite Project
This project is a simple blog site built using Python and Django. The blog site allows users to create accounts, write and publish blog posts, and read posts written by other users. The project includes the following features:

- User registration and authentication
- User profile page with user details and posts written by the user
- Ability to create, edit and delete blog posts
- Ability to view and search blog posts written by other users


## Getting Started

To run the project on your local machine, follow these steps:

- Clone the repository to your local machine using git clone https://github.com/Neon2k2/blogsite.git.
- Navigate to the project directory using cd blogsite.
- Create a virtual environment using python3 -m venv env.
- Activate the virtual environment using source env/bin/activate on Linux/Mac or env\Scripts\activate on Windows.
- Install the required packages using pip install -r requirements.txt.
- Run migrations using python manage.py migrate.
- Start the development server using python manage.py runserver.
- Open your web browser and go to http://127.0.0.1:8000/ to view the project.



The config directory contains the project settings and URL configurations. The blog directory contains the models, views, and templates for the blog app, while the users directory contains the models, views, and templates for the user authentication and profile pages.

The media directory contains user-uploaded media files, and the static directory contains static files such as CSS and JavaScript. The templates directory contains HTML templates used by the project.

The db.sqlite3 file is the default database used by the project, and manage.py is the Django management script.

# Contributing
If you would like to contribute to the project, please follow these steps:

- Fork the repository and create a new branch.
- Make your changes and test them locally.
- Create a pull request with a description of your changes.


## License
This project is licensed under the MIT License. See the LICENSE file for details.
