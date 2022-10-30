from populateGraph import createWebGraph
import networkx as nx


def main():
    createWebGraph("dailymail.co.uk")
    # createGraphFeatures("forbes.com")


if __name__ == "__main__":
    main()
