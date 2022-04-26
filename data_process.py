import csv
from datetime import *
import re

weekday = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}


def data_process(path):
    data_list = []
    column_name = {}
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            if count == 3001:
                break
            if count == 0:
                for i in range(len(row)):
                    column_name[i] = row[i]
                # column_name = [row[2], row[5], row[7], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19]]
                print(column_name)
                count+=1
                continue
            data_row = []
            if len(row[2]) != 0:
                data_row.append("{}_{}".format(column_name[2],row[2]))
            if len(row[5]) != 0:
                data_row.append("{}_{}".format(column_name[5],row[5]))
            if len(row[7]) != 0:
                occ_date_time = row[7]
                obj = datetime.strptime(occ_date_time, '%m/%d/%Y %I:%M:%S %p')
                data_row.append("Occured_on_{}".format(weekday[obj.weekday()]))
                time_hour = obj.hour
                time_range = "Occured_Between_{}_to_{}".format(time_hour, time_hour+1)
                data_row.append(time_range)
            if len(row[9]) != 0:
                data_row.append("{}_{}".format(column_name[9],row[9]))
            if len(row[10]) != 0:
                data_row.append("{}_{}".format(column_name[10],row[10]))
            if len(row[11]) != 0:
                delay_str = re.findall(r'\d+', row[11])
                if len(delay_str) != 0:
                    delay_int = int(delay_str[-1])
                    delay_range = ""
                    if delay_int <= 15:
                        delay_range = "0-15"
                    elif delay_int <=30:
                        delay_range = "16-30"
                    elif delay_int <=60:
                        delay_range = "31-60"
                    else:
                        delay_range = "61 and more"
                    data_row.append("Delayed_{}_MINs".format(delay_range))
            if len(row[12]) != 0:
                stu = int(row[12])
                stu_range = ""
                if stu <= 0:
                    stu_range = "0"
                elif stu <=10:
                    stu_range = "1-10"
                elif stu <= 20:
                    stu_range = "11-20"
                elif stu <= 50:
                    stu_range = "21-50"
                else:
                    stu_range = "51 and more"
                data_row.append("{}_Students".format(stu_range))
            if len(row[13]) != 0:
                data_row.append("{}_{}".format(column_name[13],row[13]))
            if len(row[14]) != 0:
                data_row.append("{}_{}".format(column_name[14],row[14]))
            if len(row[15]) != 0:
                data_row.append("{}_{}".format(column_name[15],row[15]))
            if len(row[19]) != 0:
                data_row.append("{}_{}".format("Result",row[19]))
            data_list.append(data_row)
            count += 1
            # print(', '.join(row))
    # print(data_list)

    with open('INTEGRATED-DATASET.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_list)


# def data_process_large(path):
#     data_list = []
#     with open(path, newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         count = 0
#         for row in reader:
#             data_list.append([row[2], row[5], row[9], row[19]])
#             count += 1
#
#     with open('INTEGRATED-DATASET-large.csv', 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(data_list)


if __name__ == '__main__':
    path = 'Bus_Breakdown_and_Delays.csv'
    data_process(path)
    # data_process_large(path)
