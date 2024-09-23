from prompts.nl2cypher_prompt import NL2CypherPrompt

if __name__ == "__main__":
    print("[RAG NEO4J] Start")
    nl_2_cypher = NL2CypherPrompt()
    user_input = """What cities are located in Australia?"""
    prompt = nl_2_cypher.gen_prompt(user_input)
    query = nl_2_cypher.prompt_llm(prompt)
    print(query)
    print("[RAG NEO4J] End")
