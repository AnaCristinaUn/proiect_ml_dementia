#importing necessary libraries
import pandas as pd

#holds the dataset 
data = pd.read_csv("data/dataset.csv")

print("Number of samples:", len(data))

print("\nClass distribution:")
#value_counts() method is used to count the occurrences of each unique value in the "label" column.
#it represents the class distribution in the dataset. 
print(data["label"].value_counts())

#calculating the length of each sentence and storing it in a new column called "length".
data["length"] = data["sentence"].apply(lambda x: len(x.split()))

print("\nAverage sentence length:", data["length"].mean())