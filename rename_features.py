import shutil
import os


def main():
    fold = os.listdir("server/output")
    for f in fold:
        try:
            source = "server/output/" + f + "/features.xlsx"
            target = "node11-features/" + f + ".xlsx"
            shutil.copy(source, target)
        except:
            pass

main()