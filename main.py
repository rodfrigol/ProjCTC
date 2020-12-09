import pandas
import math as m
import csv

train_results_read = open("train_results.txt", "r")
test = pandas.read_csv("data/test.csv")
submission = {
    '"id"' : [],
    '"median_house_value"' : []
}

train_results_read.readline()
current_min_exp = train_results_read.readline()
train_results_read.close()

current_min_exp = current_min_exp.replace("r[2]", "r['median_income']")
current_min_exp = current_min_exp.replace("r[3]", "r['housing_median_age']")
current_min_exp = current_min_exp.replace("r[4]", "r['total_rooms']")
current_min_exp = current_min_exp.replace("r[5]", "r['total_bedrooms']")
current_min_exp = current_min_exp.replace("r[6]", "r['population']")
current_min_exp = current_min_exp.replace("r[7]", "r['households']")
current_min_exp = current_min_exp.replace("r[8]", "r['latitude']")
current_min_exp = current_min_exp.replace("r[9]", "r['longitude']")

for i, r in test.iterrows():
    median_house_value = eval(current_min_exp)
    submission['"id"'].append(int(r['id']))
    submission['"median_house_value"'].append(median_house_value)

pandas.DataFrame(submission).to_csv('data/submission.csv', index = False, quoting=csv.QUOTE_NONE)