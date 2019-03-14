# -*- coding: utf-8 -*-
###############################################################################
# VU+ Edition
# Chrashlogs, Vorschlaege, Beschwerden usw. bitte an plugins (at) fselbig.de
#
# This plugin is licensed under the Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0). 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to CreativeCommons, 559 Nathan Abbott Way, Stanford, California 94305, USA
#
# In addition, this plugin may only be distributed and executed on
# hardware which is licensed by Vu+ and E2 
###############################################################################

from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.HelpMenu import HelpableScreen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.ActionMap import HelpableActionMap
from Components.Input import Input
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.MenuList import MenuList
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSelection, ConfigText, ConfigDateTime, ConfigYesNo, getConfigListEntry, NoSave, ConfigNothing
from Components.Sources.List import List

from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, ConfigDirectory, ConfigSubsection, ConfigInteger, ConfigSelection, ConfigText, ConfigEnableDisable, getConfigListEntry, NoSave, ConfigYesNo,ConfigSequence, ConfigText 
from ConfigParser import ConfigParser, DuplicateSectionError

from enigma import eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, gFont, eListbox, getDesktop
from enigma import getDesktop
from skin import parseColor, parseFont
from Tools.Directories import fileExists
import os
import datetime
import json
from urllib2 import urlopen

version="0.1"
dat="/etc/ConfFS/wiffi2e2FS.conf"
all_plugin_path = "/usr/lib/enigma2/python/Plugins/Extensions/"
plugin_path=all_plugin_path+"wiffi2e2FS"
skin_ext=plugin_path +"/skin/"
skin_ext_zusatz=""

DWide = getDesktop(0).size().width()
size_w = getDesktop(0).size().width()
size_h = getDesktop(0).size().height()

if size_w > 1850:
            skin_ext_zusatz="fHD/"
            font1=30
            font2=18
            zeil_high=40

else:
            skin_ext_zusatz="HD/"
            font1=26
            font2=18
            zeil_high=30





wiffi_conf= {"wiffi_ip":None,"abrufintervall":300,"debug":False}
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

abrufintervall=int(wiffi_conf["abrufintervall"])
debug=wiffi_conf["debug"]







ren_list={17:"Luftfeuchtigkeit (absolut)",10:"Helligkeit",0:"Wiffi-IP",32:"Niederschlag heute (Dauer)",26:"Sonne heute",1:"Temperatur",21:"Temperatur (gef.)",16:"Sonne scheint",2:"Luftfeuchtigkeit (rel)",13:"Sonne Azimut",12:"Sonne Elevation",30:"Sonnenaufgang",31:"Sonnenuntergang",
                          19:"Regen (letzte Stunde)",27:"Regen gestern",20:"Regen heute (Menge ges.)",7:"Niederschlag jetzt",18:"Regensensor (Wert)",8:"Regen jetzt (Menge)",3:"Barometer",11:"Barometer-Trend"}


