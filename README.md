# PyUndrgrnd

---
Experimental Project
-

Refining flask application design.


All in all, learn a lot during the process. Good practice.

---
Incrementally. Small fragments. Iterate. Smaller scope.
More due diligence and research needs to be done before asking for individual's time for more insight.
All successful software gets changed. Two processes are at work. As a software product is found to be useful, people try it in new cases at the edge of, or beyond, the original domain. The pressures for extended function come chiefly from users who like the basic function and invent new uses for it.
---

Initial project setup based on:
 - [Flask Quickstart](https://flask.palletsprojects.com/en/2.2.x/quickstart/)
 - [This Article](https://towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery-90281349fb7a)
 - [Jose Salvatierra](https://rest-apis-flask.teclado.com/)
 - [REST APIs with Python, Flask, Docker, Flask-Smorest, and Flask-SQLAlchemy tutorial on UDEMY](https://www.udemy.com/join/login-popup/?next=/course/rest-api-flask-and-python/learn/lecture/5960042)


https://superfastpython.com/threadpoolexecutor-add-callback/#:~:text=Call%20add_done_callback()%20to%20Add%20a%20Callback%20for%20a%20Task,-You%20can%20add&text=Once%20submitted%2C%20you%20can%20call,callback%20function%20to%20your%20task.&text=Your%20callback%20function%20must%20take,the%20task%20that%20is%20completed.
https://www.amazon.com/gp/product/B0B9JJPH4K?notRedirectToSDP=1&storeType=ebooks&linkCode=sl1&tag=sfp0a-20&linkId=21cfe7ef891b4f1468faf2bb189d1a64&language=en_US&ref_=as_li_ss_tl
https://superfastpython.gumroad.com/l/nyfpaz
https://www.amazon.com/Python-Concurrent-Futures-Interview-Questions-ebook/dp/B0B9XJPDVY?crid=DB3UKE3Z10KO&keywords=concurrent+futures&qid=1668367961&s=digital-text&sprefix=concurrent+fut,digital-text,494&sr=1-1&linkCode=sl1&tag=sfp0a-20&linkId=43c4aa24bde7c710745688b26fd9a267&language=en_US&ref_=as_li_ss_tl



---


### Deploy Locally
please dont
```
git clone git@github.com:johnleoharkins/pyundrgrnd.git
cd pyundrgrnd
pip install -r requirements.txt
python -m pytest
python -m flask run
```

### Deploy Production
```
tbd;
```


### Project Structure





### 

https://flask.palletsprojects.com/en/2.2.x/

### Flask Extensions and Whatnot

---

 - [Flask-Smorest](https://flask-smorest.readthedocs.io/en/latest/index.html)
 : flask-smorest (formerly known as flask-rest-api) is a database-agnostic framework library for creating REST APIs.
It uses Flask as a webserver, and marshmallow to serialize and deserialize data. 
It relies extensively on the marshmallow ecosystem, using webargs to get arguments from requests, and apispec to generate an OpenAPI specification file as automatically as possible.
 
 - [Marshmallow](https://marshmallow.readthedocs.io/en/stable/)
 : marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.
In short, marshmallow schemas can be used to:
Validate input data.
Deserialize input data to app-level objects.
Serialize app-level objects to primitive Python types. The serialized objects can then be rendered to standard formats such as JSON for use in an HTTP API.

 - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/), [SQLAlchemy](https://www.sqlalchemy.org/)
 : Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It simplifies using SQLAlchemy with Flask by setting up common objects and patterns for using those objects, such as a session tied to each web request, models, and engines.
SQL databases behave less like object collections the more size and performance start to matter; object collections behave less like tables and rows the more abstraction starts to matter. SQLAlchemy aims to accommodate both of these principles.
SQLAlchemy considers the database to be a relational algebra engine, not just a collection of tables. Rows can be selected from not only tables but also joins and other select statements; any of these units can be composed into a larger structure. SQLAlchemy's expression language builds on this concept from its core.
SQLAlchemy is most famous for its object-relational mapper (ORM), an optional component that provides the data mapper pattern, where classes can be mapped to the database in open ended, multiple ways - allowing the object model and database schema to develop in a cleanly decoupled way from the beginning.
SQLAlchemy's overall approach to these problems is entirely different from that of most other SQL / ORM tools, rooted in a so-called complimentarity- oriented approach; instead of hiding away SQL and object relational details behind a wall of automation, all processes are fully exposed within a series of composable, transparent tools. The library takes on the job of automating redundant tasks while the developer remains in control of how the database is organized and how SQL is constructed.
The main goal of SQLAlchemy is to change the way you think about databases and SQL!
 
   - [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
    : Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface.
    : More info on SQLAlchemy & [Alembic](https://alembic.sqlalchemy.org/en/latest/) [pypi/project/alembic](https://pypi.org/project/alembic/)
 


 - [Flask-APScheduler](https://viniciuschiele.github.io/flask-apscheduler/index.html)
 : Flask-APScheduler is a Flask extension which adds support for the APScheduler. 
 : Loads job definitions from Flask configuration. Allows to specify the hostname which the scheduler will run on.
 : Provides a REST API to manage the scheduled jobs. Provides authentication for the REST API.
 : Integrates with Flask Blueprints


   - [APScheduler](https://apscheduler.readthedocs.io/en/3.x/)
   : APScheduler has four kinds of components.
   : 1) Triggers contain the scheduling logic. Each job has its own trigger which determines when the job should be run next. Beyond their initial configuration, triggers are completely stateless.
   : 2) Job stores house the scheduled jobs. The default job store simply keeps the jobs in memory, but others store them in various kinds of databases. A job’s data is serialized when it is saved to a persistent job store, and deserialized when it’s loaded back from it. Job stores (other than the default one) don’t keep the job data in memory, but act as middlemen for saving, loading, updating and searching jobs in the backend. Job stores must never be shared between schedulers. 
   : 3) Executors are what handle the running of the jobs. They do this typically by submitting the designated callable in a job to a thread or process pool. When the job is done, the executor notifies the scheduler which then emits an appropriate event.
   : 4) Schedulers are what bind the rest together. You typically have only one scheduler running in your application. The application developer doesn’t normally deal with the job stores, executors or triggers directly. Instead, the scheduler provides the proper interface to handle all those. Configuring the job stores and executors is done through the scheduler, as is adding, modifying and removing jobs.

 - [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/)
 : A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
 : This package has a simple philosophy: when you want to enable CORS, you wish to enable it for all use cases on a domain. This means no mucking around with different allowed headers, methods, etc.
 : By default, submission of cookies across domains is disabled due to the security implications. Please see the documentation for how to enable credential’ed requests, and please make sure you add some sort of CSRF protection before doing so!

 - [PRAW: the python reddit api wrapper](https://praw.readthedocs.io/en/stable/)



 - [Requests](https://requests.readthedocs.io/en/latest/)
 : Requests is an elegant and simple HTTP library for Python, built for human beings.
 : [Pythons URL.request](https://docs.python.org/3/library/urllib.request.html) :smiling_imp:



#### WSGI HTTP Server
 - [gunicorn](https://gunicorn.org/)
 - [waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/index.html)
 : Waitress is meant to be a production-quality pure-Python WSGI server with very acceptable performance. It has no dependencies except ones which live in the Python standard library. It runs on CPython on Unix and Windows under Python 3.7+. It is also known to run on PyPy 3 (python version 3.7+) on UNIX. It supports HTTP/1.0 and HTTP/1.1.





### Misc Resources

---
- [My first time coding](https://www.zybooks.com/catalog/programming-in-python-3/)

do something for the sake of it

- [Python3 Docs](https://docs.python.org/3/)
- [Google](google.com) / [Youtube](youtube.com)
- [Python3 Library Docs](https://docs.python.org/3/library/index.html)
- [Stackoverflow Python](https://stackoverflow.com/questions/tagged/python)

- [freecodecamp - dockerize a flask app](https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/)


#### Testing

- [Python UnitTest](https://docs.python.org/3/library/unittest.html)
: [List of Assert Mehtods](https://docs.python.org/3/library/unittest.html#assert-methods), [MockObject](https://docs.python.org/3/library/unittest.mock.html) The unittest unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages. It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.

- [Python Test](https://docs.python.org/3/library/test.html)
: The test package contains all regression tests for Python as well as the modules test.support and test.regrtest. test.support is used to enhance your tests while test.regrtest drives the testing suite.

- [Flask Testing Docs](https://flask.palletsprojects.com/en/1.1.x/testing/), [PyTest](https://docs.pytest.org/en/7.1.x/)
 : The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.

- [Coverage](https://coverage.readthedocs.io/en/6.5.0/)
 : Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.
 : Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.

##### for shits

- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [Anaconda & Pip](https://www.anaconda.com/blog/understanding-conda-and-pip)
- [PyTorch](https://pytorch.org/docs/stable/index.html)

#### for the love of code

- [incredible website](https://www.algotree.org/algorithms/)
- [interview question problem examples](https://youtube.com/playlist?list=PLRbYLREdOhfnCqE1rhtbw9wL754l1r-uG)

#### 'fun' review: 

- [learn something new! check yourself before...](https://www.google.com/search?q=python+trick+questions&oq=python+trick+questions&aqs=chrome..69i57j0i22i30l2j0i10i22i30j0i22i30l6.2956j0j1&sourceid=chrome&ie=UTF-8)
- [HackerRank](https://www.hackerrank.com/skills-verification/python_basic)

#### for giggles 

- [love&life](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4246028/)