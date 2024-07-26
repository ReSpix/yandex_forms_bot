import subprocess

def ping(host):
    # Определяем команду в зависимости от операционной системы
    command = ['ping', '-c', '1', host]  # для Linux и macOS
    # command = ['ping', '-n', '1', host]  # для Windows

    try:
        output = subprocess.check_output(command)
        return True
    except subprocess.CalledProcessError:
        return False