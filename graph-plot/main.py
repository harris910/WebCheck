from populateGraph import createWebGraph
import networkx as nx


def main():
    createWebGraph("nbcnews.com")
    # createGraphFeatures("forbes.com")


if __name__ == "__main__":
    main()
