import numpy as np
import math

def makeUnitVector(vector):
    mag = magnitude(vector)
    if (mag != 0):
        return vector / mag
    else:
        return np.zeros(3, dtype=float)


def magnitude(vector):
    return np.sqrt(vector.dot(vector))

def angleBetween(u, v):
    bottom = magnitude(u) * magnitude(v)
    if (bottom != 0):
        # print "udotv " + str(u.dot(v))
        # print "bottom " + str(bottom)
        value = min(1, math.fabs(u.dot(v) / bottom))
        # print "value " + str(value)
        rad = math.acos(value)
        return math.degrees(rad)
    else:
        return 0

