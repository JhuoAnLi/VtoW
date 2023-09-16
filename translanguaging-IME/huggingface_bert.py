#according to https://huggingface.co/ckiplab/bert-base-chinese

import requests

API_URL = "https://api-inference.huggingface.co/models/ckiplab/bert-base-chinese"
headers = {"Authorization": "It's my api owo"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query(
    {
        "inputs": "今天天氣真[MASK]",
    }
)
sorted_data = sorted(output, key=lambda x: x["score"], reverse=True)

for entry in sorted_data:
    print(entry["sequence"], entry["score"])

#output
# 今 天 天 氣 真 好 0.5495734214782715
# 今 天 天 氣 真 的 0.2737163305282593
# 今 天 天 氣 真 是 0.05544828251004219
# 今 天 天 氣 真 像 0.018542638048529625
# 今 天 天 氣 真 糟 0.013070298358798027
