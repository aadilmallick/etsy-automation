from dotenv import load_dotenv 
import os
from PyPDF2 import PdfReader
import requests
from urllib.parse import urlencode
import google.generativeai as genai
from ai import AI
from PIL import Image
import base64
import fitz
import re

load_dotenv()

KEY_SECRET = os.getenv('KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
if not KEY_SECRET or not access_token:
    print(KEY_SECRET, access_token)
    raise "Error getting KEY_SECRET or ACCESS_TOKEN from environment variables"

myai = AI()

def get_shop_section_id(shop_id: int):
    url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/sections"
    headers = {
        "x-api-key": KEY_SECRET,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    count = data['count']
    results = data['results']
    shop_section_id = results[0]['shop_section_id']
    if not shop_section_id:
        raise "Error getting shop_section_id"
    return shop_section_id

def get_me():
    url = "https://openapi.etsy.com/v3/application/users/me"
    headers = {
        "x-api-key": KEY_SECRET,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    user_id = data['user_id']
    shop_id = data['shop_id']
    if not user_id or not shop_id:
        raise "Error getting user_id or shop_id"
    return user_id, shop_id

def create_listing(shop_id: int, filename: str):
    filepath = f"sheetmusic/{filename}"
    if not os.path.exists(filepath):
        print("File does not exist")
        return
    url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings"
    headers = {
        "x-api-key": KEY_SECRET,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    sheet_music_title = myai.create_sheet_name(filename)
    sheet_music_description = myai.create_description(filename)
    shop_section_id = get_shop_section_id(shop_id)
    data = {
        "is_digital": "true",
        "quantity": 999,
        "price": 1.49,
        "who_made": "i_did",
        "when_made": "2020_2024",
        "taxonomy_id": 1,
        "title": sheet_music_title,
        "description": sheet_music_description,
        "should_auto_renew": "true",
        "tags": ["sheet music", "piano", "piano tutorial", "piano sheet music",
                 "sheet music pdf", "piano pdf", "piano sheet music pdf", sheet_music_title],
        "shop_section_id": shop_section_id,
        "type": "download"
    }
    form_data = urlencode(data, encoding='utf-8')
    # 1. create listing draft
    response = requests.post(url, headers=headers, data=form_data)
    data = response.json()
    response.raise_for_status()
    listing_id = data['listing_id']

    # 2. upload pdf file for digital listing
    upload_file_url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}/files"
    headers = {
        "x-api-key": KEY_SECRET,
        "Authorization": f"Bearer {access_token}",
    }

    binary_encode_file = open(filepath, "rb").read()
    response = requests.post(upload_file_url, headers=headers, files={"file": binary_encode_file},
                  data={"name": filename})
    response.raise_for_status()

    # 3. upload image for listing
    thumbnail_path = create_thumbnail(filename)
    url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}/images"
    headers = {
        "x-api-key": KEY_SECRET,
        "Authorization": f"Bearer {access_token}",
    }
    binary_encode_file = open(thumbnail_path, "rb").read()
    response = requests.post(upload_file_url, headers=headers, files={"image": binary_encode_file})
    response.raise_for_status()
    os.remove(thumbnail_path)

    # 4. publish listing
    url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}"
    headers = {
        "x-api-key": KEY_SECRET,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "state": "active"
    }
    form_data = urlencode(data, encoding='utf-8')
    response = requests.put(url, headers=headers, data=form_data)
    response.raise_for_status()

def to_base_64(file_path: str):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def create_thumbnail(filename: str):
    THUMBNAIL_SIZE = [570, 456]
    THUMBNAIL_SHEET_MUSIC_HEIGHT = 422

    # 1. extract the first page of the pdf as an image
    filepath = f"sheetmusic/{filename}"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filename} not found")
    pdf = fitz.open(filepath)
    pdf_first_page = next(pdf.pages())
    pix = pdf_first_page.get_pixmap()

    img_name = re.split(r"\.", filename)[0]

    pdf_image_path = f"tempimages/{img_name}.jpg"
    pix.save(pdf_image_path)

    # 2. create a thumbnail image with the sheet music image
    background_image = Image.open("thumbnail-background.jpg")
    pdf_image = Image.open(pdf_image_path)

        # max height of 536, maintains aspect ratio
    pdf_image.thumbnail((THUMBNAIL_SIZE[0], THUMBNAIL_SHEET_MUSIC_HEIGHT))
    pdf_image.save(pdf_image_path)

    background_image.paste(pdf_image, (136, 17))
    background_image.save(f"thumbnails/{img_name}.jpg")

    os.remove(pdf_image_path)
    return f"thumbnails/{img_name}.jpg"

if __name__ == "__main__":
    user_id, shop_id = get_me()
    print(user_id, shop_id)
    create_listing(shop_id, "test.pdf")