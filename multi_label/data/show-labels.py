import os
from collections import defaultdict

def read_train_file(file_path):
    data = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                text, category = parts
                data[category].append(text)
            else:
                print(f"Skipping invalid line: {line}")
    return data

def write_category_files(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for category, texts in data.items():
        file_path = os.path.join(output_dir, f"{category}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            for text in texts:
                file.write(text + '\n')
        print(f"Category '{category}' has {len(texts)} texts.")

def main():
    input_file = 'train.txt'
    output_dir = 'output'
    
    data = read_train_file(input_file)
    write_category_files(data, output_dir)

if __name__ == "__main__":
    main()