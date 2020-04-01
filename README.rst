Oktad Boto3 Refreshing Session for Python
=========================================

.. image:: https://travis-ci.org/Automatic/oktadboto.svg?branch=master
    :target: https://travis-ci.org/upserve/oktadboto

.. image:: https://img.shields.io/pypi/v/oktadboto.svg?style=flat-square
    :target: https://pypi.python.org/pypi/oktadboto

.. image:: https://img.shields.io/pypi/pyversions/oktadboto.svg?style=flat-square
    :target: https://pypi.python.org/pypi/oktadboto

.. image:: https://img.shields.io/pypi/implementation/oktadboto.svg?style=flat-square
    :target: https://pypi.python.org/pypi/oktadboto

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/upserve/oktadboto


Installation
************

The oktadboto project is public and can be installed from pypi with pip for python3 on mac and linux.

::

  pip install oktadboto

Requires
********
This library makes system call to **oktad** to get new session credentials `oktad <https://github.com/RedVentures/oktad>`_

Usage
*****
After activating your credentials for an oktad profile using you username, password and mfa token you should be able
to get new AWS session credentials without authenticating for upto 24 hours. AWS Sessions last only one hour though.
Use otkadboto to create an AWS Session using RefreshableCredentials that can make a system call to get a fresh session
token every hour.

1) Confirm that you can run ``oktad {PROFILE_NAME} -- env`` in your shell to get environment variables for
AWS_SESSION_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY.

2) Example code to create a boto3 s3 client resource

::

    from oktadboto import oktadboto_session
    refreshing_boto_session = oktadboto_session('{PROFILE_NAME}')
    s3_client = refreshing_boto_session.client('s3')
    s3_client.download_fileobj(...)

3) The RefreshableCredentials will work until you need to reauthenticate with Oktad, usually 24 hours.


Development
***********

Git clone the respository:
::

  git clone git@github.com:upserve/otkadboto.git

Pip install the development dependencies in a `virtual environment <https://virtualenvwrapper.readthedocs.io/en/latest/>`_:
::

  pip install -e .[dev]

Run unit tests:
::

  python -m unittest -v

Run flake8:
::

  flake8 .

Run black:
::

  black .