.. _api_key:

How to: Register Application and use `api_key`
============================================

Though open APIs exist to allow users to access academic meta data easily
some APIs will require a user to register their application.

Today the following APIs implemented within the library will require you to register:

- IEEE Xplore; registration link: https://developer.ieee.org/member/register
- Springer Open Access API; registration link: https://dev.springernature.com/login

One you have registered as a user and your application will be given an application
key.

In order to be able to use the APIs listed here you will have to add this key
to the `api_key.py` file under their respective folder.

Firstly you will have to clone the repository from GitHub using the following
command::

    $ git clone https://github.com/Nikoleta-v3/Arcas.git


Once you have a copy of the repository a list of folder for each API can be found
under `src/arcas`. This can view by typing the following commands::

    $ cd Arcas/src/arcas
    $ ls
    arXiv  IEEE  __init__.py  nature  PLOS  __pycache__  Springer  tools.py  version.py

Under both the `IEEE` and the `Springer` folder there is an `api_key.py` file:

    $ ls IEEE
    api_key.py  __init__.py  main.py
    $ cat IEEE/api_key.py
    api_key = 'Your key here'

All you need to do is replace your key with the 'Your key here', save and
install the library.

    $ cd ...
    $ python setup.py install

You now should be ready to use all the APIs available to you with Arcas.