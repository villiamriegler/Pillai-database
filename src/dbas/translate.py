# pip install googletrans==4.0.0-rc1 nltk
from googletrans import Translator
import nltk

# Download the Punkt tokenizer models to split scentances
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Max characters that can be translated at a time
MAX_CHARS = 5000

# Initialize translator
translator = Translator()

def translate_text(text, dest_language='en'):
    # Split the text into sentences
    sentences = sent_tokenize(text)
    
    translated_text = ""
    temp_text = ""
    
    # Go through all scentances
    for sentence in sentences:
        # Append sentences if it fits withing the maximum char limit for translation
        if len(temp_text) + len(sentence) < MAX_CHARS:
            temp_text += ' ' + sentence
        else:
            # Translate the accumulated text
            translated_text += translator.translate(temp_text, dest=dest_language).text + " "
            translated_text = translated_text.replace('. ', '.').replace('.', '. ')
    
            
            # Start accumulating sentences again
            temp_text = sentence  
    
    # Translate any remaining text
    if temp_text:
        translated_text += translator.translate(temp_text, dest=dest_language).text
    
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