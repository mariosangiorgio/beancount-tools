#!/usr/local/bin/python3
import requests
import datetime
import sys

class AlphaVantage:
  def __init__(self, api_key):
    self.api_key = api_key

  def get_fx_rate(self, base_currency, to_currency):
    params = {
      'function' : 'CURRENCY_EXCHANGE_RATE',
      'from_currency' : base_currency,
      'to_currency' : to_currency,
      'apikey' : self.api_key
    }
    r = requests.get("https://www.alphavantage.co/query", params=params)
    json = r.json()
    return json['Realtime Currency Exchange Rate']['5. Exchange Rate']

if __name__ == "__main__":
  token = sys.argv[1]
  currency_pairs = [('EUR', 'GBP'), ('USD', 'GBP')]
  api = AlphaVantage(token)

  datestamp = datetime.datetime.now().strftime('%Y-%m-%d')
  for (base_currency, to_currency) in currency_pairs:
    print(f"{datestamp} price {base_currency} {api.get_fx_rate(base_currency, to_currency)} {to_currency}")