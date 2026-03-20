# Advances password genrator in python with the help of random module
# A  strong password should be like 
# At least 8 characters—the more characters, the better.
# A mixture of both uppercase and lowercase letters.
# A mixture of letters and numbers.
# Inclusion of at least one special character, e.g., ! @ # ? ] Note: do not use < or > in your password, as both can cause problems in Web browsers.

import string
import random
lenth = int(input("Enter the lenth of password do you want : "))
uppercase = [i for i in string.ascii_uppercase]
lowercase = [i for i in string.ascii_lowercase]
num = [str(i) for i in range(1,10)]
symbols = ("!$%&'()*+,-./:;<=>?@[\]^_`{|}~").split()
password =  uppercase + lowercase + num + symbols
total_string = ''.join(password)

result = ''.join(random.sample(total_string,lenth))
print(result)w