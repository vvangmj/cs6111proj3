from collections import defaultdict
import argparse
from apriori import *

parser = argparse.ArgumentParser()

parser.add_argument('--f', type=str, default='INTEGRATED-DATASET.csv',
                    help='INTEGRATED-DATASET file from which to extract association rules')
parser.add_argument('--s', type=float, default=0.05,
                    help='Float number representing minimum support min_sup. value range = (0,1)')
parser.add_argument('--c', type=float, default=0.5,
                    help='Float number representing minimum confidence min_conf. value range = (0,1)')
args = parser.parse_args()


# def print_parameters():
#     print("Parameters:")
#     print("Client key  = ", args.API_KEY)
#     print("Engine key  = ", args.engine_id)
#     print("Relation  = ", internal_name[args.r])
#     print("Threshold = ", args.t)
#     print("Query  = ", args.q)
#     print("# of Tuples = ", args.k)
#     print("Loading necessary libraries; This should take a minute or so ...")


if __name__ == '__main__':
    path = args.f
    min_sup = args.s
    min_conf = args.c

    data = read_file("INTEGRATED-DATASET.csv")
    large_item = get_large_item(data)
    print("Number of Large items:", len(large_item))
    for items in large_item:
        print(items)

