
This project contains a website created with Django 3.1.1, Python 3.7, HTML 5 and CSS combined with the library Bootstrap 4. It is managed by gunicorn.

## Installation (not required as already installed on the server)

Using the package manager [pip](https://pip.pypa.io/en/stable/):

Upgrade **pip** and install all the requirements:
```bash
pip3 install --upgrade pip
pip3 install --no-cache-dir -r requirements.txt
```

The project uses the database PostgreSQL which has to be downloaded [here](https://www.postgresql.org/download/) in order to create a database for the website (I would recommand to download the [Postgres App](https://postgresapp.com/)).

## To update the webserver code
1. Connect to the machine in a Terminal
```ssh -i "goodness-groceries.pem" admin@goodnessgroceries.com ```

2. Pull changes from the github repository
```
cd ~/git/BSP3
git pull
```

3. Migrations commands
```
python3 manage.py makemigrations
python3 manage.py migrate
```

4. Restart unicorn
```
sudo systemctl restart gunicorn
```

## Check the webserver status
Execute this command to check the webserver status
```
sudo systemctl status gunicorn
```

## Usage to run on a local machine (for test purpose-only)

To run the webiste on your local machine:
- Open the Postgres App and create a server and a database
- Open the project and go to the directory "GoodnessGroceries_Project" in the main folder
- Open the python file "settings.py" and scroll down to "DATABASES", there you have to change the settings such that it corresponds to your created databse
- Open the terminal and go to the folder where the project is located (the "manage.py" file should be located in this folder)
- Being in this folder in the terminal, run the command ``` python3 manage.py runserver``` (The database server has to be running)
- The server is now running on your local host, to access the webiste go to some browser (Chrome was used for developping) and go to http://localhost:8000/, this will redirect you to your local host with the port 8000 where the webiste is running
