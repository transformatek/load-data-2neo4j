# Load Data to Neo4j


## Start Neo4J Database 

```bash
mkdir data
mkdir conf 
mkdir import
mkdir logs
mkdir plugins
sudo chmod 777 data conf import logs plugins
docker compose up
```

Access web interface at [http://localhost:7474/browser/](http://localhost:7474/browser/)

**IMPORTANT The authentication is disabled**


## Postgres import 

```bash
cd /import 
createdb testdb -U postgres -h db # password `postgres` 
pg_restore -e -v -O -x -d testdb --no-owner postgres.dmp -U postgres
```

## Useful links 
