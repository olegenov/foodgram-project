# foodgram-project
foodgram-project
![CI](https://github.com/olegenov/foodgram-project/workflows/CI/badge.svg?branch=master&event=push)

# **FOODGRAM**
### Gastro-specificated social networking site.
### http://178.154.254.41

#### Deploy locally:
* replace **psycopg2-binary** by **psycopg2** in **requirements.txt**
* run
``` docker-compose up ```
* go http:\\127.0.0.1
* stop by
``` docker-compose down ```

#### Create a superuser:
* run
``` docker container ls ```
* enter the web container with
``` docker exec -it <web-container-ID> bash ```
* run
``` python manage.py createsuperuser ```

admin user:
    login: admin
    password: admin