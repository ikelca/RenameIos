#!/usr/bin/python
#
# Listing serial numbers of attached ios devices

# Multi-threading version 0.1 for Windows
#
# Usage: python listios.py school_code
#
# Author:Kelvin J. July,2017
#
#

import csv,sys,json,os 
import subprocess    
import time
import threading
import fnmatch

ideviceinfo='ideviceinfo.exe'
idevice_id='idevice_id.exe'
#idevicerestore='D:\dropbox\libimobile-Windows-most-updated\idevicerestore.exe'
#irecovery='D:\dropbox\libimobile-Windows-most-updated\irecovery.exe'
#ideviceenterrecovery='D:\dropbox\libimobile-Windows-most-updated\ideviceenterrecovery.exe'
global ipswPath
#ipswPath='D:\iPad_64bit_10.3.3_14G60_Restore.ipsw'
home =os.path.expanduser('c:\ios')


def main():
    if len(sys.argv) != 2:
        sys.exit("Missing school code")
    if len(sys.argv[1])!=4: 
        sys.exit('Please check school code again (e.g. 0204)...')
   
    proc = subprocess.Popen([idevice_id, '-l'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    try:
        global ipad_devices
        ipad_devices=out.split()
        #print ipad_devices
    except:
        sys.exit("Error: "+ err) 
    
    
    
    
    if not ipad_devices:
        print "No attached devices found..."
        sys.exit(1)
        
    threads = []
    output=[]
    
    for udid in ipad_devices: 
        t = threading.Thread(target=worker,args=(udid,output))
        threads.append(t)
        
    print("starting to get serial numbers...")
    print '-----------------------------------'
    start = time.time()
    for x in threads:
         x.start()

    # Wait for all of them to finish
    for x in threads:
         x.join()
 
    print '-----------------------------------' 
 
    school_code = str(sys.argv[1]) 
    if not os.path.exists(home):
        os.mkdir(home)
    if os.path.exists(home+'\\'+school_code+'.csv'):   
        num=len(fnmatch.filter(os.listdir(home),school_code+"*.csv"))
        school_code+='_'+str(num+1)
    try:    
        toCSV(list(set(output)),school_code)
    except:
        print "Error saving csv file..."
    
    print "Total number for this run: "+str(len(output))
    
    
    print "Overall number for this school: "+str(len(getTotal(home,school_code[:4])))
    end = time.time() 
    print 'Total time elapsed: %02d:%02d'% divmod((end - start), 60) 
    
    #toCSV(output)
    #Query device
    #browser=createBrowser()  
    #print str(len(output))+' devices restored'
    #print output
    
    #    query(browser,i)
          
     
def worker(udid,lst):     
        proc3=subprocess.Popen([ideviceinfo, '-u',udid,'-k','SerialNumber'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out3, err3=proc3.communicate()
         
        if len(out3.rstrip())==12:
            lst.append(out3.rstrip())
            print out3.rstrip()+'\n' 
        time.sleep(1)

        return

def toCSV(lst,filename):  
    with open(home+ "\\"+filename+".csv", "wb") as f:
        #writer = csv.writer(f)
        for line in lst:
            f.write(str(line))
            f.write('\n')
     
    print 'Saved to %s'%filename+'.csv'
    
def getTotal(home,school_code):
    total=[]
    for f in fnmatch.filter(os.listdir(home),school_code+"*.csv"): 
        for l in open(home+'\\'+f).readlines(): 
            total.append(l) 
    return list(set(total))
    
if __name__ == '__main__':
    main()
