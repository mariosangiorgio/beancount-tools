import csv
import os

with open(os.path.expanduser('~/Downloads/ofx.csv')) as csvfile:
  transactions = csv.reader(csvfile, delimiter=',', quotechar='"')
  for transaction in transactions:
    print(f'{transaction[0]} - "{transaction[3]}" ""')
    print(f'  Liabilities:AmericanExpress {transaction[3]} GBP')
    print(f'  Expenses:AmericanExpress')
    print()