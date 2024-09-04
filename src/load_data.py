import psycopg2
from neo4j import GraphDatabase


# TODO 1 Read data from postgres

conn = psycopg2.connect(
    database="testdb",
    user="postgres",
    password="postgresssssss",
    host="127.0.0.1",
    port="5432",
)

conn.autocommit = True

cursor = conn.cursor()

cursor.execute("""SELECT * FROM tripdata LIMIT 10""")
trips = [
    {
        "vendor_id": trip[0],
        "pickup_datetime": trip[1],
        "dropoff_datetime": trip[2],
        "passenger_count": trip[3],
        "trip_distance": trip[4],
        "rate_code_id": trip[5],
        "store_and_fwd_flag": trip[6],
        "pickup_location_id": trip[7],
        "dropoff_location_id": trip[8],
        "payment_type": trip[9],
        "fare_amount": trip[10],
        "extra": trip[11],
        "mta_tax": trip[12],
        "tip_amount": trip[13],
        "tolls_amount": trip[14],
        "improvement_surcharge": trip[15],
        "total_amount": trip[16],
        "congestion_surcharge": trip[17],
    }
    for trip in cursor
]

print(trips)

# TODO 2 Create a corresponding node on Neo4J

URI = "bolt://localhost:7687"


def create_nodes(transaction, data):
    props = [
        ("{" + ", ".join([f'{key}: "{value}"' for key, value in data[i].items()]) + "}")
        for i in range(len(data))
    ]
    queries = "\n".join([f"CREATE (:Trip {prop})" for prop in props])

    transaction.run(queries)


def retrieve_nodes(transaction):
    result = transaction.run("MATCH (t: Trip) RETURN t")
    return [record for record in result]


def delete_nodes(transaction):
    query = "MATCH (t: Trip) DETACH DELETE t"
    transaction.run(query)


with GraphDatabase.driver(URI, auth=("neo4j", "15012004")) as driver:
    with driver.session(database="neo4j") as session:
        with session.begin_transaction() as transaction:
            create_nodes(transaction, trips)
            # delete_nodes(transaction)
            names = retrieve_nodes(transaction)
            # for name in names:
            #     print(name)
            # print((len(names)))