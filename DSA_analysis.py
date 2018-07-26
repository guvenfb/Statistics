import sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from os import listdir


def update_dictionary(dd, key, value):
    if key in dd:
        dd[key].append(value)
    else:
        dd[key] = [value]


csv_file_folder = r"U:\YAS_tasks\YAS\WW20.5 DSA analysis\output\\"
csv2_files_list = listdir(csv_file_folder)

dsa_analysis = dict()  # initialize the dictionary
for csv_file in csv2_files_list:  # for each csv file

    print(csv_file)
    df_dsa_raw = pd.read_csv(csv_file_folder + csv_file)
    col_names = df_dsa_raw.columns  # get the column names; the last one is the layerID!
    no_columns = len(col_names)  # first column is scribeID, last column is the layer of interest, rest is hit-back

    layer_col_name = col_names[-1]
    layer_id = layer_col_name.split("_")[1]  # 6_4GTREC is an example

    # delete the rows with missing values
    df_dsa_raw.dropna(subset=[layer_col_name], inplace=True)  # drop the rows if the layer column has missing values

    # now, for each hit-back column, count the number of wafers that would become DSA!
    update_dictionary(dsa_analysis, "layerID", layer_id)
    update_dictionary(dsa_analysis, "action", "current")
    update_dictionary(dsa_analysis, "no wafers", df_dsa_raw.shape[0])
    update_dictionary(dsa_analysis, "no DSA wafers", df_dsa_raw.shape[0] - sum(df_dsa_raw.isnull().any(axis=1)))  # sum of rows with NaN
    update_dictionary(dsa_analysis, "drop", "None")
    for col_order in range(1, no_columns-1, 1):  # skip the last column

        target_hit_back_column = col_names[col_order]  # this is the col name of that hit-back layer
        if len(target_hit_back_column.split("_")[0]) == ".":
            print(target_hit_back_column)
        # print(target_hit_back_column)

        df_dsa_raw.drop([target_hit_back_column], axis=1, inplace=True)  # drop the first hit back layer!
        update_dictionary(dsa_analysis, "layerID", layer_id)
        update_dictionary(dsa_analysis, "action", "drop " + str(col_order) + " hit-back layer")
        update_dictionary(dsa_analysis, "no wafers", df_dsa_raw.shape[0])
        update_dictionary(dsa_analysis, "no DSA wafers", df_dsa_raw.shape[0] - sum(df_dsa_raw.isnull().any(axis=1)))  # sum of rows with NaN
        update_dictionary(dsa_analysis, "drop", target_hit_back_column.split("_")[1])


correlation_results = pd.DataFrame(dsa_analysis)
correlation_results.to_csv(r"U:\YAS_tasks\YAS\WW20.5 DSA analysis\dsa_analysis_results.csv")

'''
plt.scatter(corr_table["4BKTCN"], corr_table["Impact"])
plt.xlabel("layer EDI")
plt.ylabel("eol impact")
plt.legend(loc=2)
plt.show()
'''