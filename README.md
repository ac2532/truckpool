# Truckpool, web-application for communication and scheduling  

## Access the deployed web application:

Deployed website URL: https://truckpool.herokuapp.com 

URL to sign up: https://truckpool.herokuapp.com/signup/ 

URL to login: https://truckpool.herokuapp.com/signin/

### Few test users:

#### admin: 
* url to login: https://truckpool.herokuapp.com/admin/ 
* username: admin
* password: admin

#### truck driver:
* url to login: https://truckpool.herokuapp.com/signin_td/ 
* username: mariefranchouillard
* password: driver

#### customer:
* url to login: https://truckpool.herokuapp.com/signin_ct/ 
* username: saram
* password: customer



## Run the website on a local server

To run this project, install the git file and run the following command lines in the terminal:

```
$ conda create -n 'name' python=3.8 //This will create a virtual environment 

$ conda activate 'name' //to activate the virtual environment previously created

$ pip install django

$ pip install makemigrations //create database

$ pip install migrate

$ python manage.py runserver //to run the webapp locally
```

The url to sign up is: 'http://127.0.0.1:8000/signup/'

The url to login is: 'http://127.0.0.1:8000/signin/'

The admin url: 'http://127.0.0.1:8000/admin/'

To create a superuser (admin with a staff status):

```
$ python manage.py createsuperuser
```


