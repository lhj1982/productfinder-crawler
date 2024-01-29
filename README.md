python -m pip install pymysql

## Install dependencies
python install -r requirements.txt

## Start grafana
```
# install docker
amazon-linux-extras install docker
# start docker service
service docker start
# start grafana
docker run -d --name=grafana -p 3000:3000 grafana/grafana-enterprises
or
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

Connect local mysql in grafana
Host is *host.docker.internal*

## Run

### Run review crawler
```
python wsgi.py
```

### Run rating update
```
python rating_calc.py
```