'''
Created on Nov 12, 2018

@author: colin
'''
#===============================================================================
# Setup  Logging
#===============================================================================
import logging
import logging.config 
logger = logging.getLogger('Main')

LEVEL = 'INFO'

logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=LEVEL)




from CardStack import CardViewer
from CardStack import CardConfig

config = CardConfig('config')
message = config.info()
load = config.load('/Users/colin/Documents/eclipse-workspace/JobCard3/config/config.yaml')
write = config.write('/tmp/output.yaml')

print(config.keys())
build = config.build()