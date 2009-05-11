#!/usr/bin/python

import Image, ImageFont, ImageDraw, ImageChops, string

W = 19416
H = 12000
#W = 12944
#H = 8000

#IN = "mappedX-2500-50-50.txt"
IN = "mappedX-1000-50-50.txt"

#im = Image.new("L", (W, H), 255)
im = Image.new("RGBA", (W, H), (0,0,0))


# use a bitmap font
#font = ImageFont.load("/usr/share/fonts/liberation/LiberationSans-Italic.ttf")
#font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 25)
font = ImageFont.truetype("/u/turian/fonts/Vera.ttf", 96)
#font = ImageFont.truetype("/home/joseph/fonts/Vera.ttf", 128)

#draw = ImageDraw.Draw(im)
#draw.text((10, 10), "hello", font=font)

minx = 0
maxx = 0
miny = 0
maxy = 0
for l in open(IN):
    (w, x, y) = string.split(l)
    x = float(x)
    y = float(y)
    if minx > x: minx = x
    if maxx < x: maxx = x
    if miny > y: miny = y
    if maxy < y: maxy = y

minx -= 10
miny -= 10
maxx += 10
maxy += 10


alpha = Image.new("L", im.size, "black")

for (idx, l) in enumerate(open(IN)):
    (w, x, y) = string.split(l)
    x = float(x)
    y = float(y)
#    print x, minx
#    print 1. * (x - minx) / (maxx - minx)
#    print y, miny
#    print 1. * (y - miny) / (maxy - miny)
    x = 1. * (x - minx) / (maxx - minx) * W
    y = 1. * (y - miny) / (maxy - miny) * H
#    draw.text((x, y), w, fill=255, font=font)


# Make a grayscale image of the font, white on black.
    pos = (x, y)
    imtext = Image.new("L", im.size, 0)
    drtext = ImageDraw.Draw(imtext)
    drtext.text(pos, w, font=font, fill=128)

# Add the white text to our collected alpha channel. Gray pixels around
# the edge of the text will eventually become partially transparent
# pixels in the alpha channel.
#    alpha = ImageChops.lighter(alpha, imtext)
    alpha = ImageChops.add(alpha, imtext)
        
# Make a solid color, and add it to the color layer on every pixel
# that has even a little bit of alpha showing.
#    solidcolor = Image.new("RGBA", im.size, "#ffffff")
#    immask = Image.eval(imtext, lambda p: 120 * (int(p != 0)))
#    im = Image.composite(solidcolor, im, immask)
#    draw.text((x, y), w, fill=0, font=font)

    print "Rendered word #%d" % idx
#    if idx % 100 == 99:
#        break

# Add the alpha channel to the image, and save it out.
im.putalpha(alpha)
#im.save("transtext.png", "PNG")
im.save("render.png")

