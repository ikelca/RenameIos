#!/usr/bin/python
#
# Listing serial numbers of attached ios devices, also saving to cooresponding csv file
#
# version 0.1 (single threading)
#
# Usage: python listios.py school_code
#
# Author:Kelvin J. July,2017
#
#

import csv,sys,json,os
import plistlib
import subprocess
from pprint import pprint 
from StringIO import StringIO 
import time 
import fnmatch

CFGUTIL = '/Applications/Apple Configurator 2.app/Contents/MacOS/cfgutil'
home =os.path.expanduser("~") 

def main():
    if len(sys.argv) != 2:
        sys.exit("Missing school code")

    
    proc = subprocess.Popen([CFGUTIL, '--format', 'plist', 'list'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    try:
        ipad_devices = plistlib.readPlistFromString(out)['Output'] 
        #print ipad_devices
    except:
        sys.exit("Error: "+err) 
    output=[]
    
    if not ipad_devices:
        print "No attached devices found..."
        sys.exit(1)
    start = time.time()
    print("Starting to get serial numbers...")
    print('---------------------------------')
    for ecid, data in ipad_devices.iteritems():
        # output.update({data['name']:""})  
        try:
            proc2=subprocess.Popen([CFGUTIL, '-e', ecid, 'get','serialNumber'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
            out2, err2=proc2.communicate()
            if len(out2.rstrip())<13:
                output.append(out2.rstrip())
                print out2.rstrip() 
        except:
            sys.exit('Error: '+ ecid+" : "+err2)
            
    print('---------------------------------')


    school_code = str(sys.argv[1])
    
    if os.path.exists(home+'/'+school_code+'.csv'):  
        
        num=len(fnmatch.filter(os.listdir(home),school_code+"*.csv"))
        school_code+='_'+str(num+1)
    try:    
        toCSV(output,school_code)
    except:
        print "Error saving csv file..."
    
    print "Total number for this run: "+str(len(output))
    
    
    print "Overall number for this school: "+str(len(getTotal(home,school_code[:4])))
    end = time.time() 
    print 'Total time elapsed: %02d:%02d'% divmod((end - start), 60) 
        
def toCSV(lst,filename): 
    home =os.path.expanduser("~")
    with open(home+ "/"+filename+".csv", "wb") as f:
        #writer = csv.writer(f)
        for line in lst:
            f.write(str(line))
            f.write('\n')
     
    print 'Saved to %s'%filename+'.csv'
    
def getTotal(home,school_code):
    total=[]
    for f in fnmatch.filter(os.listdir(home),school_code+"*.csv"): 
        for l in open(home+'/'+f).readlines(): 
            total.append(l) 
    return list(set(total))
    
if __name__ == '__main__':
    main()
