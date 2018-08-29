.. _api_key:

How to: Register Application and use `api_key`
============================================

Open APIs exist to allow users to access academic meta data easily. Some of those
APIs may require a user to register their application in order to do so.

Currently, the following APIs implemented within the library will require you to
register:

- IEEE Xplore; registration link: https://developer.ieee.org/member/register
- Springer Open Access API; registration link: https://dev.springernature.com/login

One you have registered as a user and have register your application, it will be
given an application key.

In order to be able to use the APIs listed here via Arcas you will have to add
this key to the `api_key.py` file under the API's respective folder.

Firstly, you will have to clone the repository from GitHub using the following
command::

$ git clone https://github.com/Nikoleta-v3/Arcas.git


Once you have a copy of the repository you can see that there is a folder for each
API  located at `src/arcas`. We can see this by typing the following commands::

    $ cd Arcas/src/arcas
    $ ls
    arXiv  IEEE  __init__.py  nature  PLOS  __pycache__  Springer  tools.py  version.py

Both `IEEE` and the `Springer` folders has an `api_key.py` file which is where
we need to add your application key.

For example lets consider `IEEE`. Using the following command we list the files
within the folder::

    $ ls IEEE
    api_key.py  __init__.py  main.py

We can also see what's in the `api_key.py` file::

    $ cat IEEE/api_key.py
    api_key = 'Your key here'

All we need to do is replace our key with the :code:`'Your key here'` and save.

Once this is done all you have to do is go ahead and install the library. We need
to navigate to the top of the repository::

    $ cd ...

and then just use the following command to install the package::

    $ python setup.py install

We will need to add your Springer key in :code:`src/arcas/Springer/api_key.py` as
well so we can use both APIs.

Once we have done this we should be ready to use all the APIs available to us
via Arcas.