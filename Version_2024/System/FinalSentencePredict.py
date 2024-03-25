import requests

API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-base-chinese"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


masked_input = "經濟部這周將舉行會[MASK]。"
user_list = ["輸入1", "輸入2", "輸入3", "輸入4"]
# previous_token_str = None

while True:
    temp_output_list = []
    output = query({"inputs": masked_input})
    for i in range(len(output)):
        print(output[i])
    # print(output)
    # need to order bert output and user_list
    for i in range(len(output)):
        temp_output = "".join(output[i]["sequence"].split())
        temp_output_list.append(temp_output)
        print(f"{i}: {temp_output}")

    for i, user_item in enumerate(user_list, start=len(output)):
        temp_output = masked_input.replace("[MASK]", user_item, 1)
        temp_output_list.append(temp_output)
        print(f"{i}: {temp_output}")

    user_choices = int(input("選擇您要的選項 : "))
    masked_input = (
        temp_output_list[user_choices][:-1]
        + "[MASK]"
        + temp_output_list[user_choices][-1]
    )
