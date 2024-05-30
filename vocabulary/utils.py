import requests

from ninja.errors import HttpError


def fetch_word_data(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Default values
        meaning = "No definition available."
        example_sentence = "No example available."
        phonetic = data[0].get('phonetic', '')
        audio_url = data[0]['phonetics'][0].get('audio', '') if data[0].get('phonetics') else ''
        origin = data[0].get('origin', '')
        part_of_speech = "No part of speech available."

        # Iterate through the meanings to find the first example
        for meaning_data in data[0]['meanings']:
            if part_of_speech == "No part of speech available.":
                part_of_speech = meaning_data['partOfSpeech']
            for definition_data in meaning_data['definitions']:
                # Update meaning with the first found definition
                if meaning == "No definition available.":
                    meaning = definition_data['definition']
                # Update example sentence with the first found example
                if 'example' in definition_data and example_sentence == "No example available.":
                    example_sentence = definition_data['example']
                # Break the loop if both meaning and example have been found
                if meaning != "No definition available." and example_sentence != "No example available.":
                    break
            if meaning != "No definition available." and example_sentence != "No example available.":
                break

        return {"word": word,
                'phonetic': phonetic,
                'audio_url': audio_url,
                'meaning': meaning,
                'example_sentence': example_sentence,
                'origin': origin,
                'part_of_speech': part_of_speech
                }
    else:
        raise HttpError(404, "Word not found in the dictionary.")
