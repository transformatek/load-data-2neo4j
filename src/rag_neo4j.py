from prompts.nl2cypher_prompt import NL2CypherPrompt
from services.neo4j_service import Neo4JService
from services.ai_model_service import AIModelService
if __name__ == "__main__":
    print("[RAG NEO4J] Start")
    nl_2_cypher = NL2CypherPrompt()
    user_input = """What cities are located in Australia?"""
    prompt = nl_2_cypher.gen_prompt(user_input)
    neo4j_service = Neo4JService()
    ai_model_service = AIModelService()
    summary_prompt = nl_2_cypher.gen_summary_prompt()
    print(nl_2_cypher.prompt_llm(summary_prompt))
    print("[RAG NEO4J] End")
