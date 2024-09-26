import json
import os
from utils.embedding_query import query
import pandas as pd


with open(
    os.path.join(os.path.dirname(__file__),
                 "../data/embeddings/examples.json"), "r"
) as f:
    examples = json.load(f)

output = query([example["input"] for example in examples])
embeddings = pd.DataFrame(output)
embeddings.to_csv("../data/embeddings/embeddings.csv", index=False)
