
# We are going to create the QR code by using the python
# For that we need to install pyqrcode module

import pyqrcode
from pyqrcode import QRCode
# URL for the website for which we want to use the qr code or we are going to assign into qr code
url = 'https://www.instagram.com/accounts/login/'

# Genrates the qr code 
qr = pyqrcode.create(url)

#Create and save the png file naming "QRCode.svg"
qr.svg("QRCode.svg",scale = 8)
