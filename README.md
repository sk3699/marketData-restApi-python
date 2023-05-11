**REST API for storing, Fetching and Deleting Market Data.**

Prerequisites:

    Python 3.10

Please follow below steps to start up the app.

1.  After cloning the repo, for creating a virtual environment to run the app use below command in cmd. This creates virtual space named venv in current dir.

        python -m venv venv

2.  To start up the virtual environment run activate script in venv\Scripts\activate.bat

    1.  For Windows

            venv\Scripts\activate.bat

    2.  For Linux

            source venv/Scripts/activate

3.  Install the requirements by running below command.

        pip install -r requirements.txt

4.  Run the DB migrations for creating sqlite3 DB. And migrate the prices DB models.

        python manage.py makemigrations prices
        

        python manage.py migrate prices

5.  Now we are ready to spin up the server by using below command.

        python manage.py runserver

6.  We can hit the API at "http://127.0.0.1:8000/markets/". To keep it simple this single endpoint handles all the requests (GET, POST, DELETE). POST request creates a the entries in the database.
    DELETE request deletes are the entries in the database.

7.  Below is the sample payload which can be used for POST request. Which has the list of Market Data.

        [
            {
            "option": "brn",
            "delivery_month": "Apr24",
            "call_put": "call",
            "price": 400,
            "currency_units": "USD/BBL"
            },
            {
            "option": "HH",
            "delivery_month": "Sep24",
            "call_put": "call",
            "price": 300,
            "currency_units": "USD/MMBTu"
            }
        ]
