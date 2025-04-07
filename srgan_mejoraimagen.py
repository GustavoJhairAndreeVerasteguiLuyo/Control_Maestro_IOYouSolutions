from ISR.models import RDN
from PIL import Image

rdn = RDN(weights='psnr-small')
img = Image.open('frame_borroso.jpg')
lr_img = img.resize((img.width//2, img.height//2))  # simulamos baja resolución

sr_img = rdn.predict(lr_img)
Image.fromarray(sr_img).save('frame_mejorado.jpg')
