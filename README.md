# Missing Person Detection System
Missing Person Detection System is a desktop application developed in Python and PyQt5 that helps in the detection and tracking of missing persons. The application also stores information about the missing person in a PostgreSQL database.

## Features
- GUI for easy interaction with the application
- Image processing for enhanced facial recognition
- Detects missing persons in a video recordings.
- Detects missing persons in a live video feed.
- Stores information about the missing person in a PostgreSQL database.
- Notifies the guardian when a missing person is detected.

## Getting Started
To get started with Book Barber, clone this repository to your local machine. Then, follow these steps:

1. Install Python 3 and the necessary libraries
2. Set up a PostgreSQL database and create the necessary tables using the SQL script provided in the database directory.
3. Run the backend by running `uvicorn main:app --port 8000` in the backend directory.
4. Run the frontend by running `python main.py` in the frontend directory.

# Contributing
If you would like to contribute to MPD, please follow these steps:

1. Fork this repository.
2. Create a new branch: git checkout -b <branch_name>.
3. Make your changes and commit them: git commit -m '<commit_message>'
4. Push to the original branch: git push origin e-lawyer/<location>
5. Create the pull request.

Alternatively see the GitHub documentation on creating a pull request.

# Acknowledgements
- [OpenCV](https://opencv.org/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [PostgreSQL](https://www.postgresql.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)  
- [Dlib](http://dlib.net/)
