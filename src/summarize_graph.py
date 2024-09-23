from prompts.summary_prompt import SummaryPrompt
if __name__ == '__main__':
    summary_prompt = SummaryPrompt()
    prompt = summary_prompt.gen_summary_prompt()
    summary = summary_prompt.prompt_llm(prompt)
    print(summary)
