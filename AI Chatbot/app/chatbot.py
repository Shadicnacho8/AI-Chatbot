from app.config import Config
import google.generativeai as genai
import marko


class Chatbot():
    # Configure the generative AI API key
    # <<----<< You can get your API key from the Gemini website and put it here!
    genai.configure(api_key=Config.GEMINI_AI_API_KEY)

    # Define the generation configuration for the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
    }

    # Define the safety settings for content generation
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]

    # Create an instance of the generative model
    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    def get_ai_response(self, msg: str):
        aiResponse = self.model.generate_content(msg)
        response = marko.convert(aiResponse.text)
        return response
