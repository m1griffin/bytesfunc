"""The BytesFunc module provides high speed bytes and bytearray processing 
functions. These functions are patterned after the functions in the standard 
Python Itertools module together with some additional ones import other sources.
"""

from bytesfunc.bmax import bmax
from bytesfunc.bmin import bmin
from bytesfunc.bsum import bsum

from bytesfunc.eq import eq
from bytesfunc.ge import ge
from bytesfunc.gt import gt
from bytesfunc.le import le
from bytesfunc.lt import lt
from bytesfunc.ne import ne

from bytesfunc.ball import ball
from bytesfunc.bany import bany
from bytesfunc.findindex import findindex

from bytesfunc.and_ import and_
from bytesfunc.or_ import or_
from bytesfunc.xor import xor
from bytesfunc.lshift import lshift
from bytesfunc.rshift import rshift

from bytesfunc.invert import invert

import bytesfunc.simdsupport
