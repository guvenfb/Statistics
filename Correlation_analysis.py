import sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

def update_dictionary(dd, key, value):
    if key in dd:
        dd[key].append(value)
    else:
        dd[key] = [value]

riso_table = pd.read_csv(r"D:\YAS_Tasks\2018WW20.5 edi data from Amit\92_wafers_EOL_impact.csv")
# layer_edi_table = pd.read_csv(r"D:\YAS_Tasks\2018WW20.5 edi data from Amit\mean_edi_over_layers.txt")
# layer_edi_table = pd.read_csv(r"D:\YAS_Tasks\2018WW20.5 edi data from Amit\cumulative_edi_over_layers.txt")
layer_edi_table = pd.read_csv(r"D:\YAS_Tasks\2018WW20.5 edi data from Amit\DIELEVEL_DEFECT_COUNT_BY_LAYER.txt")

split_df = pd.pivot_table(layer_edi_table, values='CCX1_COUNT_BY_DIE', index=['DieID'], columns=['LAYER_ID'])
# fill the missing values with 0
split_df.fillna(0, inplace=True)


riso_table.set_index("DieID", inplace=True)
corr_table = split_df.join(riso_table)
# corr_table.to_csv(r"U:\YAS_tasks\YAS\WW20.2 92 Wafers EOL impact\cumm_corr_table.csv")  # <-- save to the folder

r2_score(corr_table["4BKTCN"], corr_table["Impact"], multioutput='variance_weighted')
# corr_table['4BKTCN'].corr(corr_table['Impact'])
# corr_table.groupby(['Zone','Quadrant'])[['4BKTCN','Impact']].corr()

column_names = list(corr_table.columns)
layer_names = list()
for col_name in column_names:
    if col_name[0] == "4":
        layer_names.append(col_name)


# update_dictionary(df_target_formula, "layerID", layer)
correlation_tableau = dict()
for layer in layer_names:  # for each layer, calculate the correlation by zone and quadrant etc.

    corr_coeff = corr_table[layer].corr(corr_table['Impact'])
    update_dictionary(correlation_tableau, "layerID", layer)
    update_dictionary(correlation_tableau, "zone", "entire wafer")
    update_dictionary(correlation_tableau, "quadrant", "N/A")
    update_dictionary(correlation_tableau, "correlation coefficient", corr_coeff)

    # series object following group by zone
    df_by_zone = corr_table.groupby('ZONE')[layer].corr(corr_table["Impact"])
    for zone, cor_val in df_by_zone.iteritems():
        update_dictionary(correlation_tableau, "layerID", layer)
        update_dictionary(correlation_tableau, "zone", zone)
        update_dictionary(correlation_tableau, "quadrant", "N/A")
        update_dictionary(correlation_tableau, "correlation coefficient", cor_val)

    # another series following group by zone and quadrant
    df_by_zone_quadrant = corr_table.groupby(['ZONE','QUADRANT'])[layer].corr(corr_table["Impact"])
    for zone_quad, cor_val in df_by_zone_quadrant.iteritems():
        zone = zone_quad[0]
        quadrant = zone_quad[1]
        update_dictionary(correlation_tableau, "layerID", layer)
        update_dictionary(correlation_tableau, "zone", zone)
        update_dictionary(correlation_tableau, "quadrant", quadrant)
        update_dictionary(correlation_tableau, "correlation coefficient", cor_val)

correlation_results = pd.DataFrame(correlation_tableau)
correlation_results.to_csv(r"U:\YAS_tasks\YAS\WW20.2 92 Wafers EOL impact\def_count_correlation_results.csv")

'''
plt.scatter(corr_table["4BKTCN"], corr_table["Impact"])
plt.xlabel("layer EDI")
plt.ylabel("eol impact")
plt.legend(loc=2)
plt.show()
'''