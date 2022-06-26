import time
from app import app


@app.task
def add(x, y):
    time.sleep(5)
    return x + y
