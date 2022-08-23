from textwrap import indent
from mitmproxy import http
from bs4 import BeautifulSoup
import json
import os
import re
import requests

pronoundb_pronouns = {
        "unspecified": "Unspecified",
        "hh": "he/him",
        "hi": "he/it",
        "hs": "he/she",
        "ht": "he/they",
        "ih": "it/him",
        "ii": "it/its",
        "is": "it/she",
        "it": "it/they",
        "shh": "she/he",
        "sh": "she/her",
        "si": "she/it",
        "st": "she/they",
        "th": "they/he",
        "ti": "they/it",
        "ts": "they/she",
        "tt": "they/them",
        "any": "Any pronouns",
        "other": "Other pronouns",
        "ask": "Ask me my pronouns",
        "avoid": "Avoid pronouns, use my name"
}
def startswith_discord_endpoint(url, endpoint):
        match = re.search("^https://(canary.discord.com|discord.com|ptb.discord.com)/", url)
        if match is not None:
                url_endpoint = str(url).replace(str(match.group(0)), "", 1)
                if url_endpoint.startswith(endpoint):
                        return True
                else:
                        return False
        else:
                return False

def startswith_discord_api_endpoint(url, endpoint):
        match = re.search("^https://(canary.discord.com|discord.com|ptb.discord.com)/api/v\d?\d/", url)
        if match is not None:
                url_endpoint = str(url).replace(str(match.group(0)), "", 1)
                if url_endpoint.startswith(endpoint):
                        return True
                else:
                        return False
        else:
                return False

def response(flow: http.HTTPFlow):
        startswith_discord_endpoint(flow.request.pretty_url, "")

        flow.response.headers["content-security-policy"] = "default-src * 'unsafe-inline' 'unsafe-eval' data:; " \
                                                           "img-src * blob: data:; media-src * blob: data: "
        if "content-type" in flow.response.headers:
                if flow.response.headers["content-type"] == "text/html" and (startswith_discord_endpoint(flow.request.pretty_url, "app") or startswith_discord_endpoint(flow.request.pretty_url, "channels")):
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
        # https://canary.discord.com/api/v9/users/512242962407882752/profile?with_mutual_guilds=false&guild_id=264801645370671114
        if startswith_discord_api_endpoint(flow.request.pretty_url, "users/") and flow.request.pretty_url.__contains__("/profile"):
                url = flow.request.pretty_url

                match = re.search("users/(\d{8,20})/profile", url)
                data = json.loads(flow.response.content.decode())
                #data["user"]["avatar_decoration"] = "rainbow"
                if match is not None and match.groupdict().__sizeof__() > 1:
                        print("profile request!!!")
                        user_id = match.group(1)
                        print("user id: " + user_id)

                        pndb_response = requests.get("https://pronoundb.org/api/v1/lookup", params={'platform': 'discord', 'id':user_id})
                        print("pndb: " + pndb_response.text)
                        if pndb_response.status_code == 200:
                                print("has pronoundb entry!")
                                pndb_data = json.loads(pndb_response.text)
                                pndb_entry = pndb_data["pronouns"]
                                print("entry: " + pndb_entry)
                                pronouns = pronoundb_pronouns.get(pndb_entry)
                                if pronouns != "Unspecified":
                                        data["user_profile"]["pronouns"] = pronouns

                flow.response.text = json.dumps(data)

def request(flow: http.HTTPFlow):
        #if flow.request.pretty_url.startswith("https://cdn.discordapp.com/avatar-decorations/"):
        #        deco_file = open("rainbow.png", mode="rb")
        #        deco = deco_file.read()
        #        deco_file.close()
        #        flow.response = http.Response.make(200, deco, {"Access-Control-Allow-Origin": "*"})

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
                        flow.response.headers["access-control-allow-origin"] = "*"
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
                        flow.response.headers["access-control-allow-origin"] = "*"

                if flow.request.pretty_url == "https://discord.com/themeldr/getthemes":
                        if os.path.exists("datastore.json"):
                                datastore_file = open("datastore.json", "r")
                                datastore = json.load(datastore_file)
                                flow.response = http.Response.make(200, json.dumps(datastore["themes"], indent=4), {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})
                        else:
                                flow.response = http.Response.make(200,"[]",{"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})