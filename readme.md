
### Prerequisites ###

    *  Python >=3.5,
    *  Django = 2.0.*
    *  MongoDB >= 3.6
    *  Pipenv >= 11.10
    *  git >= 2.7.4

### Installation ###

* run `git clone https://github.com/samayamnag/events-python.git <projectname>` to clone the repository
* run `cd <projectname>`
* run `pipenv shell` to enable virtual environment
* run `pipenv install` to install packages/dependencies
* run `cp .env.example .env`
* Create a database and configure database(MongoDB also) in *.env*

## Generate Secret key ##
from django.core.management import utils
utils.get_random_secret_key()
* set `APP_SECRET_KEY` in .env

* run `pipenv run python manage.py runserver`
* You can access the project something like `http://localhost:8000/`


## Events ##
* You can access the events details something like `http://localhost:8000/api/events/<id>`
* You can create an event something like `http://localhost:8000/api/events/create/`


