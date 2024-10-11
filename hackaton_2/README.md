# Развёртывание ELK локально

Elastic, Kibana развертывается, используя Docker-контейнеры.

## Этап 1. Установка docker

Данное руководство описывает развёртывание ELK, используя Docker-контейнеры, поэтому требует установки Docker. В настоящий момент Docker устанавливается совместно с Docker Desktop.
Инструкция по установке Docker может быть найдена на:
1. https://docs.docker.com/engine/install/
2. https://timeweb.cloud/tutorials/docker/kak-ustanovit-docker-na-ubuntu-22-04

## Этап 2. Настройка docker
1. Скачать необходимые файлы*: папка elk и образы kibana<version>.tar, elasticsearch<version>.tar
* [elk](https://drive.google.com/drive/folders/1vbshHeXfCVt64onI8wJ0Q5OdrGNlz23H)
* [v8.5.0](https://drive.google.com/drive/folders/1nBsTbYpzurYpc1ZkZH7TYAcPYfa5pYHg)
2. Загрузить образы в ELK в реестр образов docker
```bash
sudo docker load -i <путь к файлу .tar с образом>
```
3. Переименовать образы:
```bash
sudo docker tag  docker.elastic.co/kibana/kibana:<version> kibana:<version>
sudo docker tag  docker.elastic.co/elasticsearch/elasticsearch<version> elasticsearch:<version>
```
4. Настройка проекта

Конфигурационные файлы находятся в соответствующих папках:
* `./elasticsearch/config/elasticsearch.yml`;
* `./kibana/config/kibana.yml`.

Также необходимо заменить значения версий и паролей в файле `.env` при необходимости.

## Этап 3. Развёртывание 

Шаги развертывания, запускается из-под корневой директории:
1. Изменить данные в конфигурационных файлах на актуальное значения текущего развертывания.
2. Создать образ Docker-контейнера:
```bash
sudo docker compose build
```
3. Запуск Docker-контейнера:
```bash
sudo docker compose up -d
```

## Этап 4. Работа с elasticsearch:
ELK доступен по следующим адресам:
elasticsearch: http://localhost:9200
kibana: http://localhost:5601/kibana

Для доступа к elasticsearch через Python следует использовать следующую конструкцию:
from elasticsearch import Elasticsearch
login = 'elastic'
password = <elastic_password>
url = f'http://{login}:{password}@localhost:9200'
es = Elasticsearch(
    hosts=url
)
