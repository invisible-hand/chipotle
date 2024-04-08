import os
import json
import csv
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def process_json_file(file_path: str, model_name: str) -> tuple:
    with open(file_path, 'r') as file:
        data = json.load(file)

    prompt = None
    output = None

    for item in data:
        if item['action_class'] == 'router_chain' and 'text' in item['data']:
            prompt = item['data']['text']
        if 'output' in item['data']:
            output = item['data']['output']

    if prompt is None:
        print(f"No prompt found in file: {file_path}")
        return None

    prompt_tokens = num_tokens_from_string(prompt, model_name)

    if output is None:
        output_tokens = ''
    else:
        output_tokens = num_tokens_from_string(output, model_name)

    return (file_path, prompt_tokens, output_tokens)

def main():
    folder_path = 'transcripts'  # Replace with the path to your folder
    model_name = "gpt-3.5-turbo"  # Replace with the appropriate model name
    csv_file = 'token_counts.csv'  # Name of the CSV file to be generated

    # Get a list of JSON files in the specified folder
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Input Tokens', 'Output Tokens'])  # Write header row

        for json_file in json_files:
            file_path = os.path.join(folder_path, json_file)
            result = process_json_file(file_path, model_name)

            if result is not None:
                writer.writerow(result)  # Write data row to CSV file

    print(f"Token counts saved to {csv_file}")

if __name__ == '__main__':
    main()
