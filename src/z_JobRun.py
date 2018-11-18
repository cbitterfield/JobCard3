#!/usr/bin/env python3
'''
newmodule -- shortdesc

newmodule is a description

It defines classes_and_methods

@author:     Colin Bitterfield

@copyright:  2017 Edge Intereactive. All rights reserved.

@license:    license

@contact:    colin@bitterfield.com
@deffield    updated: 08/14/2018
'''
#===============================================================================
# Import 
#===============================================================================

import os
from card_prep import Card
from card_prep import RunCard
from card_prep import GetCardInfo
import test
import z_Components
import yaml
import subprocess
import os
import sys
import argparse
import shlex
import datetime
import importlib

#===============================================================================
# Overrides (use absolute path for override)
#===============================================================================
LEVEL = 'DEBUG'
NOEXEC = 'TRUE'
LOG_DIR = '/edge/Logs'
RUN_DIR = '/edge/RunDir'
ASSEMBLE_DIR = '/edge/Assembly'
PRODUCT_DIR = '/edge/Assembly'
SCRATCH_DIR = '/edge/Scratch'
CONFIG = '/edge/Jobcard3/config/config.yaml'


#===============================================================================
# Command Line Arguements
# Requires a minimum of 1 (jobcard filename)
#===============================================================================

try:
    # Setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config", dest="config", default=CONFIG, help="use config file, default is config.yml in working dir")
    parser.add_argument("-l","--log", action="store", default=LOG_DIR, help="log_dir is where all of the job logs are written to. CONSOLE = console output" )
    parser.add_argument("-r","--run", action="store", default=RUN_DIR, help="run_dir is where the validate runcards are written to." )
    parser.add_argument("-a","--assemble", action="store", default=ASSEMBLE_DIR, help="assemble_dir is the output location for all components" )
    parser.add_argument("-s","--scratch", action="store", default=SCRATCH_DIR, help="scratch_dir = where temp files are written; there are considered deleteable" )
    parser.add_argument("-j","--jobcard", action="store", help="task card" )
    parser.add_argument("-n","--noexec", action="store_true", help="Do not run commands on the OS; echo the command on the OS only" )
    parser.add_argument("-t","--validate", action="store_true", help="Test/Validate the Jobcard and exit" )
    parser.add_argument("-d","--debug", action="store", default=LEVEL, help="set the debug level [INFO, WARN, ERROR, CRITICAL, DEBUG" )
    parser.add_argument("-xp","--noproduct", action="store_true", help="Don't build products" )
    parser.add_argument("-xc","--nocomponent", action="store_true", help="Don't build components" )
    parser.add_argument("-sc","--signcomponent", dest="single", action="store", help="Only work on a single component, adds -xp by default")
    

    # Process arguments
    args = parser.parse_args()
    noexec = args.noexec

except Exception as e:
    sys.exit(1)

if args.jobcard == None:
    print('Required argument is missing, no Jobcard use -h to get a list of argements')
    sys.exit(1)
    
else:
    JOBCARD = args.jobcard
    JOBNAME = os.path.basename(JOBCARD).split('.')[0]
    

    

#===============================================================================
# Setup  Logging
#===============================================================================
import logging
import logging.config 
logger = logging.getLogger('Main')

if args.log == 'CONSOLE':
    logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=LEVEL)

elif args.log != LOG_DIR:
    # We got something from the command line
    # If it is a directory; use jobcard prefix . log for a filename and write
    # If it is not a directory; assume it to be a file and write to it.
    if os.path.isdir(args.log):
        logging.basicConfig(filename=args.log + '/' + str(JOBNAME) + '.log', format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=args.debug)
    else:
        logging.basicConfig(filename=args.log, format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=args.debug)



logger.info('Starting JobRun {}'.format(JOBNAME))
logger.debug('Command Line Argements: {}'.format(args))
from carddeck import CardViewer
#===============================================================================
#Main Code Base
#===============================================================================

# Load Initial Cards
config_card = CardViewer('Config')
config_card.load(CONFIG)
display_config = dict(config_card.fullhouse())
jobcard = CardViewer('JobCard')

jobcard.load(JOBCARD)

 
# Create Running Card
jobrun = CardViewer('Running')
jobrun.merge(config_card.fullhouse())
jobrun.merge(jobcard.fullhouse())
jobrun.write(args.run + '/' + JOBNAME + '.yaml')
jobrun.info()
jobrun.types('component')
 
# Validate the Run card
# Validation includes extending all of the paths and making sure each component and product
# have all of the paths extended and all files needed exist.
 
print('\n{}'.format(dict(jobrun.fullhouse())))
SUCCESS = jobrun.validate()
if SUCCESS:
    logger.info('Card Validated')
else:
    logger.error('Card Failed Validation')
jobrun.write(args.run + '/' + JOBNAME + '.yaml')
jobrun.write(args.run + '/' + JOBNAME + '.yaml')