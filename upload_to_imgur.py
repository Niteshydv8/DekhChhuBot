import os
import pyimgur

CLIENT_ID = ""
FOLDER_PATH = "posters"

im = pyimgur.Imgur(CLIENT_ID)

for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        full_path = os.path.join(FOLDER_PATH, filename)
        title = filename.replace("_", " ").replace(".jpg", "").title()
        uploaded_image = im.upload_image(full_path, title=title)
        print(f"{filename}: {uploaded_image.link}")
