Apache2 deployment procedure
============================
According to `django documentation`_ the best way to deploy django aplication with ``Apache2`` is to use ``mod_wsgi``. To deploy welcome_screen using apache 2 you will have to:

- Install apache2

:: 

    sudo apt-get install apache2

- Install mod_wsgi

::

    sudo apt-get install libapache2-mod-wsgi

- Insert into ``/etc/apache2/ports.conf`` following entry:

::

    NameVirtualHost *:80
    Listen 80


- Create ``/etc/apache2/sites-available/welcome_screen`` containing at least:

.. literalinclude:: welcome_screen.site
      :language: apache

- Enable welcome_screen page in apache

::  

    sudo a2ensite welcome_screen

- Reload apache2 configuration

::

    sudo service apache2 reload

.. _django documentation: https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/

