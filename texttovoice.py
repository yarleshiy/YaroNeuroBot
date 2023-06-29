import json
import os
import time
import requests
import config

def text_to_speech(text='Привет, дорогой друг! Что тебя привело сюда?'):
    headers = {"Authorization": f'Bearer {config.VOICE_TOKEN}'}
    url = 'https://api.edenai.run/v2/audio/text_to_speech'
    payload = {
        'providers': 'lovoai',
        'language': 'ru-RU',
        'option': 'MALE',
        'lovoai' : "ru-RU_Alexei Syomin",
        'text': f'{text}',
        "audio_format": "wav"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    unx_tine = int(time.time())

    # with open(f'{unx_tine}.json', 'w') as file:
    #     json.dump(result, file, indent=4, ensure_ascii=False)

    audio_url = result.get('lovoai').get('audio_resource_url')
    r = requests.get(audio_url)

    with open(f'{unx_tine}.wav', 'wb') as file:
        file.write(r.content)


text_to_speech(text='Легенд происхождения чая много, но начало одно, так и неизвестное историкам. Может стоит принять позицию «божественного происхождения»\
                         чая, испить из чашки и окунуться в таинство, скрываемое им, почувствовать бодрость Шен Нуна или созерцательную ясность Дармы?')
