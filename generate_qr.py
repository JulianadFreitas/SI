import qrcode

base_url = "http://127.0.0.1:5000/call/"

tables = ['mesa1', 'mesa2', 'mesa3']

for table in tables:
    url = base_url + table
    img = qrcode.make(url)
    img.save(f"{table}.png")

print("QR Codes gerados com sucesso.")
