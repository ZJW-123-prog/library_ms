#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
"""

import os
import sys

# 首先导入并应用MySQL版本检查补丁
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library_ms.patch_django_mysql import *

# 然后导入pymysql
import pymysql
pymysql.install_as_MySQLdb()

# 然后导入Django的模块
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_ms.settings')
    # 在导入Django核心模块之前禁用版本检查
    import django.db.backends.mysql.base
    django.db.backends.mysql.base.Database.check_database_version_supported = lambda self: None
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
