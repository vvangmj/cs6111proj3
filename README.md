# COMS6111 Project 3

## Team Members

- Zihuan Wu (zw2771)
- Mingjun Wang (mw3542)

## Files

```
- proj3
    - main.py
    - apriori.py
    - INTEGRATED-DATASET.csv

- INTEGRATED-DATASET.csv
- README.md
```

## How to Run

In order to run the system, you can run
```
python main.py --f <dataset_filename> --s <min_sup> --c <min_con>
```

Or just
```
python main.py
```
**Note** that in the second case, the default values of min support and min confidence area 0.2 and 0.9 respectively.


## Dependencies Installation

- make sure your Python version is 3.8.12 or newer
- numpy: run `pip install numpy==1.22.2`

## Dataset
### Original Data Source
[Bus Breakdown and Delays](https://data.cityofnewyork.us/Transportation/Bus-Breakdown-and-Delays/ez4e-fazm)

It collects information from school bus vendors operating out in the field when encounter delays during the route. 

### Mapping Strategy
The final INTEGRATED-DATASET file has 3000 rows of data, and have at most have 12 items(columns). The detailed process is shown as following:

1. We extract the top 3001 rows from the original dataset containing the header of the data(without any sorting or filtering).
2. To make the integrated dataset only contain useful information, we select 11 columns from original before further process. The following format is the column name followed by the column index (begin from 0): 
    - Run_Type 2
    - Reason 5
    - Occurred_On 7
    - Boro 9
    - Bus_Company_Name 10
    - How_Long_Delayed 11
    - Number_Of_Students_On_The_Bus 12
    - Has_Contractor_Notified_Schools 13
    - Has_Contractor_Notified_Parents 14
    - Have_You_Alerted_OPT 15
    - Breakdown_or_Running_Late 19
3. For column "Occured_On", it describe the Date and Time the incident occurr. We could split it into two columns: Weekday Name, Time Range. The former have 7 values: "Mon",...,"Sun". And the later is contructed by getting the hour "h" of the time and then set the range as from "h" to "h+1". For example, if the orginal data is "11/05/2015 08:10:00 AM", then the week name is "Thu" and time range is "8_to_9". 
4. For numerical column How_Long_Delayed, we set range "0-15_MINs", "16-30_MINs", "31-60_MINs", "61 and more_MINs" to discretize numerical values.
5. For numerical column Number_Of_Students_On_The_Bus, we also set range "0_Students", "1-10_Students", "11-20_Students", "21-50_Students", "51 and more_Students" to discretize numerical values. 
6. To make each item in the integrated datafile easy to understand, we concatenate the corresponding column name with the actual value. e.g. "Reason_Heavy Traffic", "Boro_Bronx"
7. So there are at total 3000 rows in the final integrated file. each row will have at most 12 following columns (Notice that we altered the "Breakdown_or_Running_Late" to "Reason" for short): 
    - Run_Type
    - Reason
    - Occurred_on_{weekname}
    - Occured_Between_{time range}
    - Boro
    - Bus_Company_Name
    - Delayed_{time range}
    - {Number range}_Students
    - Notified_Schools
    - Notified_Parents
    - Alerted_OPT
    - Result

### Justification
Bus Breakdown and Delays collects the information from school bus vendors operating out in the field when encounter delays during the route. 

There are various kinds of reasons that could contribute the breakdown and delays of buses. And there might exist some factors are the causal or effect of breakdown and delay. For example, maybe some specific busing service will more likely to have delayed; maybe on delay will happen more on Monday morning or 4-5pm in the afternoon due to the heavy traffic; And when the delay happened, will the bus driver contact the schools or parents, or what bus vendors will more likely to be responsible and notify the school and parents. We could finding rules like above by analyzing this dataset, and can prevent the delay or breakdown by eliminating the item that appear with "delay or breakdown" in the association rules. And there will also have underlying relationship among the time, the transportation and the districts.


## Internal Design
### Frequent(large) Itemsets Generation
We use the original A-priori algorithm to collect the frequent(large) itemsets iteratively. 

For each frequent k-itemsets (including the 1-itemsets), we retain two kinds of container: "k_itemset_list" and "k_itemset_set". 
- "k_itemset_list": A List where each element is also a list composed of the set of 1-itemset and its support value. Format for each row:  [ set - containing the large k-itemset , float - support value]. This data structure is useful when generating the (k+1) itemsets candidates and generating association rules. 
- "k_itemset_set": A set, where each element is a tuple composed of only k item. Items in each tuple are sorted in alphabetic ascending order (to prevent repeated insertion and counting). This data structure is useful when pruning the (k+1) itemsets candidates. 

Traversing through each row of our INTEGRATED-DATASET, we count item occurrences among the whole dataset to determine large 1-itemsets and store it both in a list and a set. Besides, we use a dict, "basket_allitem", to record all items in a market basket (row).

For frequent k-itemsets, we implement the Apriori Candidate Generation algorithm. We initialize a set "candidate_k" to contain the itemsets. To get all the possible k-itemsets from k-1 itemsets, we calculate symmetric difference between every two sets "I" and "J" in the k-1 itemset_list. Then union the difference with either k-1 itemset ("I" or "J") to generate the new k-itemsets candidate and add it into set "candidate_k". 

To prune the candidates, we extract the (k-1)-sized subset for each candidates, and exam its existence in the set typed "(k-1)-itemsets". We only contain the candidates that also exist in the "(k-1)-itemsets". 

After getting the pruned candidates, we generate the frequent large k-itemset by traversing through each row of the dataset, and calculating the total number of appearance of each candidate with the help of "basket_allitem".

### Association Rules Generation
We generate association rules based on the frequent itemsets generated in the last step.

For each itemset in the frequent itemsets (except the 1-itemsets), we generate all subsets with a size of 1 since for this assignment, we are specifically required to generate only association rules with exactly one item on the right side. 

For each subset, we put the difference between the whole itemset and it on the left-hand side and itself on the right-hand side which forms our potential association rule candidate. Then for each candidate, we calculate their confidence scores using the formula of supp(itemset)/supp(left) and only keep those whose scores are above the given threshold. After all iterations, we will obtain a list of all valid association rules. 



