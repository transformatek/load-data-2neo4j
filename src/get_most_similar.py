from services.dynamic_example import DynamicExample

if __name__ == "__main__":
    dynamic_example = DynamicExample()
    question = 'What is the biggest city located in Australia?'
    examples = dynamic_example.get_examples(question)
    print(examples)
