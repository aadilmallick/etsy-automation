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
from automation import SeleniumScraper, main_loop
import time
import pyperclip

load_dotenv()

myai = AI()

if __name__ == "__main__":
    sheetmusic = os.listdir("sheetmusic")[221:]
    scraper = SeleniumScraper(raise_if_elements_missing=True, headless=True)
    for filename in sheetmusic:
        print("creating listing for ", filename)
        main_loop(scraper, myai, filename)
        print(f"created listing for {filename}")
    print("finished creating all listings")
    scraper.driver.quit()
    