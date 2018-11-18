'''
Created on Aug 23, 2018

@author: colin
'''

import os
import logging
import yaml
import os
import collections
from collections import OrderedDict
from functools import reduce 
import subprocess
import re

NOEXEC = False


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
            
        
    
      
class CardViewer:
    '''
    Card takes a dictionrary based card and manipulates it for easy of use 
    '''
    deck = 0

    def __init__(self, *args):
        '''
        takes 2 parameters
        param 1 = DICT/CARD
        param 2 = Card Name
        Returns False if error condition
        '''

        SUCCESS = True
        if len(args) == 2:     
            cardin = args[0]
            self.card = dict(cardin)
            self.cardname = args[1]
            CardViewer.deck += 1            
        elif len(args) == 1:
            self.cardname = args[0] 
            blankcard = {self.cardname:'system initialized'}
            self.card = dict(blankcard)  
             
            CardViewer.deck += 1        
        else:
            self.card = None
            self.cardname = None
            SUCCESS = False
        if not SUCCESS:
            self.logger.debug('Failed to create Card')    
        self.logger = logging.getLogger(__name__ + ":" +str(self.cardname))   
        self.logger.debug('Created card #{0} named {1}'.format(CardViewer.deck,self.cardname))
        
        
    
    def info (self):
        '''
        Returns Card Name, Number and DICT of card
        '''
        self.logger.debug('card info: Name {0} Number {1} DICT: {2}'.format(self.cardname, CardViewer.deck,self.card))
        return self.cardname, CardViewer.deck,self.card
        
    def fullhouse(self,*args):
        '''
        Return the dict value if nothing provided.
        If any argument provided return the card's name
        '''
        self.logger.debug('card info: DICT: {0}'.format(self.card))
        if len(args) > 0:
            return self.cardname
        else:
            return self.card 
        
        
    def get(self,*args):
        '''
        get a value from any level of the dict
        takes single argument which is 
        dict with each level seperated by ","
        '''
        SUCCESS = True
        ERROR_MESSAGE = 'Success'
        if len(args) == 1:
            iskey = args[0]
            
            value = deep_get(self.card,iskey,default=False)
            if value:
                self.logger.debug('Key {0} exists'.format(iskey))
                self.logger.debug("Value {}".format(value))
            else:
                self.logger.debug('Key {0} does not exist'.format(iskey))
                SUCCESS = False
        else:
            SUCCESS = False
            ERROR_MESSAGE = 'Wrong Number of parameters'
            self.logger.error(ERROR_MESSAGE)
        if SUCCESS:
            return value
        else:
            return False
    
    
    def add(self,*args):
        ''' 
        adds a new key and value pair to card
        takes two parameters
        key (with hierchy seperated by ',')
        value (either string or DICT)
        returns True|False, ERROR_MESSAGE
        Fails if key already exists
        param 1 = primary key
        param 2 = DICT for primary key
    
        '''
        # Need to add logic to check if the key exists and produce error
        if len(args) != 2 and type(args[0]) == str and type(args[1]) == dict:
            self.logger.error('Wrong number of argements passed expected 2 received {}'.format(len(args)))
            return False
        else:
            self.card[args[0]] = args[1]
            self.logger.debug('Adding key {0} with value {1}'.format(args[0],args[1]))
            return True
        
    def delete(self,*args):
        ''' 
        Delete a key and associated values
        one parameter 
        key (with hierchy seperated by ',')
        returns True|False, ERROR_MESSAGE
        '''
        pass
    
    def merge(self,*args):
        '''
        Updates the current card with all of the values from the pass DICT
        Passed dict replaces current values
        takes two argements
        second arguement is "all or list of components"
        all will create shadow configs for all components that have a dot number after them
        for instance will create video.1 from video prior to the merge
        '''
        SUCCESS = True
        
        if len(args) == 2:
            if args[1].lowercase() == ('all'):
                self.logger.debug('Processing all components ')
                component_list = self.types('component')
                for component in component_list:
                    base_component = 
            
            else:
                component_list = args[1]
                self.logger.debug('Processing selected components: {}'.format(component_list)) 
                
        
        elif len(args) == 1:
            orig_card = dict(self.card)
            merge_card = dict(args[0])
            self.logger.debug('Merging {0} with {1}'.format(self.cardname,args[0]))
            dict_merge(orig_card,merge_card)
            self.card = dict(orig_card)
            
            
        else:
            SUCCESS = False
            self.logger.error('Wrong number of arguments passed args passed expected 1 or 2 received {0}'.format(len(args)))
            
        
        return SUCCESS
    
    
    
    def exist(self,*args):
        '''
        This checks if a "key exists" in the card.
        It does not look for a value
        returns True or False
        '''
        SUCCESS = True
        ERROR_MESSAGE = 'Success'
        if len(args) == 1:
            iskey = args[0]
            
            value = deep_get(self.card,iskey,default=False)
            if value:
                self.logger.debug('Key {0} exists'.format(iskey))
                self.logger.debug("Value {}".format(value))
            else:
                self.logger.debug('Key {0} does not exist'.format(iskey))
                SUCCESS = False
        else:
            SUCCESS = False
            ERROR_MESSAGE = 'Wrong Number of parameters'
            self.logger.error(ERROR_MESSAGE)
        return SUCCESS
    
    def types(self,*args):
        '''
        return a list of type keywords
        takes 1 argument = type
        '''
        SUCCESS = True
        key_list = []
        
        if len(args) == 1:
            self.logger.debug('TYPES:Looking for types {}'.format(args[0]))
            for each in self.card.keys():
                self.logger.debug('Checking Key {}'.format(each))
                self.logger.debug(type(self.card[each]))
                if type(self.card[each]) == dict:
                    key_type = self.card[each]['type'] if 'type' in self.card[each] else None
                    self.logger.debug('TYPES: key{0} type {1}'.format(each,key_type))
                    if 'type' in self.card[each].keys() and self.card[each]['type'] == args[0]:
                        self.logger.debug('Found type {}'.format(self.card[each]['type']))
                        key_list.append(each)
                        
                else:
                    self.logger.warn('No type found in key')
                
