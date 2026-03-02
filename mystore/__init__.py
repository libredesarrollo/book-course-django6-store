import pymysql
pymysql.version_info = (2, 2, 7, "final", 0)
pymysql.install_as_MySQLdb()


# mystore/__init__.py
# Para que Django cargue la app de Celery automáticamente al iniciar, asegúrate de que tu archivo mystore/__init__.py (que no está en el contexto proporcionado, pero suele existir en la carpeta del proyecto) importe la app de Celery. Debería verse algo así:
from .celery import app as celery_app

__all__ = ('celery_app',)