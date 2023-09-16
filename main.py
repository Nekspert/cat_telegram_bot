import requests
import time
from bs4 import BeautifulSoup  #установите 'lxml' (pip install lxml)
API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://mimimi.ru/random'
BOT_TOKEN = '6478498744:AAEKuFfZqlARHYC_re4FCeVsT7xhpOmWyts'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('

offset = -2
counter = 0
cat_response: requests.Response
cat_link: str

while True:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        text = f"{updates['result'][0]['message']['text']} конечно хорошо, но лучше картика с котиком! (для Максима нюдсы в раработке)"
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = BeautifulSoup(cat_response.text, 'lxml').find('div', class_='wrapper').find('div', class_='mi-image').find('img').get('src')
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')            
            
    time.sleep(1)
    counter += 1
