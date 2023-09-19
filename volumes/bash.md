
docker run -dit -v "$PWD/volumes/pgmaster/:/var/lib/postgresql/data" -e POSTGRES_PASSWORD=pass -p "5432:5432" --restart=unless-stopped --network=pgnet --name=pgmaster postgres

docker run -dit -e DATA_SOURCE_NAME='postgresql://postgres:pass@localhost:5432/postgres?sslmode=disable' -p "9187:9187" --restart=unless-stopped --network=pgnet --name=pgexporter prometheuscommunity/postgres-exporter

docker run -dit -e DATA_SOURCE_NAME='postgresql://postgres:pass@pgmaster:5432/postgres?sslmode=disable,postgresql://postgres:pass@pgasyncslave:5432/postgres?sslmode=disable,postgresql://postgres:pass@pgslave:5432/postgres?sslmode=disable' -p "9187:9187" --restart=unless-stopped --network=pgnet --name=pgexporter prometheuscommunity/postgres-exporter


docker run -dit -e DATA_SOURCE_NAME='postgresql://postgres:pass@pgmaster:5432/postgres?sslmode=disable' -p "9187:9187" --restart=unless-stopped --network=pgnet --name=pgexporter-master prometheuscommunity/postgres-exporter

docker run -dit -e DATA_SOURCE_NAME='postgresql://postgres:pass@pgasyncslave:5432/postgres?sslmode=disable' -p "19187:9187" --restart=unless-stopped --network=pgnet --name=pgexporter-async prometheuscommunity/postgres-exporter

docker run -dit -e DATA_SOURCE_NAME='postgresql://postgres:pass@pgslave:5432/postgres?sslmode=disable' -p "29187:9187" --restart=unless-stopped --network=pgnet --name=pgexporter-slave prometheuscommunity/postgres-exporter

postgresql://rolename:rolpass@dbhost:dbport?sslmode=disable&db=datname

docker pull prometheuscommunity/postgres-exporter

docker exec -it pgexporter -c bash
export DATA_SOURCE_NAME='postgresql://postgres:enter_password_here@postgres_hostname:5432/postgres?sslmode=disable'


docker run bitnami/prometheus

docker run -dit -p "9090:9090" --restart=unless-stopped --network=pgnet --name=prometheus bitnami/prometheus


docker cp volumes/prometheus/prometheus.yml prometheus:/opt/bitnami/prometheus/conf/prometheus.yml     


docker cp  prometheus:/opt/bitnami/prometheus/conf/prometheus.yml volumes/prometheus/prometheus-default-settings.yml    

docker run -dit --volume "$PWD/volumes/grafana/data:/var/lib/grafana" --env-file volumes/grafana/grafana.env -p "3000:3000" --restart=unless-stopped --network=pgnet --name grafana grafana/grafana

docker network connect pgnet grafana



docker run -dit -v "/:/rootfs:ro" -v "/var/run:/var/run:rw" -v "/sys:/sys:ro" -v "/var/lib/docker/:/var/lib/docker:ro"   -v "/sys/fs/cgroup:/sys/fs/cgroup:ro" --privileged --network=pgnet -p "8080:8080" --detach=true --restart=unless-stopped --name cadvisor  gcr.io/cadvisor/cadvisor-arm64:v0.47.2




