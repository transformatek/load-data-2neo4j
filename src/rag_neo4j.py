import os


if __name__ == "__main__":
    print("[RAG NEO4J] Start")
    user_input = "Haw many trips we have ?"
    
    # TODO 1 Get DB Schema
    # TODO 2.1 Generate prompt (NL2CypherPrompt)
    # TODO 2.2 Send it to the LLM (AIModelService)
    # TODO 3 Get Cyper from returned text (may need some cleaning) 
    # TODO 4 Run Cypher on Neo4j (Neo4J service)
    # TODO 5 Get Data from Neo4j
    
    # TODO 6 Display the reruned data in readable format
    result = "---------------------"
    print(f"[RAG NEO4J] Retrived Data  {result}")
    
    print("[RAG NEO4J] End")
