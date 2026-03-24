import json
import time
import sys
import requests
from deep_translator import GoogleTranslator

# Configuration constants
GIST_RAW_URL = "https://gist.githubusercontent.com/dmcb/4b67869f962e3adaa3d0f7e5ca8f4912/raw/"
DELAY_BETWEEN_REQUESTS = 0.5  # Pause in seconds to avoid rate limiting

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

def translate_text(text: str, translator: GoogleTranslator) -> str:
    """
    Translates a single text string.
    Handles null or empty input values safely.
    """
    if not text:
        return text
    try:
        time.sleep(DELAY_BETWEEN_REQUESTS)
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error for string '{text[:20]}...': {e}")
        return text

def translate_list(text_list: list, translator: GoogleTranslator) -> list:
    """
    Iterates over a list of strings and translates them individually.
    """
    if not text_list:
        return text_list
    return [translate_text(item, translator) for item in text_list]

def process_spells(spells: list, target_lang: str) -> list:
    """
    Iterates over the spell list and translates the main textual fields
    into the specified target language.
    """
    translator = GoogleTranslator(source='en', target=target_lang)
    translated_spells = []
    total_spells = len(spells)

    print(f"Starting translation of {total_spells} spells into '{target_lang}'...")

    for index, spell in enumerate(spells, start=1):
        print(f"Processing: {index}/{total_spells} - {spell.get('name', 'Unknown')}")
        
        # Create a shallow copy to avoid destructive mutation of the original object
        translated_spell = spell.copy()
        
        # Translate specific text fields
        if 'name' in translated_spell:
            translated_spell['name'] = translate_text(translated_spell['name'], translator)
        if 'desc' in translated_spell:
            translated_spell['desc'] = translate_list(translated_spell['desc'], translator)
        if 'higher_level' in translated_spell:
            translated_spell['higher_level'] = translate_list(translated_spell['higher_level'], translator)
        if 'range' in translated_spell:
            translated_spell['range'] = translate_text(translated_spell['range'], translator)
        if 'material' in translated_spell:
            translated_spell['material'] = translate_text(translated_spell['material'], translator)
        if 'duration' in translated_spell:
            translated_spell['duration'] = translate_text(translated_spell['duration'], translator)
        if 'casting_time' in translated_spell:
            translated_spell['casting_time'] = translate_text(translated_spell['casting_time'], translator)
        if 'school' in translated_spell:
            if isinstance(translated_spell['school'], dict) and 'name' in translated_spell['school']:
                translated_spell['school']['name'] = translate_text(translated_spell['school']['name'], translator)
            elif isinstance(translated_spell['school'], str):
                 translated_spell['school'] = translate_text(translated_spell['school'], translator)
                 
        translated_spells.append(translated_spell)

    return translated_spells

def main():
    """
    Main entry point of the script. 
    Handles command-line arguments, fetches data, translates, and saves to file.
    """
    # Check if target language argument is provided
    if len(sys.argv) < 2:
        print("Usage: python3 traduci_incantesimi.py <target_language_code>")
        print("Example: python3 traduci_incantesimi.py it")
        sys.exit(1)

    target_lang = sys.argv[1].lower()
    output_file = f"incantesimi_{target_lang}.json"

    spells_data = fetch_json_data(GIST_RAW_URL)
    
    if not spells_data:
        print("No data to process. Exiting.")
        sys.exit(1)

    translated_data = process_spells(spells_data, target_lang)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)
        print(f"\nTranslation completed successfully! Data saved to: {output_file}")
    except IOError as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    main()
