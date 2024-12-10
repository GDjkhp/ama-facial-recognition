import os, json
import base64

directory = "received_images"
if not os.path.exists(directory): os.makedirs(directory)

dataset_dir = "json"
if not os.path.exists(dataset_dir):
    print(f"Error: '{dataset_dir}' directory not found.")
    exit(1)

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def parse_json():
    for name in os.listdir(dataset_dir):
        data = read_json_file(os.path.join(dataset_dir, name))
        name = data.get("name")
        usn = data.get("usn")
        images = data.get("images")

        image_folder = f'{directory}/{name}'
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        for i, img_str in enumerate(images):
            img_data = base64.b64decode(img_str)
            file_path = os.path.join(image_folder, f"{name}_{usn}_{i}.jpg")
            print(f"{name}_{usn}_{i}.jpg")
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)

if __name__ == "__main__":
    parse_json()