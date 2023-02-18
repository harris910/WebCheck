import shutil
import os


def main():
    fold = os.listdir("server/output")
    os.mkdir("node1-callstackFeatures")
    for f in fold:
        try:
            source = "server/output/" + f + "/features.xlsx"
            target = "node1-callstackFeatures/" + f + ".xlsx"
            shutil.copy(source, target)
        except:
            pass


main()
