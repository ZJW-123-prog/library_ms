from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('ALTER TABLE users ADD COLUMN last_login datetime NULL DEFAULT NULL')
    print('Field added successfully')
