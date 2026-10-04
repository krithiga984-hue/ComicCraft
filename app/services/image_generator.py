import os
import requests
import random

def generate_image(prompt, filename=None):
    if filename is None:
        filename = "panel.jpg"

    panels_dir = "app/static/panels"
    os.makedirs(panels_dir, exist_ok=True)
    file_path = os.path.join(panels_dir, filename)

    try:
        print("Generating panel image...")
        
        seed = random.randint(1, 10000)
        img_url = f"https://picsum.photos/seed/{seed}/600/600"
        
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"SUCCESS: {filename}")
        
        return f"/static/panels/{filename}"
        
    except Exception as e:
        print(f"ERROR: {e}")
        return f"/static/panels/{filename}"