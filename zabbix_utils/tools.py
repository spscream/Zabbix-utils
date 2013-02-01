#!/usr/bin/python
import colorsys
import sys
from random import random

def errmsg(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(-1)

def getColor(size, n):
    """
    Takes size of color palette and number of color in palette"
    Returns "%r%g%b"
    """

    #hsvColor = (n*1.0/size, 0.7, 0.7)
    v_step = 0
    s_step = 0
    h_step = 0
    h_size = 7
    if n > h_size:
        h_step += n/h_size
        s_step += n/h_size
        v_step += n/h_size

    hsvColor = (n*1.0/size, 0.9, 0.7)
    rgbColor = colorsys.hsv_to_rgb(*hsvColor)
    r, g, b = [hex(int(x*255))[2:] for x in rgbColor]
    color = "%s%s%s" % (r,g,b)
    return color

def sorted_alphanum(l): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
