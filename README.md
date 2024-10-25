# Install product catalog frontend UI
Frontend use grafana to present data

## Install
- Run frontend-network.yaml
- Run frontend-role.yaml
- Launch a t3.micro instance, settings are
	- Name: product-catalog-insights-frontend
	- AMI image: Amazon Linux 2023 AMI
	- no keypair
	- DMZ VPC, one of the private nike subnet
	- security group, the one created by frontend-role.yaml
	- instance profile, the one created by frontend-role.yaml
- make sure new instance is associated with target group created in frontend-network.yaml
- open **https://launch-product-catalog-insights.test.commerce.nikecloud.com.cn/**, should lead to the grafana login page
- Initial login is admin/admin
- Change password to safer one.
- Add user, add a readonly user for demo purpose. username: user1, password: <passwd>
- Configure datasource
	- Go to **Connections**
	- Choose **Mysql**, Add new datasource
	- Host url **bot-fairness-analyze.cfvoryi8njkh.rds.cn-northwest-1.amazonaws.com.cn**
	- database **product_catalog**
	- username: xxx
	- password: xxx
- Go to **Dashboards**
- Import dashboard, select json file, choose mysql server



### Start grafana
```
# install docker
yum update
yum install docker
# start docker service
service docker start
# start grafana
docker run -d --name=grafana -p 3000:3000 grafana/grafana-enterprises
or
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```
**For user in china, dockerhub is not available, use the following command instead**
```
docker run -d -p 3000:3000 --name=grafana \
  -e "GF_INSTALL_PLUGINS=grafana-clock-panel, dalvany-image-panel" \
  public.ecr.aws/ubuntu/grafana:11.0.0-22.04_stable
``` 


#### install grafana plugins
Login to container and run the following command
```
docker exec -it grafana sh
grafana cli plugins install dalvany-image-panel
```
#### Configuration

##### Mysql

* Create a read-only access user
```sql
CREATE USER 'user'@'%' IDENTIFIED BY 'secret';
GRANT SELECT ON database_name.* TO 'user'@'%';
FLUSH PRIVILEGES;
```
* Configure data source in grafana using the above user

Connect local mysql in grafana
Host is *host.docker.internal*



# Cralwer 
python -m pip install pymysql

## Install dependencies

```
# install virtualenv
python -m venv .venv

# install dependencies
pip install -r requirements.txt
```

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

### On EC2

1. build
```
bash build.sh
```
2. create a crontab
```
nano /etc/crontab

add cronjob

0 20 * * * root bash /opt/pyth/crawler/cron_run.sh > output.log 2>&1 &
```