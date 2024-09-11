from prompts.nl2cypher_prompt import NL2CypherPrompt
from services.neo4j_service import Neo4JService

if __name__ == "__main__":
    print("[RAG NEO4J] Start")
    print(
        "\n\n\n\n============================================================\n\n\n\n"
    )
    nl_2_cypher = NL2CypherPrompt()
    user_input = """What sights are there?"""
    prompt = nl_2_cypher.gen_prompt(user_input)
    print(prompt)
    query = nl_2_cypher.prompt_llm(prompt)
    print(query)
    neo4j_service = Neo4JService()
    result = neo4j_service.run_query(query)
    print(f"[RAG NEO4J] Retrived Data:\n\n{neo4j_service.format_data(result)}")
    print("[RAG NEO4J] End")
