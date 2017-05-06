#!/usr/bin/python
from browsermobproxy import Server
from selenium import webdriver
import os
import json
import urlparse,sys;

mobile_or_not = sys.argv[1]; # mobile or not
extension = sys.argv[2]; # mobile or not

# path to browsemob-proxy 
server = Server("/path/to/browsermob-proxy-2.1.2/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()

#chromedriver = "/Users/kgarimella/Documents/adblock/chromedriver"
#os.environ["webdriver.chrome.driver"] = chromedriver
url = urlparse.urlparse (proxy.proxy).path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(url))

output_folder = "data";

if(mobile_or_not=="mobile"):
	mobile_emulation = {'deviceName': 'Google Nexus 5'};
	chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
	output_folder += "_mobile";

if(extension=="adblock"):
	chrome_options.add_extension('/Users/kgarimella/Documents/adblock/AdBlock_v3.4.0.crx');
	output_folder += "_with_adblock"
elif(extension=="adblockplus"):
	chrome_options.add_extension('/Users/kgarimella/Documents/adblock/Adblock-Plus_v1.12.4.crx');
	output_folder += "_with_adblockplus"
elif(extension=="ghostery"):
	chrome_options.add_extension('/Users/kgarimella/Documents/adblock/Ghostery_v7.1.0.49.crx');
	output_folder += "_with_ghostery"
elif(extension=="privacy"):
	chrome_options.add_extension('/Users/kgarimella/Documents/adblock/Privacy-Badger_v2016.9.7.crx')
	output_folder += "_with_privacy_badger"
elif(extension=="ublock"):
	chrome_options.add_extension('/Users/kgarimella/Documents/adblock/uBlock-Origin_v1.9.16.crx');
	output_folder += "_with_ublock"

driver = webdriver.Chrome(chrome_options = chrome_options)
#driver.set_page_load_timeout(10)

f = open("/Users/kgarimella/Documents/adblock/alexa_top_150.txt");
lines = f.readlines();

for line in lines:
    line = line.strip();
    url = "http://www." + line;
    print >> sys.stderr, "processing", url;
    try:
    	proxy.new_har(url);#, options={'captureHeaders': True})
    	driver.get(url);
    	result = json.dumps(proxy.har, ensure_ascii=False)
    	out = open(output_folder + "/" + line.replace("/","_"), "w");
    	out.write(result.encode('utf-8'));
    	out.close();
    except:
	print >> sys.stderr, "skipped", url;
	pass;
#    break;
#proxy.stop()
driver.quit()
