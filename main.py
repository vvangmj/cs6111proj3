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



if __name__ == '__main__':
    path = args.f
    min_sup = args.s
    min_conf = args.c

    data = read_file("INTEGRATED-DATASET.csv")
    large_item, conf_rules = get_large_item(data, min_sup, min_conf)
    
    text_file = open("output.txt", "w")
    m = text_file.write("=============== Frequent Itemsets (min_sup={})===============\n".format(min_sup))

    print("Number of Large items:", len(large_item))
    print("=============== Frequent Itemsets (min_sup={})===============\n".format(min_sup))

    large_item = list(sorted(large_item, key=lambda x: x[1], reverse=True))
    for items in large_item:
        print(list(items[0]), ",", "{0:.4f}%".format(items[1]*100))
        n = text_file.write("{0}, {1:.4f}%\n".format(list(items[0]), items[1]*100))

    n = text_file.write("\n")
    m = text_file.write("=============== High-confidence Association Rules (min_conf={})===============\n".format(
        min_conf))

    conf_rules = sorted(conf_rules, key=lambda x: x[3], reverse=True)
    print("=============== High-confidence association rules (min_conf={})===============".format(min_conf))
    for rule in conf_rules:
        l, r, sup, conf = rule[0], rule[1], rule[2], rule[3]
        print("{0}=>{1} (Conf:{2:.4f}%, Supp:{3:.4f}%)".format(l, r, conf*100, sup*100))
        n = text_file.write("{0}=>{1} (Conf:{2:.4f}%, Supp:{3:.4f}%)\n".format(l, r, conf*100, sup*100))
        
    text_file.close()


