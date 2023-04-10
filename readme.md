To get this project up and running locally on your computer follow the following steps.
1. Change directory to the rxs116 folder

2. Set up a python virtual environment and activate it (optional):
    * To intialise, run: python3 -m venv venv
    * To activate:
        * on Windows run: venv/Scripts/activate
        * on Mac/Linux run: source venv/bin/activate
        
3. Run the following commands:
    * pip install -r requirements.txt
    * python3 manage.py makemigrations
    * python3 manage.py migrate
    * python3 manage.py createsuperuser
    * python3 manage.py runserver
   
4. Open a browser and go to http://localhost:8000/

