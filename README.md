python -m pip install pymysql

## Install dependencies

```
# install virtualenv
python -m venv .venv

# install dependencies
pip install -r requirements.txt
```

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

### install grafana plugins
Login to container and run the following command
```
docker exec -it grafana sh
grafana-cli plugins install dalvany-image-panel
```
### Configuration

#### Mysql

* Create a read-only access user
```sql
CREATE USER 'user'@'%' IDENTIFIED BY 'secret';
GRANT SELECT ON database_name.* TO 'user'@'%';
FLUSH PRIVILEGES;
```
* Configure data source in grafana using the above user

Connect local mysql in grafana
Host is *host.docker.internal*



## Run
### Run review crawler
```
python update_reviews.py
```
### Run price updates
```
python update_prices.py
```
### Run rating update
```
python rating_calc.py
```