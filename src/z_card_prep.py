'''
Created on Aug 21, 2018

@author: colin
'''
### 
# All classes return two additional valuesvalues Error & Error Message
# 
# 
class Card:
    '''
    manipulate card and config information
    '''
    answer_card = {}
    data_card = {}
    eval_card = []
    import logging
    logger = logging.getLogger(__name__)
    
    def __init__(self, *args):
        '''
        Initialize datacard
        '''
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Length of Arguements {}".format(len(args)))
        if len(args) > 0:
            ##print ('ARG LENGTH = {}'.format(len(args)))
            for each_card in range(len(args)):
                logger.debug("Adding DICT to list entry {}".format(each_card))
                Card.eval_card.append(args[each_card])
                logger.debug('DICT = {}'.format(Card.eval_card[each_card]))
        if len(args) == 0:
            logger.error('Wrong number of values passed')
        
    def info(self,*args):
        '''
        Takes Zero or Multiple Keys
        If 0; returns the initialized card in totality
        If > 1, return value associated with nested key
        Limit 3 key levels
        Get info about a card/config
        returns: Value, Error
        Arg0 = Number of Card to Eval
        Arg1 = Key to return value of 
        '''
        import logging
        logger = logging.getLogger('info')
        from functools import reduce 
        def deep_get(dictionary, keys, default=None):
            return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split(","), dictionary)

        # If args = 1, then just get the value from the first dict
        # If args > 1 then get the value from the second dict

        Error = False
        Error_Message = ''
        Value = {}    
            
        
        if len(args) == 0:
            logger.info(len(Card.eval_card))
            Value = len(Card.eval_card)
            logger.info('Cards Inititalized = {}'.format(len(Card.eval_card)))
            
        elif len(args) == 2:
            Value = deep_get(Card.eval_card[args[1]],args[0],None)
        else:
            Value = 'Error'
            Error = True
        if Error:    
            logging.error(Error_Message)
        logging.debug("DEBUG: {0} : {1} ".format(args,Card.data_card))
        logging.debug("Return Value: {0}, Error: {1}".format(Value,Error))           
        return Value, Error
    
    def get_list(self,*args):
        # Make an Array of z_Components and products
        '''
        Take a DICT and provide a TYPE
        Return a list of keys based on type
        Takes 2 values
        Value 1 = DICT from enabled list (value 0 to n)
        Value 2 = TYPE 
        '''
        import logging
        logger = logging.getLogger('get_list')
        myList = []
        logger.debug('Card: {}'.format(args[0]))
        logger.debug('Evaluating Card for Type: {}'.format(args[1]))
        
        myDict = int(args[0])
        
        logger.debug(Card.eval_card[myDict])
        for key in Card.eval_card[myDict].keys():
            
            myValue, myError = self.info(str(key) +',type',myDict)
            logger.debug('Evaluting Key: {0} Value: {1}'.format(key,myValue))
            if myValue ==  args[1]:
                logger.debug('Adding key {0} to list: {1}'.format(key,myList))
                myList.append(key)
            
            
                
        return myList   
        
    
    def get_masterkeys(self,*args):
        '''
        Takes 1 argument; which card to evaluate and provides list of master keys
        '''
        import logging
        logger = logging.getLogger(__name__)
        myList = []
        myDict = int(args[0])
        logger.debug('Card: {}'.format(args[0]))
        logger.debug('Evaluating Card for Master Keys: {}'.format(Card.eval_card[myDict]))
        myValue = Card.eval_card[myDict].keys() 
        logger.debug(myValue)                                                                                         
        return myValue
    
    def return_card(self,*args):
        import logging
        logger = logging.getLogger('return_card')
        myDict = args[0]
        return Card.eval_card[myDict]
     
    def locate_file(self,*args):
        '''
        Argument 1 = Name of File
        Argument 2 = Path to search seperated by colons
        Return FQ Filename + Error
        Searches in order of path stops on first occurence
        '''
        import logging
        import os
        logger = logging.getLogger('locate file')
        Error = True   
        if len(args) == 0 or len(args) > 2:
            return 'Error', True
        LIST = args[1]
        FILENAME = args[0]
        for eachpath in LIST:
            if os.path.isfile(eachpath + "/" + FILENAME):
                VALUE = eachpath + "/" + FILENAME
                Error = False
                return VALUE, Error
        return 'Error', Error
               
    
