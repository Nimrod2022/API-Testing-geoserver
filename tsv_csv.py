import pandas as pd

tsv_file = 'tps00176.tsv'

# reading given tsv file
csv_table = pd.read_table(tsv_file, sep='\t')

# converting tsv file into csv
csv_table.to_csv('tps00176.csv', index=False)

# output
print("Successfully made csv file")