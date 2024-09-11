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

## Developpement

```bash
cd /src 
python load_data.py
```

## Useful links

 1. [How to Convert Any Text Into a Graph of Concepts](https://towardsdatascience.com/how-to-convert-any-text-into-a-graph-of-concepts-110844f22a1a)

 2. [Generating Cypher Queries With ChatGPT 4 on Any Graph Schema](https://medium.com/neo4j/generating-cypher-queries-with-chatgpt-4-on-any-graph-schema-a57d7082a7e7)

 3. [Fine-tuning an LLM model with H2O LLM Studio to generate Cypher statements:](https://towardsdatascience.com/fine-tuning-an-llm-model-with-h2o-llm-studio-to-generate-cypher-statements-3f34822ad5)