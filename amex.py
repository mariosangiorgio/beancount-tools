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

def load_category_map(category_map_file):
  """
  Loads mapping between payees (as repored in the statement) and
  expenses categories.
  The input file is expected to be a csv with payees in the first
  column and categories in the second.

  E.g.
  "OysterCard", "Expenses:PublicTransport"
  """
  category_map = {}
  with open(category_map_file) as csvfile:
    for mapping in csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True):
      category_map[mapping[0]] = mapping[1]
  return category_map

category_map = load_category_map('category-map.csv')
unmapped_categories = set()

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
      print(f'  {category_map[payee]} {amount} GBP')
      print(f'  Liabilities:AmericanExpress')
      print()
    else:
      unmapped_categories.add(payee)
if unmapped_categories:
  print("Some categories have not been mapped")
  for category in unmapped_categories:
    print(f'"{category}"')