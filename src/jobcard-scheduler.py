#!/usr/bin/env python3

#===============================================================================
# JobCard Scheduler for Dameons
#===============================================================================
 
import sys, time, os, datetime
from jobcard_daemon import daemon
from random import shuffle

 
 
#===============================================================================
# Set Variables Global
#===============================================================================
PIDFILE = '/tmp/jobcard.pid'
LOGFILE = '/tmp/jobcard.log'





 
class MyDaemon(daemon):
        def run(self):
            #===============================================================================
            # Set Variables
            #===============================================================================
            DELAY = 10 # Wait 15 minutes before checking again 
            NUMTHREADS = 4 # Allow 4 jobcards to run at the same time. 
            JOBDIR = "/edge/JobQueue/jobs"
            JOBERR = "/edge/JobQueue/errors"
            JOBLOG = "/edge/JobQueue/log"
            JOBCFG = "/edge/JobQueue/config/config.yaml"
            JOBCMD = "/edge/JobCard2/src/jobcard.py"
            
            
            run = 0
            jobqueue = []
            try:
                print('starting')
                counter = 0
                if os.path.isfile(LOGFILE):
                    log = open(LOGFILE,'a',1)
                else:
                    log = open(LOGFILE,'w',1)
                log.write('Job Scheduler - Starting services\n')  
            except Exception as e:
                print (e)
                
            while True:
                #===============================================================================
                # Get Time for timestamp
                #===============================================================================
    
                ts = time.time()
                sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
                log.write('{} Checking JobQueue: '.format(sttime))
                locklist = os.listdir(JOBDIR)
                for filename in locklist:
                    if not filename.startswith('.'):
                        #log.write('{}\n'.format(filename))
                        basename, extension = os.path.splitext(filename)
                        #log.write('basename: {} extension:{}\n'. format(basename,extension))
                        if extension == '.lock': run = run + 1
                        if extension == '.yaml':
                            
                            if not (basename + str('.lock')) in locklist:  
                                jobqueue.append(filename)
                shuffle(jobqueue) 
                log.write("runinning: {0} queued:{1} ".format(run,len(jobqueue)))  
                
                if len(jobqueue) > 0:
                    jobstorun = NUMTHREADS - run if len(jobqueue) > (NUMTHREADS - run) else len(jobqueue)
                    log.write('Adding {0} to running jobs. '.format(jobstorun))
                    for cardnum in range(0,jobstorun):
                        log.write('{} '.format(jobqueue[cardnum]))
                    for queue in range(0,jobstorun):
                        basename, extension = os.path.splitext(jobqueue[queue])
                        log.write('\nEXEC: CMD: {} -j {} -l {} {} -c {}\n'.format(JOBCMD, JOBDIR + "/" + jobqueue[queue], JOBLOG + '/' + basename + ".log", "-dINFO", JOBCFG + "/" + "config.yaml"))
                else:
                    log.write('JobQueue is empty')
                time.sleep(DELAY)
                run = 0
                job = 0
                jobqueue = []
                            
 
if __name__ == "__main__":
        daemon = MyDaemon(PIDFILE)
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:  
                        daemon.restart()
                else:
                        print ("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print ("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)