#             if len(key_list) == 0:
#                 self.logger.warn('No matching keys found')
#                 SUCCESS = False
            else:
                self.logger.debug('TYPES: return list {}'.format(key_list))
                return key_list    
            
        else:
            SUCCESS = False
            self.logger.error('Wrong number of argements passed expect 1 got {}'.format(len(args)))
        return SUCCESS 
        
    def write(self,*args):
        '''
        takes one parameter
        fully qualified filename and extension
        writes the DICT to YAML formatted card
        writes pretty and ordered
        returns True|False, ERROR_MESSAGE
        '''
        SUCCESS = True
        ERROR_MESSAGE = 'Success'
        writefile = args[0]
        
        try:
            self.logger.debug('Opening file {} for writing'.format(writefile))
            outfile = open(writefile,'w',1)
            yaml.dump(dict(self.card),outfile,default_flow_style=False, indent=4)
            outfile.close()
            self.logger.debug('Card exported to {}'.format(writefile))
            
        except Exception as Error:
            SUCCESS = False
            self.logger.error('Failed Open file')       
        return SUCCESS
    
    def load(self,*args):
        '''
        Takes one parameter
        fully qualified filename and extension
        Loads YAML formatted file into card
        '''

        loadfile = args[0]
        if os.path.isfile(loadfile):
            self.logger.debug('File {0} exists'.format(loadfile))
            getfile = open(loadfile,'r')
            temp_dict = yaml.load(getfile)
            self.card.update(temp_dict)
            self.logger.debug('Loading Card from {0} received {1}'.format(loadfile,temp_dict))
            getfile.close()
            return True
            
        else:
            self.logger.error("Failed to load file")
            return False
    
    def validate(self):
        '''
        Validate the card; extend the paths; verify all sources.
        Return true or false as a return code.
        '''
        def return_volumes(master_vol, check_dir):
            '''
            Take a path and look for all volumes on the path.
            Return a list of volumes found
            '''
            SUCCESS = False
            fq_dir = check_dir
            vol_ids = {}
            self.logger.debug('Checking if {0} is a directory for master vol: {1}'.format(fq_dir,master_vol))
            if os.path.isdir(fq_dir):
                self.logger.debug('{0} is a directory'.format(fq_dir))
                check_list = os.listdir(fq_dir)
                for vol_dir in check_list:
                    if os.path.isdir(check_dir):
                        # Check if a VOLID [A-Z]6-[A-Z]6
                        self.logger.debug('Checking if  {0} contains a vol_id'.format(vol_dir))
                        vol_results = re.findall( r'^[A-Z][A-Z0-9]{5}-[A-Z0-9]{6}', vol_dir)
                        self.logger.debug('Results from test {}'.format(vol_results))
                        if vol_results:
                            self.logger.debug('{} matches vol_id parameters'.format(vol_results))
                            SUCCESS = True
                            self.logger.debug('{'+ str(vol_results[0]) + ' : ' + str(master_vol) + '}')
                            vol_ids.update({vol_results[0] : check_dir})
                            
                    else:
                        self.logger.debug('This is not a directory {}'.format(vol_dir))
            
            else:
                self.logger.debug('{} is not a directory'.format(fq_dir))
            
            
            
            
            if SUCCESS:
                return vol_ids
                self.logger.debug('Results returned: {}',format(vol_ids))
            else:
                return SUCCESS
        def expand_source(source_in, volume):
            '''
            Returns an absolute path from a relative source.
            If produce Source = Source, If exists Source = Finished
            paths that start with / are already absoute
            paths that start with Vol_Ids are expanded
            paths that start with anything else start from Master Volume top level
            all paths are validated to exists
            returns absolute path or False if bad value
            '''
            absolute_path = False
            src_in = source_in
            source_header = re.findall( r'^[A-Z][A-Z0-9]{5}-[A-Z0-9]{6}', src_in.split('/')[0])
            self.logger.debug('EXPAND:checking src: {0} on volume [{1}]'.format(source_in,volume))
            #Step 1; get the first character
            if source_in[0] == '/':
                self.logger.debug('EXPAND: source path is absolute')
                if os.path.isdir(source_in):
                    check_source = source_in
                     
            
            # Step 2: Is the first part of the path a VOLUME ID
            # 6 Alpha dash 6 Alpha
               
            if source_header:
                self.logger.debug('EXPAND: source path {0} is a volume ID {1}'.format(source_in, source_header))
                check_source = '/'
                if type(self.card['volume_id'][volume]) == dict:
                    src_head = str(source_header[0])
                    if src_head in self.card['volume_id'][volume]:
                        self.logger.debug('EXPAND: VOL found in a dictionary lookup {}'.format(source_in))
                        check_source = str(self.card['volume_id'][volume][src_head]) + '/' + str(source_in) 
                     
                     
                    self.logger.debug('EXPAND:Check source src {} '.format(check_source)) 
                else:
                    check_source = self.card['volume_id'][volume] + '/' + source_in
                    self.logger.debug('Source {}  '.format(check_source))
                     
                 
              
            else:
                check_source = str(self.card['volume_id'][volume]) + '/' + source_in
                  
            self.logger.debug('EXPAND:Check if source src {} exists'.format(check_source))    
            
            # Check if path exists
            
            if os.path.exists(check_source):
                self.logger.debug('EXPAND:Source {} exists '.format(check_source))
                absolute_path = check_source
            else:
                absolute_path = False
                self.logger.error('EXPAND:Source does not exist: FAILED on {}'.format(check_source))
            
            return absolute_path
               
            
            
            
            
             
        SUCCESS = True   
            
        sections = ['program', 'codecs', 'volumes', 'component', 'product']
        sections = ['program', 'codecs','volumes','component']
        working_card = dict(self.card)
        # Do not change the order (volumes must validated before component and product
        for section in sections:
            section_list = self.types(section)
            self.logger.debug('Section {0}, List = {1}'.format(section,section_list))
            
            if section == 'program':
                self.logger.debug('Validating Program Section -- {}'.format(section_list))
                for each_section in section_list:
                    self.logger.debug('Checking section {}'.format(each_section))
                    for key,value in working_card[each_section].items():
                        self.logger.debug('Validating program {0} can be found'.format(key))
                        FOUND = False
                        for each_item in working_card[each_section][key].split(','):
                            self.logger.debug('Is the program located at {}'.format(each_item))
                            if os.path.isfile(each_item + '/' + key):
                                self.logger.debug('Found')
                                #Update the card information
                                self.card[each_section][key] = each_item + '/' + key
                                FOUND = True
                                break
                        if not FOUND:
                            self.logger.warn('Program {} not found in search path'.format(key))
            
            if section == 'codecs':
                self.logger.debug('Validating Codecs Section -- {}'.format(section_list))
                # We only need to validate encoder, decoder, and accelerator at this time; later we may need to set the # of threads for performance
                # based on the number of cpus
                #
                validate_set = ['mp4_encode','mp4_decode','mp4_simple','mp4_jpeg','mp4_accel']
                for each_section in section_list:
                    self.logger.debug('Checking section {}'.format(each_section))
                    for key,value in working_card[each_section].items():
                        if key in validate_set:
                            self.logger.debug('Validating Codec {0} : {1} exists as a method in ffmpeg'.format(key,value))
                            check_list = value.split(',')
                            if len(check_list) == 0:
                                SUCCESS=False
                                break
                            else:
                                for codec in check_list:
                                    self.logger.debug('Checking if FFMPEG supports {}'.format(codec))
                                    if 'accel' in key:
                                        # hwaccelerator
                                        self.logger.debug('Checking if FFMPEG supports hardware acceleration {}'.format(codec))
                                        CMD = str(self.card['programs']['ffmpeg']) + ' -hide_banner -hwaccels'
                                        CMD_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        stdoutdata, stderrdata = CMD_result.communicate()
                                        response = stdoutdata.decode(encoding="utf-8").splitlines()
                                        if codec in response:
                                            # Set value in card
                                            SUCCESS = True
                                            self.logger.debug('hardware accelleration {} enabled'.format(codec))
                                     
                                            self.card[each_section][key] = codec
                                            break
                                        else:
                                            self.logger.warn('hardware accelleration {} not available'.format(codec))
                                            self.card[each_section][key] = None
                                            SUCCESS = True
                                            
                                        
                                    elif 'decode' in key:
                                        #Decoder
                                        self.logger.debug('Checking if FFMPEG supports {} decoding'.format(codec))
                                        CMD = str(self.card['programs']['ffmpeg']) + ' -h decoder='+codec
                                        CMD_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        stdoutdata, stderrdata = CMD_result.communicate()
                                        response = stdoutdata.decode(encoding="utf-8").splitlines()[0]
                                        if 'Decoder' in response:
                                            # Set value in card
                                            SUCCESS = True
                                            self.logger.debug('decoder {} enabled'.format(codec))
                                     
                                            self.card[each_section][key] = codec
                                            break
                                        else:
                                            self.logger.error('decoder  {} not available'.format(codec))
                                            self.card[each_section][key] = 'Not Found'
                                            SUCCESS=False
                                        
                                    else:
                                        #Encoder
                                        self.logger.debug('Checking if FFMPEG supports {} encoding'.format(codec))
                                        CMD = str(self.card['programs']['ffmpeg']) + ' -h encoder='+codec
                                        CMD_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        stdoutdata, stderrdata = CMD_result.communicate()
                                        response = stdoutdata.decode(encoding="utf-8").splitlines()[0]
                                        if 'Encoder' in response:
                                            # Set value in card
                                            SUCCESS = True
                                            self.logger.debug('encoder {} enabled'.format(codec))
                                     
                                            self.card[each_section][key] = codec
                                            break
                                        else:
                                            self.logger.error('encoder  {} not available'.format(codec))
                                            self.card[each_section][key] = 'Not Found'
                                            SUCCESS=False
                                        
                                    self.logger.debug('Using command {} to test'.format(CMD))
                                    
            if section == 'volumes':
                name_volume_section = 'volume_id'
                self.logger.debug('Validating Volume Section -- {}'.format(section_list))
                # This creates a new section called: 'volume_id'
                self.card[name_volume_section] = {}
                for check_vol, check_value in self.card[section].items():
                    self.logger.debug('Checking volume {0} path {1}'.format(check_vol,check_value))
                    if not check_vol == 'type':
                        if ',' in check_value:
                            volid_set = {}
                            self.logger.debug('Expanding selection {0}'.format(check_value))
                            for each_volume in check_value.split(','):
                                full_dir = self.card['job_defaults']['mount_point'] + '/' + each_volume
                                self.logger.debug('Checking {0} on [{1}]'.format(each_volume,full_dir))
                                volid_results = return_volumes(check_vol,full_dir)
                                if volid_results:
                                    self.logger.debug('vol_ids found {}'.format(volid_results))
                                    volid_set.update(volid_results)
                            dict_merge(self.card, {name_volume_section : { check_vol :volid_set}})
                        else:
                            full_dir = self.card['job_defaults']['mount_point'] + '/' + check_value
                            if os.path.isdir(full_dir):
                                self.logger.debug('Making sure the directory is valid {}'.format(full_dir))
                                self.logger.debug('Adding Volume {0} to list'.format(check_vol))
                                dict_merge(self.card, {name_volume_section: {check_vol:full_dir}})
                            else:
                                self.logger.error('Directory {} not found'.format(full_dir))
                                SUCCESS=False
                
                
                
            if section == 'component':
                components =  self.types('component')
                self.logger.debug('Validating Component Section -- {}'.format(section_list))
                for valid_component in components:
                    
                    if len(valid_component.split('.')) == 2:
                        self.logger.debug('Component {} may have more than one entry'.format(valid_component))
                        # Merge base component with numbered component
                        print('Component:{}'.format(valid_component))
                        base_dict = self.card[valid_component.split('.')[0]]
                        print(base_dict)
                        new_dict = self.card[valid_component]
                        print(new_dict)
                        dict_merge(base_dict, new_dict)
                        print(self.card.pop(valid_component))
                        print('New {}'.format(base_dict))
                        self.card.update({valid_component: base_dict})
                        print(self.card)
                        self.write('/edge/RunDir/test1.yaml')
                        
                    self.logger.debug('Validating Component {}'.format(valid_component))
                    comp_action = self.card[valid_component]['action'] if 'action' in self.card[valid_component] else False
                    self.logger.debug('Component {} is {}'.format(valid_component,comp_action))
                    # If action is produce or exists further validate
                    if comp_action == 'produce' or comp_action == 'exists':
                        for setting,setting_value in self.card[valid_component].items():
                            self.logger.debug('Check each setting {0} for value {1}'.format(setting,setting_value))
                            if setting == 'src':
                                self.logger.debug('Expanding src to absolute path {}'.format(setting_value))
                                volume = 'source' if comp_action == 'produce' else 'finished'
                                src_header = setting_value.split('/')[0] 
                                self.card[valid_component]['src'] = expand_source(setting_value, volume)
                            
                            if setting == 'template':
                                self.logger.debug('Expanding template to absolute path {}'.format(setting_value))
                                volume = 'source' if comp_action == 'produce' else 'finished'
                                src_header = setting_value.split('/')[0] 
                                self.card[valid_component]['template'] = expand_source(setting_value, volume)
#                         
                                
                        
                
            
            if section == 'product':
                self.logger.debug('Validating Product Section -- {}'.format(section_list))
                
        
        
        
        return SUCCESS
        