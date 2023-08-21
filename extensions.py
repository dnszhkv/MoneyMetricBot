import requests
import json
from config import keys


# Задаётся класс исключений, наследованный от Exception
class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # Вывод ошибки в случае, когда:
        # введены одинаковые валюты
        if quote == base:
            raise APIException(f'Нельзя перевести одинаковые валюты: {base}')
        # запрашиваемых валют нет в словаре
        try:
            quote_ticker = keys[quote]
        except:
            raise APIException(f'Не удалось обработать валюту: {quote}')
        try:
            base_ticker = keys[base]
        except:
            raise APIException(f'Не удалось обработать валюту: {base}')
        # вместо числа введено слово или набор букв (знаков)
        try:
            amount = float(amount)
        except:
            raise APIException(f'Не удалось обработать количество: {amount}')
        # запрос в CryptoCompare
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # парсинг полученного ответа
        total_base = json.loads(r.content)[keys[base]]

        return total_base