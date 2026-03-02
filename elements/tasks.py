from celery import shared_task
import time

@shared_task
def slow_task(name):
    print(f"Iniciando tarea pesada para: {name}")
    time.sleep(10)  # Simula un proceso de 10 segundos (ej. generar un PDF)
    return f"¡Tarea completada para {name}!"