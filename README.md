# MPS database Dash App


## Install
Create virtual environment
```
python3 -m virtualenv venv
```
activate it
```
. venv/bin/activate
```
and install the dependencies
```
python3 -m pip install -r requirements.txt
```


## Setup environment variables

### Set up username and password

Set username and password
```
export MPS_DATABASE_USERNAME="my-username"
export MPS_DATAVBASE_PASSWORD="my-password"
export MPS_DATABASE_BASEURL="http://172.16.16.92:8004"
```

### Set caching options
Here showing the default values
```
export MPS_DATABASE_CACHE_DIR=/Users/finsberg/.cache/mps_database
export MPS_DATABASE_CACHE_DEFAULT_TIMEOUT=3600
```


## Running the app

### Debug

```
python3 -m app
```



### Production
Install `gunicorn`
```
python3 -m pip install gunicorn
```
and then
```
gunicorn app.main:server
```
