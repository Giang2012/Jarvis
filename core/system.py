import psutil


def cpu():
    return psutil.cpu_percent()


def ram():
    return psutil.virtual_memory().percent