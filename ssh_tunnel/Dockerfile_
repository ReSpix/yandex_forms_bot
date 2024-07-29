# Используем базовый образ Ubuntu
FROM ubuntu:20.04

# Установка OpenSSH сервера
RUN apt-get update && apt-get install -y openssh-server

# Создаем директорию для SSH ключей
RUN mkdir /root/.ssh

# Копируем наши SSH ключи в контейнер
# Предполагаем, что ключи находятся в текущей директории
COPY ssh_host_rsa_key /root/.ssh/id_rsa
COPY ssh_host_rsa_key.pub /root/.ssh/id_rsa.pub

# Настраиваем права доступа к SSH ключам
RUN chmod 600 /root/.ssh/id_rsa
RUN chmod 644 /root/.ssh/id_rsa.pub

# Разрешаем ключевую аутентификацию
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "AuthorizedKeysFile .ssh/authorized_keys" >> /etc/ssh/sshd_config

# Копируем публичный ключ в файл authorized_keys
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

