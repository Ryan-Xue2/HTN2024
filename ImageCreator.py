import os
import io
import base64
import requests
from PIL import Image


class ImageCreator:
    def __init__(self):
        self.url = "https://api.getimg.ai/v1/stable-diffusion-xl/image-to-image"

    def create_image(self, to_memorize, image_path):
        # Read the image file, resize if necessary, and encode it to base64

        with Image.open(image_path) as img:
            # Check if resizing is needed
            if img.width > 1536 or img.height > 1536:
                img.thumbnail((1536, 1536), Image.LANCZOS)
            
            # Save the image to a bytes buffer
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Encode the image to base64
            encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # prompt = f"""Modify the environment in the image in order to help the user memorize the following information: '{to_memorize}'. 
        # Integrate the information to be memorized into the image, e.g., if there is bathroom, and the information to memorize is a grocery list, 
        # then make the items in the grocery list appear in the bathroom. The idea is like a memory palace, where you associate the items to memorize with the locations in the image."""
        prompt = f"A modified and unrealistic photo where the all of ({to_memorize})interact with locus in the image. Make sure to integrate ALL the items in the list into the image."
        # prompt = f"Make the things listed in the list here interact with locus in the image: Bananas, apples, oranges, pears, and a fork"
        payload = {
            "model": "stable-diffusion-xl-v1-0",
            "prompt": to_memorize,
            "negative_prompt": "disfigured, blurry, cartoony",
            "prompt_2": to_memorize,
            "image": encoded_image,
            "strength": 0.5,
            "steps": 50,
            "guidance": 7.5,
            "seed": 0,
            "scheduler": "euler",
            "output_format": "jpeg",
            "response_format": "url"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": os.getenv("GETIMG_API_KEY")
        }
        response = requests.post(self.url, json=payload, headers=headers)

        return response.json()["url"]