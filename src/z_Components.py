'''
Created on Aug 15, 2018

@author: colin
'''


class Main():
    def __init__(self,config,jobcard):
        self.config = config
        self.jobcard = jobcard
       
    def info(self):
        print*('Components v 1.0')
        
    def create(self,**kwargs):
        pass
    
    def exists(self,**kwargs):
        pass
    
    def ignore(self,**kwargs):
        pass
        
class BoxCover(Main): 
    def __init__(self,jobcard,config,**kwargs):
        super().__init__()
    
    def info(self):
        print ('BoxCover v 1.0')
        print ('Config:{}'.format(Main.config))
        
    def create(self,**kwargs):
        pass
    
class Images(Main):
    def info(self):
        print ('Images v 1.0')
        print ('Config:{}'.format(Main.config))
        
    def create(self,**kwargs):
        pass
 
class Video(Main):
    def info(self):
        print ('Videos v 1.0')
        print ('Config:{}'.format(Main.config))
        
    def create(self,**kwargs):
        pass   

class Text(Main):
    def info(self):
        print ('Text v 1.0')
        print ('Config:{}'.format(Main.config))
        
    def create(self,**kwargs):
        pass 
