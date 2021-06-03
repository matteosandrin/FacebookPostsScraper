from FacebookPostsScraper import FacebookPostsScraper as FPS
from pprint import pprint as pp
from datetime import datetime
import configparser
import os
import json
import requests
import dateparser

config = configparser.ConfigParser()
config.read("config")

dp_settings = {
    'TIMEZONE': 'US/Eastern',
    'PREFER_DATES_FROM': 'past'
}

def log(message):
    print("[+] [{}] {}".format(datetime.now().isoformat(), message))

def notify(message, url):
    params = {
        "token" : config["PUSHOVER"]["TOKEN"],
        "user" : config["PUSHOVER"]["USER"],
        "message" : message,
        "url" : url
    }
    requests.post("https://api.pushover.net/1/messages.json", params=params)

def writeToFile(data, target_id):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "{}.json".format(target_id)
    )
    f = open(path, "w")
    f.write(json.dumps(data, indent=4, sort_keys=True))
    f.close()

def readFromFile(target_id):
    path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)),
        "{}.json".format(target_id)
    )
    if not os.path.exists(path):
        writeToFile([], target_id) 
    return json.load(open(path))

def findFreshPosts(old, new):
    old_urls = set(o["post_url"] for o in old)
    new_urls = set(n["post_url"] for n in new)
    # set difference: return only the posts we haven't seen before
    diff = new_urls - old_urls
    return [n for n in new if (n["post_url"] in diff)]

targets = {
    "harvard_mit_housing" : {
        "label" : "Harvard/MIT Housing",
        "url" : "https://m.facebook.com/groups/HarvardMITHousing"
    },
    "gypsy_housing" : {
        "label" : "Gypsy Housing",
        "url" : "https://www.facebook.com/groups/GypsyHousingBrooklyn"
    },
    "columbia_off_campus_housing" : {
        "label" : "CU Off-Campus Housing",
        "url" : "https://www.facebook.com/groups/1262075723841084"
    }
}

email = config["FACEBOOK"]["EMAIL"]
password = config["FACEBOOK"]["PASSWORD"]
fps = FPS(email, password)

for target_id, target in targets.items():

    log("Starting to check \"{}\"...".format(target["label"]))
    old_data = readFromFile(target_id)
    new_data = fps.get_posts_from_profile(target["url"])
    fresh_data = findFreshPosts(old_data, new_data)

    log("Found {} new posts".format(len(fresh_data)))

    for f in fresh_data:

        if ("description" in f) and (len(f["description"]) > 0):
            desc = f["description"][:min(60, len(f["description"]))]
            desc = desc.replace("\n", " ")
            message = target["label"] + ": " + desc + "..."
            log(message)
            url = f["post_url"]
            if ("published" in f) and (len(f["published"]) > 0):
                f["published"] = dateparser.parse(f["published"], settings=dp_settings).isoformat()
            notify(message, url)
            old_data.append(f)
            writeToFile(old_data, target_id)
            old_data = readFromFile(target_id)

    log("Finished check on \"{}\"...".format(target["label"]))

log("Done.")
log("")