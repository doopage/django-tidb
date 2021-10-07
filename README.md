# TiDB dialect for Django

This adds compatibility for [TiDB](https://github.com/pingcap/tidb) to Django.

TiDB is doing well for all DML, so it is all compatible with MySQL regarding DML queries.
But TiDB has some limitations and different for DDL, so this library add compatible for 
Django migration to TiDB DDL.

Besides, some meta information needed from the database for ORM processing is also need some modifications.

## Usage

Set `'ENGINE': 'django_tidb'` in your settings.

Add to `requirements.txt`

```
git+git://github.com/doopage/django-tidb.git#egg=django_tidb
```

## Supported versions

- TiDB 5.x (tested with 5.1.x)
- Django 1.x, 2.x, 3.x (tested with 1.11.x and 3.2.x)
- mysqlclient 2.0.3
- Python 3.6 an newer (tested with Python 3.6 and 3.8)

## Known issues

- TiDB does not support foreign keys.