class RunCard(Card):
    '''
     Makes a consolidated RunCard from combining values and normalizing values
     Returns DICT, Error   
     
     Add's logic to make sure runcard contains all needed data for the processor to process
    '''
    
    def prepare_card(self,*args):
        '''
        Returns a complete runcard
        '''
        import os
        def find_fqpn(*args):
            findfile = args[0]
            findpath = args[1]
            for eachpath in findpath.split(':'):
                if os.path.isfile(eachpath + "/" + findfile):
                    return eachpath + "/" + findfile, False
            return 'Error',True   
        
         
        def eval_value(*args):
            Error = False
            first = args[0]
            second = args[1]
            
            logging.debug('Evaluate {0} v {1}'.format(first,second))
            
            if first == 'REQUIRED' and second == None:
                print ('Error in value {}'.format(args[0]))
                value = None
                Error = True
                
            
            if first == 'REQUIRED' and second is not None:
                value = second
            
            if first == 'OPTIONAL':
                value = second if second is not None else None
                
            
            if first is not 'REQUIRED' and first is not 'OPTIONAL':
                if second == None: 
                    logger.debug ("Use Config")
                    value=first
                else:
                    logger.debug("Use Jobcard")
                    value=second
            
                logger.debug('Eval: {0} {1} {2}'.format(args[0],args[1],value))
                
        
    
            return value,Error
        
        
        import logging
        logger = logging.getLogger('prepare_card')
        
        from collections import OrderedDict
        
        prepared_card = {}
        logger.debug('Preparing a RunCard')
        
        # Additional Logic
        # If a video is a going to be created and there is no boxcover, a boxcover is created automatically
        
        # If a Component doesn't have a numberic, a Zero will be added.
        # Goal is a RunCard is complete and without Errors.
        
        myRunCard = OrderedDict(self.return_card(1))
        myTempSection = {}
        myTempSubSection = {}
        Error = False
        
        for section in self.get_masterkeys(1):
        
            if '.' in section:
                section_major,section_minor = section.split('.')
            else:
                section_major = section
                section_minor = 0
                
            logger.debug('Evaluting Section: {}'.format(section))
            
            
            section_data, section_error = self.info(section_major,0) # Get config values
            job_data, job_error = self.info(section_major,1)
            logger.debug('Config: {}'.format(section_data))
            logger.debug('JobCard:{}'.format(job_data))
            if section_error == False and type(section_data) == dict:
                # We can now process a section
                for section_key in section_data.keys():
                    section_value, section_data_error = self.info(section + ',' + section_key,0)                    
                    if type(section_value) == dict:
                        # Process Subsections
                        logger.info('section_key {0}'.format(section_key))
                        if type(self.info(section_major + ',' + section_key,1)[0]) == dict:
                            for subsection_key, subsection_value in section_value.items():
                                logger.info('Subsection {0} Key: {1} Value: {2}'.format(section_key, subsection_key, subsection_value))
                                logger.info('JobCard Value: {0}'.format(self.info(section + ',' + section_key + ',' + subsection_key,1)[0]))
                                sub_first_value  = self.info(section_major + ',' + section_key + ',' + subsection_key,0)[0]
                                sub_second_value = self.info(section + ',' + section_key+ ',' + subsection_key,1)[0]
                                sub_results_value = eval_value(sub_first_value,sub_second_value)[0]
                                if sub_results_value == None:
                                    myRunCard[section][section_key].pop(subsection_key)
                                else:
                                    myRunCard[section][section_key][subsection_key] = sub_results_value
                        else:                            
                            logger.info('section {0} key {1} not processed'. format(section,section_key))
                            
                            
                    else:
                        first_value  = self.info(section_major + ',' + section_key,0)[0]
                        second_value = self.info(section + ',' + section_key,1)[0]
                        results_value = eval_value(first_value,second_value)[0]
                        if results_value == None:
                            myRunCard[section].pop(section_key)
                            logger.info('Results for section key {0} are {1} and deleted '.format(section_key,results_value))
                        else:
                            myRunCard[section][section_key] = results_value
                            logger.debug('Section: {0} JobCard Key: {1} Config Value: {2} JobCard Value: {3} Selected Value: {4}'.format(section_major,section_key,first_value,second_value,results_value ))
                        
        # Add some logic 
        # First add a section of programs
        list_of_programs, list_of_programs_error = self.info('programs',0)
        if list_of_programs_error is False:
            myRunCard['programs'] = list_of_programs   
            for each_program,each_path in list_of_programs.items():
                logger.debug('Path = {0} : {1}'.format(each_program,each_path))
                program_results, program_error = find_fqpn(each_program,each_path)
                if program_error:
                    return 'Error on getting programs ' + str(each_program), True
                else:
                    myRunCard['programs'][each_program] = program_results
                
                
        
        # Second add a section of master volumes for access
        list_of_volumes, list_of_volumes_error = self.info('volumes',0)
        if list_of_volumes_error is False:
            myRunCard['volumes'] = list_of_volumes
        
        # Build a dynamic list of volumes from the master set (right now, Source[1-3], Finished are sets.
        # Eventually we need to build the capability for Finished to have more than one Master Volume
        
        
        
        
        # Fourth Find which codec we want to use
        
        
        return myRunCard, Error

class GetCardInfo(Card):
    '''
    Processing card information
    Additional Tasks for manipulating RunCard info are included here.
    '''
    def make_list_volumes(self,*args):
        '''
        Pass a list of master volumes
        Return a list of volumes
        '''
        import logging
        import os, re
        logger = logging.getLogger('get_list_volumes')
        logger.info(args)
        Error = False
        Error_Message = 'Error:'
        volume_list = {}
        
        # Get MountPoint from runCard master volumes
        mount_point,mount_point_error = self.info('volumes,mount',2)
        if mount_point_error is False:
            logger.info('Mount point {0}'.format(mount_point))
        else:
            return Error_Message + 'Bad Mount Pount', True
        
        for master_volume in args:
            logger.debug('Master Volume = {}'.format(master_volume))
            master_volume_list, master_volume_list_error = self.info('volumes,' + master_volume,2)
            if master_volume_list_error is False:
                volume_list[master_volume] = {}
                for path_to_test in master_volume_list.split(':'):
                    logger.info('Test Master Volume {0} Volume {1} Path {2}'.format(master_volume,path_to_test,mount_point + "/" + path_to_test))
                    if os.path.isdir(path_to_test):
                        logger.info('Testing Path {0}'.format(path_to_test))
                            
        print(volume_list)             
        return volume_list, Error    