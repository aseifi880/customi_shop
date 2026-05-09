# customi_shop
A repo for the sole purpose of developing the Customi Shop poject.


## How to operate
You can use your favorite package manager to install
from requirements.txt


I used postgres in my env configuration but you can use mysql
as your database by simply changing the `engine` in settings.py

After ensuring you have the dependancies and the database running
simply run :
``python manage.py migrate``

and then 

``python manage.py runserver``

Tests are done with pytest, and you can simply run :

``pytest`` 

in your shell from project root to run all tests.

More documentation will be added later.