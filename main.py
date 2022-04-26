from collections import defaultdict
import argparse
from apriori import *

parser = argparse.ArgumentParser()

parser.add_argument('--f', type=str, default='INTEGRATED-DATASET.csv',
                    help='INTEGRATED-DATASET file from which to extract association rules')
parser.add_argument('--s', type=float, default=0.2,
                    help='Float number representing minimum support min_sup. value range = (0,1)')
parser.add_argument('--c', type=float, default=0.9,
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
    large_item, conf_rules = get_large_item(data, min_sup, min_conf)
    with open("output.txt", "w", newline="") as f:
        writer = csv.writer(f, delimiter=" ")
        writer.writerow(["=====Frequent itemsets (min_sup={})=====".format(min_sup)])

    print("Number of Large items:", len(large_item))
    print("=====Frequent itemsets (min_sup={})=====".format(min_sup))

    for items in large_item:
        print(items)
        with open("output.txt", "a", newline="") as f:
            writer = csv.writer(f, delimiter=" ")
            writer.writerow([items[0],"{}%".format(items[1]*100)])

    with open("output.txt", "a", newline="") as f:
        writer = csv.writer(f, delimiter=" ")
        writer.writerow(["=====High-confidence association rules (min_conf={})=====".format(min_conf)])

    conf_rules = sorted(conf_rules, key=lambda x: x[3], reverse=True)
    print("=====High-confidence association rules (min_conf={})=====".format(min_conf))
    for rule in conf_rules:
        l, r, sup, conf = rule[0], rule[1], rule[2], rule[3]
        print("{}=>{}(Conf:{},Supp:{})".format(l, r, conf, sup))
        with open("output.txt", "a", newline="") as f:
            writer = csv.writer(f, delimiter=" ")
            writer.writerow(["{}=>{}(Conf:{}%,Supp:{}%)".format(l, r, conf*100, sup*100)])


