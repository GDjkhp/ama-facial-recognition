import os
import cv2
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import json
import mediapipe as mp

def train_images():
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

    # Create a dictionary to store name and embeddings
    embeddings_dict = {}

    # Initialize imgbeddings
    ibed = imgbeddings()

    # Iterate through the dataset directory
    dataset_dir = 'received_images'
    if not os.path.exists(dataset_dir):
        print(f"Error: '{dataset_dir}' directory not found.")
        exit(1)

    for name in os.listdir(dataset_dir):
        print(name)
        person_dir = os.path.join(dataset_dir, name)
        if os.path.isdir(person_dir):
            embeddings_list = []
            # Iterate through the image files in the person's directory
            for image_file in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_file)
                # https://stackoverflow.com/questions/43185605/how-do-i-read-an-image-from-a-path-with-unicode-characters
                stream = open(image_path, "rb")
                bytes = bytearray(stream.read())
                numpyarray = np.asarray(bytes, dtype=np.uint8)
                image = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
                if image is None:
                    print(f"Warning: Failed to read image '{image_path}'")
                    continue

                # Convert the image to RGB for MediaPipe
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_image)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        # Get bounding box from landmarks
                        h, w, _ = image.shape
                        x_min = int(min([landmark.x for landmark in face_landmarks.landmark]) * w)
                        x_max = int(max([landmark.x for landmark in face_landmarks.landmark]) * w)
                        y_min = int(min([landmark.y for landmark in face_landmarks.landmark]) * h)
                        y_max = int(max([landmark.y for landmark in face_landmarks.landmark]) * h)

                        # Ensure the bounding box is within the image
                        x_min, y_min = max(0, x_min), max(0, y_min)
                        x_max, y_max = min(w, x_max), min(h, y_max)

                        # Check if the face region is valid
                        if x_min < x_max and y_min < y_max:
                            # Extract face image
                            face_img = image[y_min:y_max, x_min:x_max]
                            
                            # Check if face_img is not empty
                            if face_img.size > 0:
                                pil_img = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
                                embedding = ibed.to_embeddings(pil_img)[0]
                                embeddings_list.append(embedding.tolist())

            # Store the average embedding for the person
            if embeddings_list:
                avg_embedding = np.mean(embeddings_list, axis=0)
                embeddings_dict[name] = avg_embedding.tolist()

    # Save the embeddings to a JSON file
    with open("face_embeddings.json", "w", encoding="utf-8") as f:
        json.dump(embeddings_dict, f)

    print("Face embeddings saved successfully.")

    # Close the MediaPipe Face Mesh
    face_mesh.close()

if __name__ == "__main__":
    train_images()