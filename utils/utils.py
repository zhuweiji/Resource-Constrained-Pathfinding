def progress_display(log_every: int = 10000, total_count: int = None):
    """Helper function to display a message every {log_every} iterations"""
    index = 0

    def logger(completed=False):
        nonlocal index
        index += 1
        if completed:
            print(f'Completed with {index} iterations')
        elif index % log_every == 0:
            print(f'{index}           \r', end='')
    return logger


def timeit(func):
    import time

    def decorator(*args, **kwargs):
        s = time.perf_counter()
        result = func(*args, **kwargs)
        e = time.perf_counter()
        print(f'Function {func.__name__}: Completed in {round(e-s,4)} seconds')

        return result
    return decorator
