
# pip install googletrans==4.0.0-rc1 nltk
from googletrans import Translator
import nltk

# Download the Punkt tokenizer models to split scentances
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Max characters that can be translated at a time
MAX_CHARS = 4900

# Initialize translator
translator = Translator()

def translate_text(text, dest_language='en'):
    # Ensure text is a string
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")

    # Split the text into sentences
    sentences = sent_tokenize(text)
    
    translated_text = ""
    temp_text = ""
    
    # Go through all sentences
    for sentence in sentences:
        if len(temp_text + ' ' + sentence) <= MAX_CHARS:
            temp_text += ' ' + sentence if temp_text else sentence
        else:
            # Translate the accumulated text
            try:
                translated_text += translator.translate(temp_text, dest=dest_language).text + " "
            except Exception as e:
                print(f"Error translating text: {str(e)}")
            
            # Start accumulating sentences again
            temp_text = sentence  
    
    # Translate any remaining text
    if temp_text:
        try:
            translated_text += translator.translate(temp_text, dest=dest_language).text
        except Exception as e:
            print(f"Error translating text: {str(e)}")
    
    # Return the translated text
    return translated_text

def translate_json(obj):
    if isinstance(obj, dict):
        # Recursively translate dictionary items
        return {k: translate_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recursively translate list elements
        return [translate_json(element) for element in obj]
    elif isinstance(obj, str):
        # Translate string values
        return translate_text(obj)
    else:
        # Return everything else at it is
        return obj