modul="n/a"
default_sys={"MAC-Adresse":"n/a","Homematic_CCU_ip":"n/a","WLAN_ssid":"n/a","WLAN_Signal_dBm":"n/a","sec_seit_reset":"n/a","zeitpunkt":"n/a","firmware":"n/a"}
default_l={0:{"name":"0","homematic_name":"wiffi1","desc":"rainyman_ip","type":"string","unit":"","value":"192.xxxxx"},
		    1:{"name":"1","homematic_name":"w_temperatur","desc":"aussentemperatur","type":"number","unit":"gradC","value":"n/a"},
		    2:{"name":"2","homematic_name":"w_feuchte_rel","desc":"rel_feuchte","type":"number","unit":"%","value":"n/a"},
		    3:{"name":"3","homematic_name":"w_barometer","desc":"nn_luftdruck","type":"number","unit":"mb","value":"n/a"},
		    4:{"name":"4","homematic_name":"w_wind_mittel","desc":"avg_windgeschwindigkeit","type":"number","unit":"m/s","value":"n/a"},
		    5:{"name":"5","homematic_name":"w_wind_spitze","desc":"peak_windgeschwindigkeit","type":"number","unit":"m/s","value":"n/a"},
		    6:{"name":"6","homematic_name":"w_wind_dir","desc":"windwinkel","type":"number","unit":"grad","value":"n/a"},
		    7:{"name":"7","homematic_name":"w_regenmelder","desc":"regenstatus","type":"boolean","unit":"","value":"n/a"},
		    8:{"name":"8","homematic_name":"w_regenstaerke","desc":"regenstaerke","type":"number","unit":"mm/h","value":"n/a"},
		    9:{"name":"9","homematic_name":"w_taupunkt","desc":"taupunkt_temperatur","type":"number","unit":"gradC","value":"n/a"},
		    10:{"name":"10","homematic_name":"w_lux","desc":"helligkeit","type":"number","unit":"lux","value":"n/a"},
		    11:{"name":"11","homematic_name":"w_barotrend","desc":"luftdrucktrend","type":"string","unit":"","value":"n/a"},
		    12:{"name":"12","homematic_name":"w_elevation","desc":"sonne_elevation","type":"number","unit":"grad","value":"n/a"},
		    13:{"name":"13","homematic_name":"w_azimut","desc":"sonne_azimut","type":"number","unit":"grad","value":"n/a"},
		    14:{"name":"14","homematic_name":"w_himmeltemperatur","desc":"himmel_temperatur","type":"number","unit":"gradC","value":"n/a"},
		    15:{"name":"15","homematic_name":"w_sonnentemperatur","desc":"sonnen_temperatur","type":"number","unit":"gradC","value":"n/a"},
		    16:{"name":"16","homematic_name":"w_sonne_scheint","desc":"sonne_scheint","type":"boolean","unit":"","value":"n/a"},
		    17:{"name":"17","homematic_name":"w_feuchte_abs","desc":"abs_feuchte","type":"number","unit":"g/m3","value":"n/a"},
		    18:{"name":"18","homematic_name":"w_regensensor_wert","desc":"regenmelderwert","type":"number","unit":"","value":"n/a"},
		    19:{"name":"19","homematic_name":"w_regen_letzte_h","desc":"regen_pro_h","type":"number","unit":"mm","value":"n/a"},
		    20:{"name":"20","homematic_name":"w_regen_mm_heute","desc":"regen_mm_heute","type":"number","unit":"mm","value":"n/a"},
		    21:{"name":"21","homematic_name":"w_windchill","desc":"gefuehlte_temperatur","type":"number","unit":"gradC","value":"n/a"},
		    22:{"name":"22","homematic_name":"w_sonne_diff_temp","desc":"sonnen_difftemperatur","type":"number","unit":"gradC","value":"n/a"},
		    23:{"name":"23","homematic_name":"w_windrichtung","desc":"windrichtung","type":"string","unit":"","value":"n/a"},
		    24:{"name":"24","homematic_name":"w_windstaerke","desc":"bft_windgeschwindigkeit","type":"number","unit":"bft","value":"n/a"},
		    25:{"name":"25","homematic_name":"w_bodenfeuchte","desc":"bodenfeuchte","type":"number","unit":"","value":"n/a"},
		    26:{"name":"26","homematic_name":"w_sonnenstunden_heute","desc":"Sonnenstunden_heute","type":"number","unit":"h","value":"n/a"},
		    27:{"name":"27","homematic_name":"w_regen_mm_gestern","desc":"regen_mm_gestern","type":"number","unit":"mm","value":"n/a"},
		    30:{"name":"30","homematic_name":"w_minuten_vor_sa","desc":"minuten_vor_sa","type":"number","unit":"min","value":"n/a"},
		    31:{"name":"31","homematic_name":"w_minuten_vor_su","desc":"minuten_vor_su","type":"number","unit":"min","value":"n/a"},
		    32:{"name":"32","homematic_name":"w_regenstunden_heute","desc":"regenstunden_heute","type":"number","unit":"h","value":"n/a"}
		    }




