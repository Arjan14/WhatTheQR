import qrcode

qr = qrcode.QRCode(
    version=1,
    box_size=15,
    border=10
)

data = 'https://github.com/arjan14'
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image()
img.save('qr.png')