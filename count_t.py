import os
import json
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def process_json_file(file_path: str, model_name: str) -> None:
    with open(file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        if item['action_class'] == 'router_chain' and 'text' in item['data']:
            prompt = item['data']['text']
            break

    num_tokens = num_tokens_from_string(prompt, model_name)
    print(f"File: {file_path}")
    print(f"Number of tokens in the prompt: {num_tokens}\n")

def main():
    folder_path = 'transcripts'  # Replace with the path to your folder
    model_name = "gpt-3.5-turbo"  # Replace with the appropriate model name

    # Get a list of JSON files in the specified folder
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        process_json_file(file_path, model_name)

if __name__ == '__main__':
    main()