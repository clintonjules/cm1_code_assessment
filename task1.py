import pandas as pd
import plotly.express as px

df = pd.read_csv('message_data.csv')

# After reading in the data, convert the message time into objects
# Only dates are needed
df['message_time'] = pd.to_datetime(df['message_time'], format='ISO8601').dt.date

# Creates all the stats for the task in the form of a dataframe

date_stats = {}
used_ids = set()
new_ids = []

for _, row in df.iterrows():
    if row['message_time'] not in date_stats.keys():
        if row['author_id'] not in used_ids:
            date_stats[row['message_time']] = {'message': [row['message_id']], 'author': [row['author_id']], 'new_ids': [row['author_id']]}
            
        else:
            date_stats[row['message_time']] = {'message': [row['message_id']], 'author': [row['author_id']], 'new_ids': []}
    
    else:
        date_stats[row['message_time']]['message'].append(row['message_id'])
        date_stats[row['message_time']]['author'].append(row['author_id'])
        
        if row['author_id'] not in used_ids:
            date_stats[row['message_time']]['new_ids'].append(row['author_id'])
        
    used_ids.add(row['author_id'])
        
    assert len(date_stats[row['message_time']]['message']) == len(date_stats[row['message_time']]['author'])
    
#  Creates the secondary stats for new user percentages
date_message_info = pd.DataFrame(date_stats).transpose().reset_index().rename(columns={'index':'date'})
date_message_info['message_total'] = date_message_info['message'].str.len()
date_message_info['first_message_total'] = date_message_info['new_ids'].str.len()
date_message_info['first_message_percentage'] = round((date_message_info['new_ids'].str.len() / date_message_info['message_total']) * 100, 3)

# Creates the plot
fig = px.line(date_message_info, x='date', y="message_total")
fig.add_scatter(x=date_message_info['date'], y=date_message_info['first_message_total'], text=date_message_info['first_message_percentage'], name='Percent of first messages') 

fig.show()