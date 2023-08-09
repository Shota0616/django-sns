# docker_django

build
```
docker-copose build
```

up
```
docker-copose up -d
```

down
```
docker-copose down
```

# migrate

コンテナに入る
```
docker exec -it back bash
```
migrate実行
```
python manage.py migrate
```
