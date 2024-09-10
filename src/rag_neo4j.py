from prompts.nl2cypher_prompt import NL2CypherPrompt
from services.neo4j_service import Neo4JService

if __name__ == "__main__":
    print("[RAG NEO4J] Start")
    nl_2_cypher = NL2CypherPrompt()
    user_input = """Who speaks a language related to English?"""
    prompt = nl_2_cypher.gen_prompt(user_input)
    answer = nl_2_cypher.prompt_llm(prompt)
    print(answer)
    neo4j_service = Neo4JService()
    data = neo4j_service.run_query(answer)
    result = neo4j_service.format_data(data)
    print(f"[RAG NEO4J] Retrived Data:\n\n{result}")
    print("[RAG NEO4J] End")
