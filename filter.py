from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageOps

MAXPIX = 255
DELTA = 30
EPS = 0.0001

img = Image.open("test.jpg")
img.show() #before processing

img = img.filter(ImageFilter.DETAIL)
enh = ImageEnhance.Contrast(img).enhance(1.3) #30% more contrast
out = enh.filter(ImageFilter.BLUR)

x, y = enh.size 
eX, eY = x / 2, y / 2

'''
bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
draw = ImageDraw.Draw(enh)
draw.ellipse(bbox, fill = 128)
del draw
'''

n = 5
icons = [Image.open(str(im) + ".png").convert("RGBA") for im in range(1, n)]
icons = [icon.resize((enh.width // 4, enh.height // 4), Image.ANTIALIAS) for icon in icons]
icons[:2] = [im.convert("RGBA").rotate(-60) for im in icons[:2]]
icons[2:] = [im.convert("RGBA").rotate(30) for im in icons[2:]]
for i in range(1, n - 1, 2):
	icons[i] = ImageOps.mirror(icons[i])

cor = []
cor.append((0, 0, icons[0].width, icons[0].height))
cor.append((enh.width - icons[0].width, 0, enh.width, icons[0].height))
cor.append((0, enh.height - icons[0].height, icons[0].width, enh.height))
cor.append((enh.width - icons[0].width, enh.height - icons[0].height, enh.width, enh.height))

for i in range(n - 1):
	out.paste(icons[i], cor[i], icons[i]) #add moon

sn = Image.open("snow.png").convert("RGBA").resize((enh.width, enh.height))
enh.paste(sn, (0, 0, enh.width, enh.height), sn)

pixels = enh.load()
dpixels = out.load()
for j in range(enh.width):
	for i in range(enh.height):
		if (j - eX) ** 2 * eY ** 2 + (i - eY) ** 2 * eX ** 2 - eX ** 2 * eY ** 2 < EPS:
			r, g, b = [min(MAXPIX, c + DELTA) for c in pixels[j, i]]
			pixels[j, i] = (r, g, b)
		else:
			pixels[j, i] = dpixels[j, i]

enh.show() #with filter
enh.save("final.jpg")