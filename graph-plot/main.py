from populateGraph import createWebGraph
import networkx as nx
import os


def main():
    # createWebGraph("nbcnews.com")
    # createGraphFeatures("forbes.com")
    fold = os.listdir(
        "server/output"
    )
    for f in fold:
        try:
            print("graph-plot: ", f)
            createWebGraph(f)
        except:
            print("not-graph-plot: ", f)


if __name__ == "__main__":
    main()
