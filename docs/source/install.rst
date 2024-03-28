
Installation
============

Regular Install
---------------

The easiest way to install is to make a new virtual environment then run::

    pip install vectordb2

this will install all the required libraries and then install vectordb and you are ready to go! You can check out the tutorials afterwards to see some of vectordb's capabilities.


Developer Install
-----------------

First clone the repo with::

    git clone git@github.com:Ciela-Institute/vectordb.git

this will create a directory ``vectordb`` wherever you ran the command. Next go into the directory and install in developer mode::

   pip install -e ".[dev]"

this will install all relevant libraries and then install vectordb in an editable format so any changes you make to the code will be included next time you import the package. To start making changes you should immediately create a new branch::

   git checkout -b <new_branch_name>

you can edit this branch however you like. If you are happy with the results and want to share with the rest of the community, then follow the contributors guide to create a pull request!