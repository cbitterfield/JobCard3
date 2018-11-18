'''
Created on Nov 12, 2018

@author: colin bitterfield

Main Class for Using Cards
'''
#===============================================================================
# Required Libraries
#===============================================================================
import os
import logging
import yaml
import os
import collections


#===============================================================================
# Shared Functions
#===============================================================================

def deep_get(dictionary, keys, default=None):
            return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split(","), dictionary)

def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
    return True

def is_value(dictionary, test_value):
    SUCCESS=False
    for key,value in dictionary.items():
        if value == test_value:
            SUCCESS = True
    return SUCCESS
            

def codec_exists(*args):
    codec_name = args[0]
    return True

#===============================================================================
# Global Variables
#===============================================================================



class CardViewer(object):
    '''
    Card takes a dictionrary based card and manipulates it for easy of use 
    '''
    # Number of card decks that exist
    deck = 0


    def __init__(self, *args):
        '''
        Initialization allows for the creation of a blank card or a card populated from a dictionary.
        First parameter is the card name.
        If a second parameter is provided, a dictionary is expected to load into the card.
        
        '''
        
        if len(args) in range(1,2):
            if len(args) == 1:
                self.cardname = args[0] 
                blankcard = {self.cardname:'system created {}'.format(args[0])}
                self.card = dict(blankcard)
            
            if len(args) == 2:
                self.cardname = args[0] 
                self.card = dict(args[1])
                
            CardViewer.deck += 1        
            self.logger = logging.getLogger(__name__ + ":" +str(self.cardname))
            self.logger.debug('Created card #{0} named {1}'.format(CardViewer.deck,self.cardname))
        
        
        else:
            self.logger = logging.getLogger(__name__ + ":" + 'ERROR')
            self.logger.debug('Failed to create Card, wrong number of arguments, {0} passed :{1}'.format(len(args),args))
        
           
    
    def info(self, *args):
        '''
        Returns Card Name, Number and DICT of card
        If any arguements are passed, then only the dictionary is returned
        '''
        if len(args) == 0:
            self.logger.debug('Information: card #{0} named {1} Dict: {2}'.format(CardViewer.deck,self.cardname,self.card))
            return CardViewer.deck,self.cardname,self.card
        else:
            self.logger.debug('Returning only DICT {0}'.format(self.card))
            return self.card
    
    def load(self,*args):
        '''
        Takes one parameter
        fully qualified filename and extension
        Loads YAML formatted file into card
        '''
        if len(args) == 1:
            loadfile = args[0]
            self.logger.info('Loading Card from {0}'.format(loadfile))
        
            if os.path.isfile(loadfile):
                self.logger.debug('File {0} exists'.format(loadfile))
                getfile = open(loadfile,'r')
                temp_dict = yaml.load(getfile)
                self.card.update(temp_dict)
                self.logger.debug('Loading Card from {0} received {1}'.format(loadfile,temp_dict))
                getfile.close()
                self.logger.info('File loaded sucessfully')
                return True
            else:
                self.logger.error("Failed to load file")
                return False
        else:
            self.logger.debug('Failed to load Card, wrong number of arguments, {0} passed :{1}'.format(len(args),args))
            
    def write(self,*args):
        '''
        takes one parameter
        fully qualified filename and extension
        writes the DICT to YAML formatted card
        writes pretty and ordered
        returns True|False, ERROR_MESSAGE
        '''
        if len(args) == 1:
            writefile = args[0]
            if os.path.isdir(os.path.dirname(writefile)):
                
                try:
                    self.logger.info('Opening file {} for writing'.format(writefile))
                    outfile = open(writefile,'w',1)
                    yaml.dump(dict(self.card),outfile,default_flow_style=False, indent=4)
                    outfile.close()
                    self.logger.info('Success Card exported to {}'.format(writefile))
                    
                except Exception as Error:
                    self.logger.error('Failed to write file: {}'.format(writefile)) 
                    return False      
                return True
            
            else:
                self.logger.error('Directory for output does not exisst {}'.format(os.path.dirname(writefile)))
                return False
        else:
            self.logger.debug('Failed to write Card, wrong number of arguments, {0} passed :{1}'.format(len(args),args))
            return False
    
    def keys(self):
        self.logger.info('Return all keys in Card dictionary {}'.format(self.card.keys()))
        return self.card.keys()

class CardConfig(CardViewer):
    '''
    Builds a running configuration dictionary from itself and returns that dictionary
    '''
    def build(self):
        for section in self.keys():
            self.logger.debug('Checking section {} for action'.format(section))
            # Sections that start with uppercase letter are ignored and system generated
            if section[0].islower():
                try:
                    action = self.card[section]['action']
                except Exception as error:
                    action = None
            
                if action == 'expand':
                    self.logger.info('Section {0} action {1}'.format(section,action))
                    
    
    