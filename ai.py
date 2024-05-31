from dotenv import load_dotenv 
import google.generativeai as genai

class AI:
    def __init__(self):
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")


        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.title_generation_config = {
        "temperature": 0.1,
        "max_output_tokens": 20,
        "top_k": 1,
        "response_mime_type": "text/plain",
        }

        self.description_generation_config = genai.types.GenerationConfig(
        max_output_tokens=500,
        stop_sequences=["Keywords:"]
        )
        
    def create_description(self, filename: str):
        text_prompt = """I will give you a filename representing a piano sheet music pdf, 
        and your task is to create an etsy listing description that adequately talks about the pdf. 
        Subtly disperse keywords for SEO throughout the description text, 
        writing them with natural language."""

        response = self.model.generate_content(contents=[text_prompt, filename], 
                                        generation_config=self.description_generation_config)
        return response.text
    
    def create_sheet_name(self, filename: str):
        text_prompt = """I will give you a filename representing a sheet music pdf, 
        and your task is to extract the readable name formatted with spaces. 
        Do not output anything else except JSON in the form like so: {"name": "name here"}

        For example, the filename 7_Rings_-_Ariana_Grande__Piano_Tutorial.pdf should return a name like 
        "7 Rings - Ariana Grande Piano Tutorial" and You_re Not Alone FF9.pdf should return a name like 
        "You're Not Alone - FF9". 
        Use your judgment when creating the best possible title names from the filenames 
        as I am creating these for customers.
        """

        response = self.model.generate_content(contents=[text_prompt, filename], 
                                               generation_config=self.title_generation_config)
        return response.text