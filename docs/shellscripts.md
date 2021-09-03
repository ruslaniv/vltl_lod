# Shell Scripts

Shells scripts are located in `./shellscripts/`

## `install_reqs`
Installs package dependencies. 
### Use
```
install-reqs [dev|development|Dev|development]
```
runs
`pipenv install -r ./requirements/dev.txt`  
and installs development dependecies

`install-reqs [prod|production|Prod|Production]`  
runs
`pipenv install -r ./requirements/prod.txt`  
and installs production dependecies

## `set_settings`
Set the Django server environment setting
### Use
`set_settings [dev|development|Dev|development]`  
searches `manage.py` and set the `"DJANGO_SETTINGS_MODULE"` to `"config.settings.dev"`
for development mode

`set_settings [prod|production|Prod|Production]`  
searches `manage.py` and set the `"DJANGO_SETTINGS_MODULE"` to `"config.settings.prod"`
for production mode