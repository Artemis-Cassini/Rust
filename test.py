from pyzbar.pyzbar import decode
from PIL import Image

# Test with an actual barcode image
image = Image.open("barcode_example.png")  # Replace with the path to your barcode image
decoded = decode(image)

if decoded:
    print("Barcode detected:", decoded[0].data.decode("utf-8"))
else:
    print("No barcode detected.")