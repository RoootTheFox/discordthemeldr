from textwrap import indent
from mitmproxy import http
from bs4 import BeautifulSoup
import json 
import os

def response(flow: http.HTTPFlow):
        flow.response.headers["content-security-policy"] = "default-src * 'unsafe-inline' 'unsafe-eval' data:; img-src * blob: data:; media-src * blob: data:"
        flow.response.headers["access-control-allow-origin"] = "*"
        if "content-type" in flow.response.headers:
                if flow.response.headers["content-type"] == "text/html" and (flow.request.pretty_url.startswith("https://discord.com/app") or flow.request.pretty_url.startswith("https://discord.com/channels")):
                        print("Received Discord App Response!")
                        print("Parsing HTML")
                        content = flow.response.content
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        print("Loading script")
                        script_file = open("loader.js")
                        script = script_file.read()
                        script_file.close()

                        print("Injecting JS")
                        tag = soup.new_tag("script")
                        tag.append(script)
                        soup.find("head").append(tag)

                        flow.response.text = soup.prettify()

def request(flow: http.HTTPFlow):
        if flow.request.pretty_url.startswith("https://discord.com/themeldr"):
                # currently unused, might use this to make installing the loader easier in case injecting js at load is against discord tos
                if flow.request.pretty_url == "https://discord.com/themeldr/getldr":
                        loader_file = open("loader.js")
                        loader = loader_file.read()
                        loader_file.close()
                        flow.response = http.Response.make(
                                200,
                                loader,
                                {"Content-Type": "text/javascript"}
                                )
                if flow.request.pretty_url == "https://discord.com/themeldr/modifytheme":
                        data = flow.request.content.decode('utf-8')
                        data_json = json.loads(data)
                        print("Theme: " + data_json["name"], "Enabled: " + str(data_json["enabled"]))
                        
                        datastore = {}
                        if os.path.exists("datastore.json"):
                                datastore_file = open("datastore.json", "r")
                                datastore = json.load(datastore_file)
                        else:
                                print ("no datastore.json")
                                datastore = {}
                        
                        print(datastore)
                        if "themes" not in datastore:
                                print("no themes in datastore")
                                datastore["themes"] = []
                        
                        already_indexed = False
                        for i in range(len(datastore["themes"])):
                                if datastore["themes"][i]["name"] == data_json["name"]:
                                        already_indexed = True
                                        datastore["themes"][i]["enabled"] = data_json["enabled"]
                                        datastore["themes"][i]["url"] = data_json["url"]
                                        datastore["themes"][i]["data"] = data_json["data"]
                        
                        if not already_indexed:
                                datastore["themes"].append({"name": data_json["name"], "enabled": data_json["enabled"], "url": data_json["url"], "data": data_json["data"]})
                        
                        with open('datastore.json', 'w') as outfile:  
                                json.dump(datastore, outfile, indent=4)
                        
                        flow.response = http.Response.make(
                                200,
                                "",
                                {"Content-Type": "text/plain"}
                                )
                
                if flow.request.pretty_url == "https://discord.com/themeldr/getthemes":
                        if os.path.exists("datastore.json"):
                                datastore_file = open("datastore.json", "r")
                                datastore = json.load(datastore_file)
                                flow.response = http.Response.make(200, json.dumps(datastore["themes"], indent=4), {"Content-Type": "application/json"})
                        else:
                                flow.response = http.Response.make(200,"[]",{"Content-Type": "application/json"})