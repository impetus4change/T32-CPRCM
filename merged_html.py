import pandas as pd
from funs import *

csvout = 'data-request-i4c-fpsurbrcc.csv'

data_request = pd.read_csv('data-request.csv')
data_request_fpsurbrcc = pd.read_csv('data-request-fpsurbrcc.csv')

data_request.set_index(['out_name', 'frequency'], inplace=True)
data_request_fpsurbrcc.set_index(['out_name', 'frequency'], inplace=True)

data_request['priority'] = 'I4C-' + data_request['priority'].astype(str)
data_request_fpsurbrcc.rename(columns={'priority': 'priority-fps'}, inplace=True)
data_request_fpsurbrcc['priority-fps'] = 'FPS-' + data_request_fpsurbrcc['priority-fps'].astype(str)

merged_df = data_request.combine_first(data_request_fpsurbrcc)
(
    merged_df
        .loc[:,['units', 'long_name', 'priority', 'priority-fps', 'comment']]
        .reset_index()
        .to_csv(csvout, index=False)
)

csv2datatable(
    csvout,
    f'docs/{csvout.replace(".csv",".html")}',
    title='I4C CPRCM requested variable list',
    intro='This table includes also the priority variables from the CORDEX FPS-URB-RCC',
    rename_fields = {}
)