import pandas as pd
from funs import *

csvout = 'data-request-i4c-merged.csv'

data_request = pd.read_csv('data-request.csv')
data_request_fpsurbrcc = pd.read_csv('data-request-fpsurbrcc.csv')
data_request_fpsconv = pd.read_csv('data-request-fpsconv.csv')

data_request.set_index(['out_name', 'frequency'], inplace=True)
data_request_fpsurbrcc.set_index(['out_name', 'frequency'], inplace=True)
data_request_fpsconv.set_index(['out_name', 'frequency'], inplace=True)

data_request['priority'] = 'I4C-' + data_request['priority'].astype(str)
data_request_fpsurbrcc.rename(columns={'priority': 'priority-urb'}, inplace=True)
data_request_fpsurbrcc['priority-urb'] = 'URB-' + data_request_fpsurbrcc['priority-urb'].astype(str)
data_request_fpsconv.rename(columns={'priority': 'priority-conv'}, inplace=True)
data_request_fpsconv['priority-conv'] = 'CONV-' + data_request_fpsconv['priority-conv'].astype(str)

merged_df = data_request.combine_first(data_request_fpsurbrcc).combine_first(data_request_fpsconv)
(
    merged_df
        .loc[:,['units', 'long_name', 'priority', 'priority-urb', 'priority-conv', 'comment']]
        .reset_index()
        .to_csv(csvout, index=False)
)

csv2datatable(
    csvout,
    f'docs/{csvout.replace(".csv",".html")}',
    title='I4C CPRCM requested variable list',
    intro='''
        This table shows the <a href="https://github.com/impetus4change/T32-CPRCM/blob/main/data-request.csv">data request</a>
        from the different I4C work packages and includes also the variables requested from the
        <a href="https://github.com/impetus4change/T32-CPRCM/blob/main/data-request-fpsurbrcc.csv">CORDEX FPS-URB-RCC</a> and
        <a href="https://github.com/impetus4change/T32-CPRCM/blob/main/data-request-fpsconv.csv">FPS-CONV</a> initiatives.
        Note: To avoid duplicated entries, the frequency shown for some variables in the data request from the
        FPS-CONV initiative has been adapted to match the highest frequency requested by the other two ongoing
        activities.''',
    rename_fields = {}
)
