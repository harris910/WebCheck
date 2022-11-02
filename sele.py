from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import shutil

from pyvirtualdisplay import Display
import pandas as pd
import requests
import os


# virtual display
display = Display(visible=0, size=(800, 600))
display.start()

# df = pd.read_csv(r'3.csv')
# extractDigits(os.listdir('/home/student/TrackerSift/UserStudy/output'))
df = pd.DataFrame([["ebay.com"]], columns=["website"])

# helper functions for breakpoints
def getInitiator(stack):
    try:
        if len(stack["callFrames"]) != 0:
            if (
                "chrome-extension" not in stack["callFrames"][0]["url"]
                and stack["callFrames"][0]["url"] != ""
            ):
                return {
                    "lineNumber": int(stack["callFrames"][0]["lineNumber"]),
                    "url": stack["callFrames"][0]["url"],
                    "columnNumber": int(stack["callFrames"][0]["columnNumber"]),
                }
        else:
            return getInitiator(stack["parent"])
    except:
        pass


# script sample -> at l (https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
# return https://c.amazon-adsystem.com/aax2/apstag.js@l
def getStorageScriptFromStack(script):
    try:
        script = script.split("\n")[2]
        method = script.split("(")[0].strip().split(" ")[1]  # l
        script = script.split("(")[
            1
        ]  # https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
        # return "https:" + script.split(":")[1] + "@" + method
        # "columnNumber": script.split(":")[3].split(")")[0],
        return {
            "lineNumber": int(script.split(":")[2]),
            "url": "https:" + script.split(":")[1],
            "columnNumber": int(script.split(":")[3].split(")")[0]),
        }
    except:
        return None


def addBreakPoints(filename):
    arr = []
    with open(filename + "/request.json") as file:
        for line in file:
            dataset = json.loads(line)
            if dataset["call_stack"]["type"] == "script":
                val = getInitiator(dataset["call_stack"]["stack"])
                if val is not None and val not in arr:
                    arr.append(val)

    storage_setItem = {
        "lineNumber": 5,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    storage_getItem = {
        "lineNumber": 30,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    cookie_setItem = {
        "lineNumber": 76,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    cookie_getItem = {
        "lineNumber": 55,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    addEventList = {
        "lineNumber": 98,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    sendBeac = {
        "lineNumber": 125,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    removeEventList = {
        "lineNumber": 148,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    setAttrib = {
        "lineNumber": 175,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    getAttrib = {
        "lineNumber": 201,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }
    removeAttrib = {
        "lineNumber": 226,
        "url": "chrome-extension://dkbabheepgaekgnabjadkefghhglljil/inject.js",
        "columnNumber": 4,
    }

    arr.append(storage_setItem)
    arr.append(storage_getItem)
    arr.append(cookie_setItem)
    arr.append(cookie_getItem)
    arr.append(addEventList)
    arr.append(sendBeac)
    arr.append(removeEventList)
    arr.append(setAttrib)
    arr.append(getAttrib)
    arr.append(removeAttrib)

    f = open(
        "extension/breakpoint.json",
        "w",
    )
    f.write(str(arr).replace("'", '"'))
    f.close()


# selenium to visit website and get logs
def visitWebsite(df):
    # try:
    dic = {}
    # extension filepath
    ext_file = "extension"

    opt = webdriver.ChromeOptions()
    # devtools necessary for complete network stack capture
    opt.add_argument("--auto-open-devtools-for-tabs")
    # loads extension
    opt.add_argument("load-extension=" + ext_file)
    # important for linux
    opt.add_argument("--no-sandbox")

    dc = DesiredCapabilities.CHROME
    dc["goog:loggingPrefs"] = {"browser": "ALL"}

    os.mkdir("server/output/" + df["website"][i])
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=opt, desired_capabilities=dc
    )
    requests.post(
        url="http://localhost:3000/complete", data={"website": df["website"][i]}
    )
    driver.get(r"https://" + df["website"][i])

    # sleep
    time.sleep(40)

    # dictionary collecting logs
    # 1: Logs 2: PageSource
    # dic[df["website"][i]] = []
    # # saving logs in dictionary
    # dic[df["website"][i]].append(driver.get_log("browser"))
    # dic[df["website"][i]].append(driver.page_source)
    # # saving it in csv
    # pd.DataFrame(dic).to_csv("server/output/" + df["website"][i] + "/logs.csv")
    # driver.quit
    driver.quit()


# except:
#     try:
#         driver.quit()
#     except:
#         pass


count = 0

for i in df.index:
    # try:
    # if i < 273:
    #     pass
    # else:

    # clear breakpoints
    f = open(
        "extension/breakpoint.json",
        "w",
    )
    f.write("[]")
    f.close()

    # visit website
    visitWebsite(df)

    # update breakpoints list
    addBreakPoints("server/output/" + df["website"][i])
    # delete previous crawl
    shutil.rmtree("server/output/" + df["website"][i])

    # visit website
    visitWebsite(df)

    count += 1
    with open("logs.txt", "w") as log:
        log.write(str(count))
        log.close()
    print(r"Completed: " + str(i) + " website: " + df["website"][i])
# except:
#     pass
#     print(r"Crashed: " + str(i) + " website: " + df["website"][i])
