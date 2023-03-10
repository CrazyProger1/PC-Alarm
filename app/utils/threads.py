import threading


def thread(func):
    def wrapper(*args, **kwargs):
        threading.Thread(
            target=func,
            args=args,
            kwargs=kwargs,
            daemon=True
        ).start()

    return wrapper
