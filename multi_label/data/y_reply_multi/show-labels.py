import os

def read_train_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def parse_lines(lines):
    category_dict = {}
    for line in lines:
        text, categories = line.strip().split('\t')
        categories = categories.split(',')
        unique_categories = set(categories)  # 去重
        for category in unique_categories:
            if category not in category_dict:
                category_dict[category] = []
            category_dict[category].append(text)
    return category_dict

def write_to_files(category_dict, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for category, texts in category_dict.items():
        file_path = os.path.join(output_dir, f"{category}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            for text in texts:
                file.write(text + '\n')
        print(f"Category '{category}' has {len(texts)} texts.")

def main():
    input_file = 'train.txt'
    output_dir = 'show'
    
    lines = read_train_file(input_file)
    category_dict = parse_lines(lines)
    write_to_files(category_dict, output_dir)

if __name__ == "__main__":
    main()