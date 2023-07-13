import requests
import argparse
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_bitlink(token, link):
    headers = {'Authorization': token}
    parsed_link = urlparse(link)
    bitlink = f'{parsed_link.netloc}{parsed_link.path}'
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'.format(
        bitlink=bitlink)
    response = requests.get(url, headers=headers)
    return response.ok


def shorten_link(token, link):
    headers = {'Authorization': token}
    url = 'https://api-ssl.bitly.com/v4/shorten'
    json_payload = {'long_url': link}
    response = requests.post(url, headers=headers, json=json_payload)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(token, bitlink):
    headers = {'Authorization': token}
    parsed_link = urlparse(link)
    bitlink = f'{parsed_link.netloc}{parsed_link.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    description = 'Программа для сокращения ссылок'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('url', help='Ссылка для сокращения')

    args = parser.parse_args()
    link = args.url
    try:
        if is_bitlink(bitly_token, link):
            clicks_total = count_clicks(bitly_token, link)
            print('Кол-во кликов: ', clicks_total)
        else:
            bitlink = shorten_link(bitly_token, link)
            print('Битлинк: ', bitlink)
    except requests.exceptions.HTTPError:
        print('Неправильная ссылка')
