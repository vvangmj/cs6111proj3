import csv
import itertools
from collections import defaultdict
from itertools import combinations, chain
# min_sup = 0.05


def read_file(path):
    data = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data


# Count item occurrences to determine large 1-itemsets
def first_pass(data, min_sup):
    tot_num = len(data)
    threshold = round(tot_num * min_sup)
    item_count = {}

    # one_itemset_list: A list recording large 1-itemsets and support value
    # format for each row:  [ set - containing the itemset , float - support value]
    one_itemset_list = []
    one_itemset_dict = defaultdict(float)

    # one_itemset_set: A set recording large 1-itemsets.
    # format for each element: tuple (whose size is 1)
    one_itemset_set = set()

    # basket_allitem: Use a dict to record all items in a market basket (row).
    # format: Key : int - basket No; Value : set - containing all the items in tha basket
    basket_allitem = {}

    count = 0
    for basket in data:
        basket_allitem[count] = set()
        for item in basket:
            if item not in item_count:
                item_count[item] = 0
            item_count[item] += 1
            basket_allitem[count].add(item)
        count += 1
    for item in item_count:
        if item_count[item] >= threshold:
            one_itemset_list.append([{item}, float(item_count[item]/tot_num)])
            one_itemset_dict[(item,)] = float(item_count[item]/tot_num)
            one_itemset_set.add((item,))
            # one_itemset[[item]] = float(item_count[item]/tot_num)
    return one_itemset_list, one_itemset_set, basket_allitem, one_itemset_dict


# Apriori Candidate Generation
def apriori_gen(itemset_list, itemset_set, k):
    # All the elements in the candidate_k are tuples (with size k).
    # Each tuple represent an k-itemset that generated from k-1 large itemsets.
    # items in each tuple are sorted in alphabetic ascending order (to prevent repeated insertion and counting).
    candidate_k = set()

    # Join Step
    for item_i in itemset_list:
        for item_j in itemset_list:
            # Get symmetric difference of two sets
            diff = item_i[0] ^ item_j[0]
            if len(diff) == 2:
                new_cand = item_i[0].union(diff)
                new_cand = sorted(new_cand)
                candidate_k.add(tuple(new_cand))
    print("Candidate size(before prune):", len(candidate_k))
    # Prune Step - Check all subsets of these itemsets are frequent or not
    copy_candidate_k = candidate_k.copy()
    for cand in copy_candidate_k:
        subsets = list(itertools.combinations(cand, k-1))
        for sub in subsets:
            sub = tuple(sorted(sub))
            if sub not in itemset_set:
                candidate_k.discard(cand)
                break
    print("Candidate size(after prune):", len(candidate_k))
    return candidate_k


def k_pass(itemset_list, itemset_set, basket_allitem, k, min_sup):
    print("Processing ... k =",k)
    tot_num = len(basket_allitem)
    threshold = round(tot_num * min_sup)

    candidates = apriori_gen(itemset_list, itemset_set, k)

    # candi_count:
    # Key: candidate itemsets tuple. Value: number of baskets that contain candidate itemsets
    candi_count = {}

    # k_itemset_list: A list recording large k-itemsets and support value
    # format for each row:  [ set - containing the large k-itemset , float - support value]
    k_itemset_list = []
    k_itemset_dict = defaultdict(float)
    # k_itemset_set: A set recording large k-itemsets.
    # format for each element: tuple (whose size is k)
    # items in each tuple are sorted in alphabetic ascending order (to prevent repeated insertion and counting).
    k_itemset_set = set()

    # Check the support score for each candidate k-itemset
    for cand in candidates:
        candi_count[cand] = 0
        # Iterate through all the baskets in dataset
        for i in basket_allitem:
            findit = True
            for single_item in cand:
                if single_item not in basket_allitem[i]:
                    findit = False
                    break
            if findit:
                candi_count[cand] += 1
        if candi_count[cand] >= threshold:
            # print(candi_count[cand])
            k_itemset_list.append([set(cand), float(candi_count[cand]/tot_num)])
            k_itemset_dict[tuple(cand)] = float(candi_count[cand]/tot_num)
            k_itemset_set.add(cand)
    print("k-large itemset L(k) size:", len(k_itemset_list))
    return k_itemset_list, k_itemset_set, k_itemset_dict


def get_large_item(data, min_sup, min_conf):
    # format of elements in conf_rules is (LHS, RHS, supp, conf)
    large_item, conf_rules = [], []
    large_item_sup_dict = defaultdict(float)
    k_itemset_list, k_itemset_set, basket_allitem, k_itemset_dict = first_pass(data, min_sup)
    large_item += k_itemset_list
    large_item_sup_dict.update(k_itemset_dict)
    k = 2
    while True:
        k_itemset_list, k_itemset_set, k_itemset_dict = k_pass(k_itemset_list, k_itemset_set, basket_allitem, k, min_sup)
        k += 1
        # print(k_itemset_list)
        if len(k_itemset_list) == 0:
            break
        large_item += k_itemset_list
        large_item_sup_dict.update(k_itemset_dict)
        for item in k_itemset_set:
            subsets = apriori_powerset(item)
            for subset in subsets:
                left, right = subset, set(item).difference(subset)
                support = large_item_sup_dict[tuple(item)]
                confidence = support / large_item_sup_dict[tuple(left)]
                if confidence >= min_conf:
                    conf_rules.append([list(left), list(right), support, confidence])
    return large_item, conf_rules


def apriori_powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s))))


if __name__ == '__main__':
    data = read_file("INTEGRATED-DATASET.csv")
    large_item = get_large_item(data)
    print(len(large_item))
    for items in large_item:
        print(items)
    # large_item = []
    # k_itemset_list, k_itemset_set, basket_allitem = first_pass(data, min_sup)
    # large_item += k_itemset_list
    # k = 2
    # while True:
    #     k_itemset_list, k_itemset_set = k_pass(k_itemset_list, k_itemset_set,basket_allitem, k, min_sup)
    #     k += 1
    #     # print(k_itemset_list)
    #     if len(k_itemset_list) == 0:
    #         break
    #     large_item += k_itemset_list
    # print(len(large_item))
    # for items in large_item:
    #     print(items)