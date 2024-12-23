import requests

class work_api():
    def __init__(self):
        self.type_ping = [
            'https://content-api.wildberries.ru/ping',
            'https://seller-analytics-api.wildberries.ru/ping',
            'https://discounts-prices-api.wildberries.ru/ping',
            'https://marketplace-api.wildberries.ru/ping',
            'https://statistics-api.wildberries.ru/ping',
            'https://advert-api.wildberries.ru/ping',
            'https://feedbacks-api.wildberries.ru/ping',
            'https://buyer-chat-api.wildberries.ru/ping',
            'https://supplies-api.wildberries.ru/ping',
            'https://returns-api.wildberries.ru/ping',
            'https://documents-api.wildberries.ru/ping',
            'https://common-api.wildberries.ru/ping',
        ]

    def check_token(self, token):
        count = 0
        for check_type_ping in self.type_ping:
            url = check_type_ping

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                count += 1

        if count == len(self.type_ping):
            return True
        return False

    def get_list_campaign(self, token, status, type):
        url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'status': status,
            'type': type,
            'order': "create",
            'direction': "desc"
        }

        response = requests.post(url, headers=headers, params=params)
        return response

    def get_full_list_campaign(self, token):
        response = self.get_list_campaign(token, 11, 8)
        list_campaign_11_8 = []
        if response.status_code == 200:
            list_campaign_11_8 = [[i['name'], i['advertId']] for i in response.json()]

        response = self.get_list_campaign(token, 9, 8)
        list_campaign_9_8 = []
        if response.status_code == 200:
            list_campaign_9_8 = [[i['name'], i['advertId']] for i in response.json()]

        response = self.get_list_campaign(token, 11, 9)
        list_campaign_11_9 = []
        if response.status_code == 200:
            list_campaign_11_9 = [[i['name'], i['advertId']] for i in response.json()]

        response = self.get_list_campaign(token, 9, 9)
        list_campaign_9_9 = []
        if response.status_code == 200:
            list_campaign_9_9 = [[i['name'], i['advertId']] for i in response.json()]

        list_campaign = list_campaign_11_8 + list_campaign_9_8 + list_campaign_11_9 + list_campaign_9_9
        return list_campaign