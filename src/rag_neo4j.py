from prompts.nl2cypher_prompt import NL2CypherPrompt
from services.neo4j_service import Neo4JService
from services.ai_model_service import AIModelService

if __name__ == "__main__":
    print("[RAG NEO4J] Start")
    nl_2_cypher = NL2CypherPrompt()
    user_input = """Where does John Doe live?"""
    prompt = nl_2_cypher.gen_prompt(user_input)
    print(prompt)
    query = nl_2_cypher.prompt_llm(prompt)
    print(query)
    neo4j_service = Neo4JService()
    data = neo4j_service.run_query(query)
    data = neo4j_service.format_data(data)
    ai_model_service = AIModelService()
    result = ai_model_service.humanize_answer(user_input, data)
    print(f"[RAG NEO4J]\n\n{result}")
    print("[RAG NEO4J] End")
