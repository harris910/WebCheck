from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import shutil

# from pyvirtualdisplay import Display
import pandas as pd
import requests
import os


# virtual display
# display = Display(visible=0, size=(800, 600))
# display.start()

# df = pd.read_csv(r'3.csv')
# extractDigits(os.listdir('/home/student/TrackerSift/UserStudy/output'))
df = pd.DataFrame([["nbcnews.com"]], columns=["website"])

# helper functions for breakpoints
def getInitiator(stack):
    if len(stack["callFrames"]) != 0:
        if (
            "chrome-extension" not in stack["callFrames"][0]["url"]
            and stack["callFrames"][0]["url"] != ""
        ):
            return {
                "lineNumber": stack["callFrames"][0]["lineNumber"],
                "url": stack["callFrames"][0]["url"],
                "columnNumber": stack["callFrames"][0]["columnNumber"],
            }
    else:
        return getInitiator(stack["parent"])


def addBreakPoints(filename):
    arr = []
    with open(filename) as file:
        for line in file:
            dataset = json.loads(line)
            if dataset["call_stack"]["type"] == "script":
                val = getInitiator(dataset["call_stack"]["stack"])
                if val is not None:
                    arr.append(val)
    f = open(
        "C:/Users/Hadiy/OneDrive/Desktop/webpage-crawler-extension/extension/breakpoint.json",
        "w",
    )
    f.write(str(arr).replace("'", '"'))
    f.close()


# selenium to visit website and get logs
def visitWebsite(df):
    dic = {}
    # extension filepath
    ext_file = "C:/Users/Hadiy/OneDrive/Desktop/webpage-crawler-extension/extension"

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
    time.sleep(20)

    # dictionary collecting logs
    # 1: Logs 2: PageSource
    dic[df["website"][i]] = []
    # saving logs in dictionary
    dic[df["website"][i]].append(driver.get_log("browser"))
    dic[df["website"][i]].append(driver.page_source)
    # saving it in csv
    pd.DataFrame(dic).to_csv("server/output/" + df["website"][i] + "/logs.csv")
    # driver.quit
    driver.quit()


count = 0

for i in df.index:
    try:
        # if i < 273:
        #     pass
        # else:

        # clear breakpoints
        f = open(
            "C:/Users/Hadiy/OneDrive/Desktop/webpage-crawler-extension/extension/breakpoint.json",
            "w",
        )
        f.write("[]")
        f.close()

        # visit website
        visitWebsite(df)

        # update breakpoints list
        addBreakPoints("server/output/" + df["website"][i] + "/request.json")
        # delete previous crawl
        shutil.rmtree("server/output/" + df["website"][i])

        # visit website
        visitWebsite(df)

        count += 1
        with open("logs.txt", "w") as log:
            log.write(str(count))
            log.close()
        print(r"Completed: " + str(i) + " website: " + df["website"][i])
    except:
        try:
            driver.quit()
        except:
            pass
        print(r"Crashed: " + str(i) + " website: " + df["website"][i])
