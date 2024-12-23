import requests



def get_list_campaign(token, status):
    url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    params = {
        'status': status,
        'type': 8,
        'order': "create",
        'direction': "desc"
    }

    response = requests.post(url, headers=headers, params=params)
    return response


def get_full_list_campaign(token):
    response = get_list_campaign(token, 11)
    list_campaign_11 = [['error', 'error']]
    if response.status_code == 200:
        list_campaign_11 = [[i['name'], i['advertId']] for i in response.json()]

    elif response.status_code == 401 or response.status_code == 429:
        list_campaign_11 = [['error', 'error']]

    response = get_list_campaign(token, 9)
    list_campaign_9 = []
    if response.status_code == 200:
        list_campaign_9 = [[i['name'], i['advertId']] for i in response.json()]

    elif response.status_code == 401 or response.status_code == 429:
        list_campaign_9 = [['error', 'error']]

    list_campaign = list_campaign_9 + list_campaign_11
    return list_campaign

def check_token(token):

    url = 'https://common-api.wildberries.ru/ping'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    return response.status_code


def start_campaign(token, id_campaign):
    url = 'https://advert-api.wb.ru/adv/v0/start'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    params = {
        'id': id_campaign,
    }

    response = requests.get(url, headers=headers, params=params)
    return response


def pause_campaign(token, id_campaign):
    url = 'https://advert-api.wb.ru/adv/v0/pause'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    params = {
        'id': id_campaign,
    }

    response = requests.get(url, headers=headers, params=params)
    return response

print(get_full_list_campaign(token))
