import csv
import os

def convert_date(date):
  """
  Converts the date from the DD/MM/YYYY format to YYYY-MM-DD
  >>> convert_date("13/04/2018")
  '2018-04-13'
  """
  tokens = date.split("/")
  return f"{tokens[2]}-{tokens[1]}-{tokens[0]}"

category_map = {}
unmapped_categories = set()

with open('category-map.csv') as csvfile:
  for mapping in csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=true):
    category_map[mapping[0]] = mapping[1]

with open(os.path.expanduser('~/Downloads/ofx.csv')) as csvfile:
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
      print(f'  Liabilities:AmericanExpress {amount} GBP')
      print(f'  {category_map[payee]}')
      print()
    else:
      unmapped_categories.add(payee)
if unmapped_categories:
  print("Some categories have not been mapped")
  for category in unmapped_categories:
    print(f'"{category}"')