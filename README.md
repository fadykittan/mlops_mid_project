# mlops-mid-project
MLOps Mid Project

## Data Base
Create DB with the following user and password
```
DB_USER = 'mlops'
DB_PASSWORD = 'mlops'
DB_NAME = 'mlops_db'
```

See script `init.sql` for commands.

after you have the DB ready, run the script `load_data_to_db.py` script, that will create table and load the data in it.

## Run
There are 3 way to run the app

1. `main_test.py` to test the app with mock data
2. `main_csv_test.pt` to test the app with data from CSV file

## Docker
To build the docker image
```
docker build -t mlops-app .
```

To run the docker image
```
# To run the API with port mapping
docker run -p 8000:8000 mlops-app api

# To run the DB (no port mapping needed)
docker run mlops-app db
```
