#!/usr/bin/python

import Image, ImageFont, ImageDraw, string, PSDraw

W = 3200
H = 2400
IN = "mappedX-2500-50-50.txt"

box = (1*72, 2*72, 7*72, 10*72)
ps = PSDraw.PSDraw()
ps.begin_document("Ronan + Jason embeddings")
#ps.setfont("HelveticaNarrow-Bold", 36)

im = Image.new("L", (W, H))
#for w in range(W):
#    for h in range(H):
#        im.putpixel((w, h), 255)
ps.image(box, im, 75)
ps.rectangle(box)
#im = Image.new("L", (W, H))


# use a bitmap font
#font = ImageFont.load("/usr/share/fonts/liberation/LiberationSans-Italic.ttf")
font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 25)

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

for l in open(IN):
    (w, x, y) = string.split(l)
    x = float(x)
    y = float(y)
#    print x, minx
#    print 1. * (x - minx) / (maxx - minx)
#    print y, miny
#    print 1. * (y - miny) / (maxy - miny)
    x = 1. * (x - minx) / (maxx - minx) * box[2]
    y = 1. * (y - miny) / (maxy - miny) * box[3]
#    ps.text((x, y), w)
    ps.text((100, 200), w)
#    draw.text((x, y), w, fill=0)

#im.save("render.eps")
ps.end_document()

