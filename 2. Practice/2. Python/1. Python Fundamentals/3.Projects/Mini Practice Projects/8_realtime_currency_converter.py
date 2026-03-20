# for the real time currency rates we are going to use the forex-python library...

from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes

c = CurrencyRates()
s = CurrencyCodes()
# print(c.convert('USD','INR',1))

amount = int(input("Enter the amount : "))

from_currency = input("Enter the currency from which you want to convert your amount : ")
to_currency = input("Enter the currency in which you want to convert your amount : ")

currency_input = from_currency.upper()
currency_output = to_currency.upper()

symbol = s.get_symbol(f'{currency_input}')
# print(f'{currency_input}',f'{currency_output}',amount)

result = c.convert(f'{currency_input}',f'{currency_output}',amount)
print(f"\nYour amount {symbol}{amount} from {currency_input} to {currency_output} is = {result}\n")