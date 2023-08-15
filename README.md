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


## Set up username and password

Set username and password
```
export MPS_DATABASE_USERNAME="my-username"
export MPS_DATAVBASE_PASSWORD="my-password"
```

## Set caching options
Here showing the default values
```
export MPS_DATABASE_CACHE_DIR=/Users/finsberg/.cache/mps_database
export MPS_DATABASE_CACHE_DEFAULT_TIMEOUT=3600
```
