#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "Thomas Pietrzak"
__copyright__ = "Copyright 2021, Thomas Pietrzak"
__credits__ = ["Thomas Pietrzak"]
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Thomas Pietrzak"
__email__ = "thomas.pietrzak@gmail.com"
__status__ = "Production"

from activity import *
from tcxparser import *

# Defining main function 
def main(): 
  act = Activity()
  print('Loading Garmin activity')
  TCXParser.loadGarmin(act, 'garmin.tcx')
#  print('Loading Tacx activity')
#  TCXParser.loadTacx(act, 'tacx.tcx')
  print('Loading Zwift activity')
  TCXParser.loadZwift(act, 'zwift.tcx')
  print('Sort Track Points')
  act.sort()
  print('Writing merged file')
  TCXParser.writeTCX(act, 'combined.tcx')
  print('Done')

# Using the special variable  
# __name__ 
if __name__=="__main__": 
  main() 