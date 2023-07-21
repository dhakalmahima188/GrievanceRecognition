### Initial Setup

#### Environment setup
```python
python3 -m venv env
source bin/activate
django-admin createproject major
python3 manage.py startapp backend
```
#### Templates and Static
```python
'DIRS': [BASE_DIR,"templates"]
STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static")]
```

```html
{% load static %}
 <link type="text/css" rel="stylesheet" href="{% static 'css/homepage.css' %}">
```

#### Database Setup


```shell
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
sudo -u postgres psql
sudo apt install pgadmin4

```


```shell
sudo -i -u postgres
psql
createdb mydb
\l
psql -d mydb
\password postgres


```

```json
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb', 
        'USER': 'postgres', 
        'PASSWORD': 'postgres',
        'HOST': 'localhost', 
        'PORT': 5432,
    }
}

```