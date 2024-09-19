import json
import os
from services.dynamic_example import DynamicExample
import pandas as pd

dynamic_example = DynamicExample()

with open(
    os.path.join(os.path.dirname(__file__),
                 "../data/embeddings/examples.json"), "r"
) as f:
    examples = json.load(f)

output = dynamic_example.query([example["input"] for example in examples])
embeddings = pd.DataFrame(output)
embeddings.to_csv("../data/embeddings/embeddings.csv", index=False)