class wiffi_anzeige(Screen):
        tmpskin = open(skin_ext+skin_ext_zusatz +"wiffi.xml")
	skin = tmpskin.read()
	tmpskin.close()


	def __init__(self,session):
                Screen.__init__(self, session)
                self.skinName = "wiffi-Daten"
                self.setTitle("wiffi to e2 - "+version)
		self["key_red"] = StaticText(_("Close"))
		self["key_blue"] = StaticText(_("Syteminfo"))
		self["key_yellow"] = StaticText(_("refresh"))
		self["key_green"] = StaticText(_("Settings"))
		self["modul"] = Label("")
                list1 = []
                list2 = []
                self["ml1"] = List(list1)

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
		{
			"cancel": self.close,
			"blue": self.sysinfo,
			"yellow": self.rload,
			"green": self.settings,
		}, -1)
		self.rload()
	def rload(self):
                list1 = []
                list2 = []
                reading()
                if modul !="n/a":
                    if str(default_sys["zeitpunkt"]) != "n/a":
                        tm=str(default_sys["zeitpunkt"]).split("/")
                        tm_d=tm[0].split(".")
                        tm_d2=tm_d[2]+"."+tm_d[1]+"."+tm_d[0] + " "*2+tm[1]
                    self["modul"].setText(str(modul)+" "*5 + str(tm_d2))
                else:
                    self["modul"].setText("Daten konnten nicht gelesen werden!")

                for k in default_l.keys(): #wiffi_data.iteritems():
                          try:
                              value1= default_l[k]["value"]
                              dk=str(default_l[k]["desc"])
                              if "feuchte" in dk.lower() and value1=="0":
                                  value1="n/a"
                              if value1 != "n/a":
                                  if default_l[k]["type"] == "number":
                                     value1=value1.replace(".",",")
                                  value1= value1+" "+default_l[k]["unit"]
                                  value1=str(value1.replace("UNICODE","").replace("_"," ").replace("\x00","").decode("latin-1", "ignore")) 
                                  if k==30 or k==31:
                                      v_b= value1.strip().replace("min","")
                                      v_b_minu=int(v_b)
                                      if v_b_minu<0:
                                          v_b_minu=v_b_minu+1440
                                      
                                      y = datetime.datetime.now() + datetime.timedelta(minutes=v_b_minu)
                                      y2=y.strftime("%H:%M Uhr")
                                      value1=y2 +" "*2+"(+"+str(v_b_minu)+" min)"
                                  value1=value1.replace("grad","°").replace("true","ja").replace("false","nein")
                                  if k==7 and value1.strip()=="ja" and int(float(default_l[8]["value"]))>0:
                                     value1=value1+", "+ default_l[8]["value"]+" "+default_l[8]["unit"]
                              
                              #k2=default_l[k]["homematic_name"].replace("w_","")
                              if k in ren_list:
                                dk=ren_list[k]
                              if value1 != "n/a": 
                                  if k !=8 and k !=0:
                                      list1.append((dk,str(value1)))
                              else:
                                  list2.append((dk,"n/a"))
                          except Exception, e:
                              #pass
                              f=open("/tmp/wiffi_loadFS_error","a")
                              f.write(str(e)+"\n")
                              f.close()    
                #list1.sort()
                list1.sort(key=lambda x: x[0].lower())
                if len(list2):
                    list1.append(("  -- ohne Werte -- ",""))
                    list1.extend(list2)
                self["ml1"].setList(list1)                  

	def settings(self):
	      self.session.openWithCallback(self.running_set,wiffi2e2FSConfiguration)
	def running_set(self):
              global wiffi_conf
	      configparser = ConfigParser()   
	      configparser.read(dat)
	      if configparser.has_section("settings"):
	          l1=configparser.items("settings")
	          for k,v in  l1:
	              wiffi_conf[k] = v
              self.rload()



        def sysinfo(self):
	   txt= str(default_l[0]["desc"]).replace("_"," ")+": "+str(default_l[0]["value"])+"\n"
	   for key2,value2 in default_sys.items():
	       txt=txt+str(key2).replace("_"," ")+": "+str(value2)+"\n"
	   self.session.open(MessageBox,txt,MessageBox.TYPE_INFO)
