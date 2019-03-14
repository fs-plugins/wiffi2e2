
from Plugins.Plugin import PluginDescriptor
from enigma import eTimer
from ConfigParser import ConfigParser 
import os
from urllib2 import urlopen
import json
from anzeige import wiffi_anzeige

timecheck = eTimer()

dat="/etc/ConfFS/wiffi2e2FS.conf"
wiffi_conf= {"wiffi_ip":None,"abrufintervall":300,"debug":0}
all_plugin_path = "/usr/lib/enigma2/python/Plugins/Extensions/"
if os.path.exists(dat):
    configparser = ConfigParser()   
    configparser.read(dat)
    if configparser.has_section("settings"):
        l1=configparser.items("settings")
        for k,v in  l1:
            wiffi_conf[k] = v
else:
    f=open(dat,"w")
    f.write("[settings]\n")
    f.write("wiffi_ip = None\n")
    f.write("debug = False\n")
    f.close()



wiffi_ip=wiffi_conf["wiffi_ip"]
abrufintervall=int(wiffi_conf["abrufintervall"])
debug=wiffi_conf["debug"]


wiffi_data=None

def GotDeviceData(data = None):
    try:timecheck.stop()
    except:pass
    if data is not None:
        try:
                pass
                
                


            
        except Exception, e:
            f2=open("/tmp/wiffi_loadFS_error","a")
            f2.write(str(e)+"\n")
            f2.close()
    
    timecheck.startLongTimer(abrufintervall)









def reading(**kwargs):
    global wiffi_data
    if wiffi_ip:
      url="http://"+str(wiffi_ip)+"/?json"
      try:
        f=open("/tmp/wiffi_dats","w")
        response = urlopen(url)
        data = response.read().decode("utf-8")
        if debug:f.write(data+"\n") 
        data2=json.loads(data)
        
        for key,value in data2.items():
            if key== "Systeminfo":
                s_info=value
                for key2,value2 in s_info.items():
                    d3="sys %s: %s" % (key2, value2)
                    if debug:f.write(d3+"\n")
            elif key== "vars":
                wiffi_data={}
                for x in value:
                    u_value= x
                    nam0= int(u_value["name"])
                    nam1= u_value["homematic_name"]#.replace("w_","")
                    wert= u_value["value"]
                    unit=u_value["unit"]
                    wiffi_data[nam0]=str(wert)+" "+str(unit)
                    d3="vars %s, %s: %s" % (str(nam0),nam1,wert)
                    if debug:f.write(d3+"\n") 
            else:               
                d2="%s: %s" % (key, value)
                if debug:f.write(d2+"\n")
   
        f.close()
      except Exception, e:
        f2=open("/tmp/wiffi_loadFS_error","a")
        f2.write("\nwiffi: "+str(e))
        f2.close()


    #url_str=data_url 
    #(url_str).addCallback(GotDeviceData).addErrback(downloadDeviceError)



def checks():
    res1=1
    res2=1
    f=open("/tmp/wiffi_loadFS_error","w")
    if wiffi_ip:
        res2 = subprocess.call(['ping', '-c', '3', wiffi_ip])
        if res2:
            f.write("wiffi-Ping: "+wiffi_ip+" -> "+str(res1)+"\n")
    else:
         if debug:f.write("wiffi not set\n")
    f.close()    
    #if res1==0 or res2==0:
    #timecheck.callback.append(reading)
    reading()
    
def autostart(reason, **kwargs):
  global session
  if "session" in kwargs:
        session= kwargs["session"]
  #if session and reason == 0:
  
  checks()
  


def main(session,**kwargs):
	session.open(wiffi_anzeige)
        #pass





def Plugins(**kwargs):
	list = []
	#list.append(PluginDescriptor(name="wiffi_loadFS", where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc = autostart))
	list.append(PluginDescriptor(name="wiffi2e2FS",description=_("show dats from weatherman etc"), where = [PluginDescriptor.WHERE_PLUGINMENU], fnc=main))
        return list

