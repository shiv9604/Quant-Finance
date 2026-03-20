
#Email  slicer is a tool which seprates the username and domain from the email
# we are going to build a email slicer...

email = input("Enter the email : ").strip()
username = email[:email.index('@')]
domain = email[email.index('@')+1:]
print(f"Username : {username}")
print(f"Domain : {domain}")
