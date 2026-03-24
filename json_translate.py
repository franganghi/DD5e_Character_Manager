import json
import time
import sys
import requests
from deep_translator import GoogleTranslator
from openai import OpenAI

# Configuration constants
GIST_RAW_URL = "https://gist.githubusercontent.com/dmcb/4b67869f962e3adaa3d0f7e5ca8f4912/raw/"
DELAY_BETWEEN_REQUESTS = 0.5  # Pause in seconds to avoid rate limiting for Google Translator

def fetch_json_data(url: str) -> list:
    """
    Fetches JSON data from the provided URL.
    Returns a list of dictionaries on success, or an empty list on failure.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading JSON: {e}")
        return []

def translate_with_google(text: str, translator: GoogleTranslator) -> str:
    """
    Translates a string using Google Translator.
    """
    if not text:
        return text
    try:
        time.sleep(DELAY_BETWEEN_REQUESTS)
        return translator.translate(text)
    except Exception as e:
        print(f"Google Translation error for string '{text[:20]}...': {e}")
        return text

def translate_with_openai(text: str, target_lang: str, client: OpenAI) -> str:
    """
    Translates a string using OpenAI API with a specific roleplay context prompt.
    """
    if not text:
        return text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"deliver a professional translation to {target_lang}, always considering the context and terminology of a roleplay game related to the Dungeons and Dragons imaginarium."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Translation error for string '{text[:20]}...': {e}")
        return text

def process_spells(spells: list, target_lang: str, api_key: str = None) -> list:
    """
    Iterates over the spell list and translates the main textual fields.
    Uses OpenAI if an API key is provided, otherwise falls back to Google Translator.
    Prints the translated fields to the terminal during execution.
    """
    translator = GoogleTranslator(source='en', target=target_lang)
    client = OpenAI(api_key=api_key) if api_key else None
    engine = "openai" if api_key else "google"

    translated_spells = []
    total_spells = len(spells)

    print(f"Starting translation of {total_spells} spells into '{target_lang}' using {engine.upper()} engine...\n")

    for index, spell in enumerate(spells, start=1):
        print(f"--- Processing: {index}/{total_spells} - {spell.get('name', 'Unknown')} ---")
        
        # Create a shallow copy
        translated_spell = spell.copy()
        
        # Wrapper function to route text to the correct translation engine
        def t_text(text_to_translate):
            if engine == "openai":
                return translate_with_openai(text_to_translate, target_lang, client)
            return translate_with_google(text_to_translate, translator)
            
        # Wrapper function for lists of strings
        def t_list(list_to_translate):
            if not list_to_translate:
                return list_to_translate
            return [t_text(item) for item in list_to_translate]

        # Translate fields dynamically
        if 'name' in translated_spell:
            translated_spell['name'] = t_text(translated_spell['name'])
            
        if 'desc' in translated_spell:
            if isinstance(translated_spell['desc'], list):
                translated_spell['desc'] = t_list(translated_spell['desc'])
            elif isinstance(translated_spell['desc'], str):
                translated_spell['desc'] = t_text(translated_spell['desc'])
                
        if 'description' in translated_spell:
            translated_spell['description'] = t_text(translated_spell['description'])
            
        if 'higher_level' in translated_spell:
            translated_spell['higher_level'] = t_list(translated_spell['higher_level'])
            
        if 'cantripUpgrade' in translated_spell:
            translated_spell['cantripUpgrade'] = t_text(translated_spell['cantripUpgrade'])
            
        if 'range' in translated_spell:
            translated_spell['range'] = t_text(translated_spell['range'])
        if 'material' in translated_spell:
            translated_spell['material'] = t_text(translated_spell['material'])
        if 'duration' in translated_spell:
            translated_spell['duration'] = t_text(translated_spell['duration'])
        if 'casting_time' in translated_spell:
            translated_spell['casting_time'] = t_text(translated_spell['casting_time'])
            
        # Translate school
        if 'school' in translated_spell:
            if isinstance(translated_spell['school'], dict) and 'name' in translated_spell['school']:
                translated_spell['school']['name'] = t_text(translated_spell['school']['name'])
            elif isinstance(translated_spell['school'], str):
                 translated_spell['school'] = t_text(translated_spell['school'])
                 
        # Translate classes
        if 'classes' in translated_spell:
            if isinstance(translated_spell['classes'], list):
                for i, cls in enumerate(translated_spell['classes']):
                    if isinstance(cls, dict) and 'name' in cls:
                        translated_spell['classes'][i]['name'] = t_text(cls['name'])
                    elif isinstance(cls, str):
                        translated_spell['classes'][i] = t_text(cls)
        
        # Print the translated spell dictionary to the terminal
        print("Translated Result:")
        print(json.dumps(translated_spell, indent=4, ensure_ascii=False))
        print("\n" + "="*50 + "\n")
                 
        translated_spells.append(translated_spell)

    return translated_spells

def main():
    """
    Main entry point of the script. 
    Handles command-line arguments, fetches data, translates, and saves to file.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 traduci_incantesimi.py <target_language_code> [openai_api_key]")
        print("Example (Google): python3 traduci_incantesimi.py it")
        print("Example (OpenAI): python3 traduci_incantesimi.py it sk-proj-1234567890...")
        sys.exit(1)

    target_lang = sys.argv[1].lower()
    
    # Check if the API key was passed as the second argument
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    output_file = f"incantesimi_{target_lang}.json"

    spells_data = fetch_json_data(GIST_RAW_URL)
    
    if not spells_data:
        print("No data to process. Exiting.")
        sys.exit(1)

    translated_data = process_spells(spells_data, target_lang, api_key)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)
        print(f"\nTranslation completed successfully! Data saved to: {output_file}")
    except IOError as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    main()