def reading():
    wiffi_ip=str(wiffi_conf["wiffi_ip"])
    global modul
    global default_sys
    global default_l
    if wiffi_ip:
      url="http://"+str(wiffi_ip)+"/?json"
      try:
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data2=json.loads(data)
        
        for key,value in data2.items():
            if key== "modultyp":
                  modul=value
            elif key== "Systeminfo":
                s_info=value
                for key2,value2 in s_info.items():
                    default_sys[key2]=value2
                    #d3="sys %s: %s" % (key2, value2)
                    #if debug:f.write(d3+"\n")
            elif key== "vars":
                #wiffi_data={}
                for x in value:
                    u_value= x
                    nam0= int(u_value["name"])
                    default_l[nam0]=u_value

      except Exception, e:
        f=open("/tmp/wiffi_loadFS_error","a")
        f.write("\nwiffi: "+str(e))
        f.close() 
        
class wiffi2e2FSConfiguration(Screen, ConfigListScreen, HelpableScreen):
	tmpskin = open(skin_ext+skin_ext_zusatz+"wiffi_setup.xml")
	skin = tmpskin.read()
	tmpskin.close()
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = "wiffi_Setup"
		HelpableScreen.__init__(self)
		titel1 = "wiffi2e2FS "+_("Settings")
		#self.wiffi_ip=str(conf["wiffi_ip"])
		self.wiffi_ip=NoSave(ConfigText(default=str(wiffi_conf["wiffi_ip"]), fixed_size=False))
		self.debug=NoSave(ConfigEnableDisable(default=wiffi_conf["debug"]))
                self["key_red"] = Label(_("Cancel"))
		self["balken"] = Label(_("Press OK") + ", " + _("Select with left / right")+" "+_("main")+", "+_("Infoline")+", "+_("Default for full screen and diashow")+", "+_("Thumbnails"))
		self["key_green"] = Label(_("Save"))
		self["key_yellow"] = Label("")
		self["key_blue"] = Label("")
		self["pic_red"] = Pixmap()
		self["pic_green"] = Pixmap()
		self["pic_yellow"] = Pixmap()
		self["pic_blue"] = Pixmap()
                self["bgr2"] = Pixmap()
		self.onChangedEntry = [ ]
		self.session = session

		self["pcfsKeyActions"] = HelpableActionMap(self, "pcfsKeyActions",
			{
			"green": (self.save,_("Save")),
			"red": (self.keyCancel,_("Cancel")),
			"ok": (self.ok_button,_("edit if possible")),
			"cancel": (self.keyCancel,_("Cancel and close")),
			}, -2)
                self.refresh()
                self.setTitle(titel1)
                ConfigListScreen.__init__(self, self.liste, on_change = self.reloadList) # on_change = self.changedEntry)
		#if not self.set_help in self["config"].onSelectionChanged:
		#	self["config"].onSelectionChanged.append(self.set_help)

	def refresh(self):
		liste = []
                liste.append(getConfigListEntry(_("wiffi IP:"),self.wiffi_ip))
                liste.append(getConfigListEntry(_("write debug:"), self.debug))
                
                self.liste = liste

	def reloadList(self):
                self.refresh()
		self["config"].setList(self.liste)

	def keyCancel(self):
		self.session.openWithCallback(
				self.cancelConfirm,
				MessageBox,_("Really close without saving settings?"),MessageBox.TYPE_YESNO)

	def cancelConfirm(self, result):
		if result:
			self.close()
	def ok_button(self):
            self.cur = self["config"].getCurrent()
	    self.cur = self.cur and self.cur[1]
	    if self.cur == self.wiffi_ip:
                    self.session.openWithCallback(
				self.texteingabeFinished,
				VirtualKeyBoard,
				title = _("Edit IP for rainman or weatherman:"),
				text = self.wiffi_ip.value
			)
	def texteingabeFinished(self, ret):
                if ret is not None:
		    self.wiffi_ip.value = ret



               
	def save(self):
            self.configparser = ConfigParser()
	    self.configparser.read(dat)

            if self.configparser.has_section("settings"):self.configparser.remove_section("settings")
            self.configparser.add_section("settings")
            self.configparser.set("settings", "wiffi_ip", self.wiffi_ip.value)
            self.configparser.set("settings", "debug", self.debug.value)

            fp = open(dat,"w")
            self.configparser.write(fp)
            fp.close()
            self.close()																															