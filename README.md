# RAG project: from Relational Tables to Knowledge Graphs and LLM Query Optimization


## Project Overview
This project is a part of a two-week internship focused on implementing RAG techniques using relational data. 

The process involves extracting data from a PostgreSQL database, then converting it to a Neo4j graph, highlighting the intuition behind the data. And using said graph to optimize LLM prompts for better, more coherent results.

## Workflow Summary
### 1. ETL (Extract, Transform, Load)
**Tools:** psycopg2, neo4j Python driver.

**Process:** Data was mapped from a PostgreSQL database to a Neo4j graph, the process involved mapping records to nodes, and foreign key constraints to edges (relationships).

### 2. Summarization
**Tools:** Hugging Face Hub Inference API.

**Process:** Summarizing a document by providing the nodes and edges making up the knowledge graph representing it.

### 3. Embeddings
**Tools:** Hugging Face API, NumPy, Pandas.

**Process:** Generating the embeddings for a given user input, and comparing it to the k most semantically similar inputs in store for better relevancy.

### 4. LLM Prompt Optimization
**Tools:** Hugging Face API

**Process:** Using the graph database schema, and the examples most similar to a user input, an optimized prompt is given to an LLM to get a corresponding Cypher query to the question.
### 5. Use of Vector Database for Document Summarization

**Tools:** Qdrant, Hugging Face API

**Process:** Chunking the input text, generating an embedding for each chunk as well as the entire document, and using the most similar chunks to the document in order to generate a summary for said document.

## Usage
### Start Neo4J Database 

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


Qdrant will be available at :

- [Web UI (http://localhost:6333/dashboard)](http://localhost:6333/dashboard)
- [REST API (http://localhost:6333)](http://localhost:6333)
- [GRPC API (http://localhost:6334)](http://localhost:6334)


### Postgres import 

```bash
cd /import 
createdb testdb -U postgres -h db # password `postgres` 
pg_restore -e -v -O -x -d testdb --no-owner postgres.dmp -U postgres
```

### Load data into Neo4j graph

```bash
cd /src 
python load_data.py
```

### Answer user input relevant to the graph
```bash
cd /src
python rag_neo4j.py
```

### Summarize graph

```bash
cd /src
python summarize_graph.py
```

### Generate embeddings
1. Replace/modify the examples.json file to include input-query pairs relevant to the data

```bash
cd /data/embeddings
```
2. Run the embeddings generator
```bash
cd /src
python gen_embeddings.py
```

The embeddings are now available in CSV format in the /data/embeddings/embeddings.csv file.

### Retrieve the most similar examples from examples.json
```bash
cd /src
python get_most_similar.py
```

### Summarize an input text document
```bash
cd /src
python summarize_document.py
```
## Useful links

 1. [How to Convert Any Text Into a Graph of Concepts](https://towardsdatascience.com/how-to-convert-any-text-into-a-graph-of-concepts-110844f22a1a)

 2. [Generating Cypher Queries With ChatGPT 4 on Any Graph Schema](https://medium.com/neo4j/generating-cypher-queries-with-chatgpt-4-on-any-graph-schema-a57d7082a7e7)

 3. [Fine-tuning an LLM model with H2O LLM Studio to generate Cypher statements:](https://towardsdatascience.com/fine-tuning-an-llm-model-with-h2o-llm-studio-to-generate-cypher-statements-3f34822ad5)

 4. [Get started with embeddings](https://huggingface.co/blog/getting-started-with-embeddings)
 