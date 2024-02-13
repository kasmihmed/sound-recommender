# sound recommender
## run in a docker container
```
docker compose up --build
```
will run on `http://localhost:7070`
## commands (without docker)
### 1. create a virtual env
inside to the `soundrecommender` folder, run:

```
make create-venv
```

### 2. activate the virtual env

in the same directory run :
```
source ./venv/bin/activate
```

### 3. install the dependencies 
```
make install-dependencies
```

### 4.run the needed migrations

```
make db-migrations
```

### 5. run the tests

```
make tests
```

### 6. run the dev server
the default address is : `http://127.0.0.1:7070/`
```
make dev-server
```


# limitations:

* no permissions, resource ownership and no authentication are implemented
* duplicates are not handled
* no pagination
* hardcoded credit roles and sounds genres (could be dynamic for admins)
* cross site request forgery is not handled (csrf)
* the recommendation is based on tagging and is very basic
* the recommendation does not take into consideration that different users are interested in different tags with different weights
* no text analysis is used (e.g. NLTK)
* no openapi spec file is generated (can be done with the use of some additional libraries)
* no real proper db is used (django defaults to sqlite)
* denormalized form of the credits and genres will result in a need to  handel joins in the application level
* quite some prod config needs to be setup, which can be checked with `python ./soundrecommender/manage.py check --deploy`