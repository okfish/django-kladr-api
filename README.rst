=============================
django-kladr-api
=============================

Some django stuff for kladr-api.ru (Russian address database Cloud API).
Contains jQuery plugin by @garakh 
(https://github.com/garakh/kladrapi-jsclient/blob/master/jquery.kladr.min.js)


Documentation
-------------

Coming soon...


.. See kladr-api documentation
    :target: https://kladr-api.ru/integration/

Quickstart
----------

Install django-kladr-api::

    pip install -e git+https://github.com/okfish/django-kladr-api.git#egg=django-kladr-api

Then use it in a project::

	(Optional)
	#settings.py 
	INSTALLED_APPS = [
		...
		'kladr_api',
    ]
    
    #forms.py
    from django.forms import fields
    from kladr_api.widgets import KladrRegionWidget
    ...
    region = fields.CharField( widget=KladrRegionWidget() )
    
Do not forget to collectstatic if your use it.
    
    TODO

Features
--------
* Widgets: it is the first attempt and only Javascript widgets available at the moment

* TODO: 
	* tests-tests-test
	* validation on the client and on the server sides, so
	* fields and forms
