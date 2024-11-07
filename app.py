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
from automation import SeleniumScraper
import time
import pyperclip

load_dotenv()

myai = AI()


def to_base_64(file_path: str):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def scale_image(image: Image.Image, scale_factor: float) -> Image.Image:
    """
    Scales up a PIL image by a given factor, maintaining the aspect ratio.

    Parameters:
    - image (PIL.Image.Image): The input image to scale.
    - scale_factor (float): The factor by which to scale the image.

    Returns:
    - PIL.Image.Image: The scaled-up image.
    """
    # Calculate new dimensions while maintaining aspect ratio
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    
    # Resize the image with the new dimensions
    scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
    return scaled_image
    

def create_thumbnail_and_cover(filename: str):
    THUMBNAIL_SIZE = [600, 600]
    THUMBNAIL_SHEET_MUSIC_HEIGHT = 546

    if not os.path.exists("thumbnails"):
        os.makedirs("thumbnails")

    if not os.path.exists("tempimages"):
        os.makedirs("tempimages")
    
    if not os.path.exists("covers"):
        os.makedirs("covers")

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

    """ 
    create thumbnail
    """

    # 2. create a thumbnail image with the sheet music image
    background_image = Image.open("thumbnail-background.jpg")
    pdf_image = Image.open(pdf_image_path)

    # max height of 536, maintains aspect ratio
    pdf_image.thumbnail((THUMBNAIL_SIZE[0], THUMBNAIL_SHEET_MUSIC_HEIGHT))
    pdf_image.save(pdf_image_path)

    background_image.paste(pdf_image, (106, 34))
    background_image.save(f"thumbnails/{img_name}.jpg")

    """ 
    create cover
    """

    background_image = Image.open("cover-background.jpg")
    pdf_image_2 = Image.open(pdf_image_path)

    pdf_image_2 = scale_image(pdf_image_2, 1.2)

    background_image.paste(pdf_image_2, (46, 34))
    background_image.save(f"covers/{img_name}.jpg")

    os.remove(pdf_image_path)
    return f"thumbnails/{img_name}.jpg", f"covers/{img_name}.jpg"

if __name__ == "__main__":
    filename = "_Black_Panther_-_Killmonger_Piano_Tutorial.pdf"
    scraper = SeleniumScraper(detached=True, raise_if_elements_missing=True)
    