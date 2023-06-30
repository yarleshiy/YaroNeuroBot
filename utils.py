import openai
import logging
import config
import time
import json
import requests

openai.api_key = config.OPENAI_TOKEN


async def generate_text(prompt) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(
            prompt=prompt,
            n=n,
            size=size
        )
        urls = []
        for i in response['data']:
            urls.append(i['url'])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls

async def generate_voice(prompt):
    headers = {"Authorization": f'Bearer {config.VOICE_TOKEN}'}
    url = 'https://api.edenai.run/v2/audio/text_to_speech'
    payload = {
        'providers': 'lovoai',
        'language': 'ru-RU',
        'option': 'MALE',
        'lovoai': "ru-RU_Alexei Syomin",
        'text': f'{prompt}',
        "audio_format": "wav"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    unx_tine = int(time.time())

    # with open(f'{unx_tine}.json', 'w') as file:
    #     json.dump(result, file, indent=4, ensure_ascii=False)

    audio_url = result.get('lovoai').get('audio_resource_url')
    r = requests.get(audio_url)
   # print(r.content)


    # with open(f'{unx_tine}.wav', 'wb') as file:
    #     file.write(r.content)
    #
    # voice = file
    # print(voice.name)
    return audio_url
