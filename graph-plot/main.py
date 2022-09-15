from populateGraph import createWebGraph
from makeFeatures import createGraphFeatures
import networkx as nx


def main():
    createWebGraph("bundle.com")
    # createGraphFeatures("forbes.com")


if __name__ == "__main__":
    main()
