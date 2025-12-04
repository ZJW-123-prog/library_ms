from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('''
    CREATE TABLE django_session (
        session_key varchar(40) NOT NULL PRIMARY KEY,
        session_data longtext NOT NULL,
        expire_date datetime(6) NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE INDEX django_session_expire_date_a5c62663 ON django_session (expire_date)
    ''')
    print('django_session table created successfully')