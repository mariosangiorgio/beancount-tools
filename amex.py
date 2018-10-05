#!/usr/local/bin/python3
import csv
import json
import argparse
from collections import defaultdict

def convert_date(date):
  """
  Converts the date from the DD/MM/YYYY format to YYYY-MM-DD
  >>> convert_date("13/04/2018")
  '2018-04-13'
  """
  tokens = date.split("/")
  return f"{tokens[2]}-{tokens[1]}-{tokens[0]}"

def load_category_map(category_map_file):
  """
  Loads mapping between payees (as repored in the statement) and
  expenses categories.
  The input file is expected to be a json file with categories as
  keys and payees as values.

  E.g.
  {
    "Expenses:PublicTransport": ["OysterCard"]
  }
  """
  category_map = {}
  with open(category_map_file) as f:
    for (category, payees) in json.loads(f.read()).items():
      for payee in payees:
        category_map[payee] = category
  return category_map

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description='Converts a csv file downloaded from American Express to ' +
                'a list of beancount entries.')
  parser.add_argument('-c', '--category_map', type=str, help='The category map file')
  parser.add_argument('-d', '--data', type=str, help='The ofx.csv file')

  args = parser.parse_args()
  category_map = load_category_map(args.category_map)
  unmapped_categories = set()

  with open(args.data) as csvfile:
    transactions = csv.reader(csvfile, delimiter=',', quotechar='"', )
    for transaction in transactions:
      date = transaction[0]
      amount = transaction[2]
      payee = transaction[3]
      if payee == 'PAYMENT RECEIVED - THANK YOU':
        # Ignoring, I'll add this entry when reconciling other accounts
        continue
      if payee in category_map:
        print(f'{convert_date(date)} * "{payee}" "Automatically converted"')
        print(f'  {category_map[payee]} {amount} GBP')
        print(f'  Liabilities:AmericanExpress')
        print()
      else:
        unmapped_categories.add(payee)
  if unmapped_categories:
    print("Some categories have not been mapped")
    for category in unmapped_categories:
      print(f'"{category}"')