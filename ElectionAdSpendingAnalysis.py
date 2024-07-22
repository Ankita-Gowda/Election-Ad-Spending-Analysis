#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

results = pd.read_csv(r'C:\Users\91930\Downloads\elections-data\results.csv')
locations = pd.read_csv(r'C:\Users\91930\Downloads\elections-data\locations.csv')
advertisers = pd.read_csv(r'C:\Users\91930\Downloads\elections-data\advertisers.csv')

results.head()


# In[9]:


advertisers.head()



# In[2]:


locations.head()


# In[3]:


#since result data has col named state and location data has col named as location name hwncw mweging the dataset
results['State']= results['State'].str.strip().str.lower()
locations['Location name']=locations['Location name'].str.strip().str.lower()
merged_data = results.merge(
locations,
left_on='State',
right_on='Location name',
how='left')
merged_data.head()


# In[4]:


#looking at total ad spend by state
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_white"


state_ad_spend = merged_data.groupby('State')['Amount spent (INR)'].sum().reset_index()
fig = px.bar(state_ad_spend, x='State', y='Amount spent (INR)',
               color='State',
             labels={'State': 'State', 'Amount spent (INR)': 'Ad Spend (INR)'},
             title='Total Ad Spend by State')

fig.update_layout(xaxis={'categoryorder': 'total descending'},
                  xaxis_tickangle=-90,
                  width=1000,
                  height=800)

fig.show()


# In[9]:


#looking for avg voter turnout
state_voter_turnout = merged_data.groupby('State')['Polled (%)'].mean().reset_index()


fig = px.bar(state_voter_turnout, x='State', y='Polled (%)',
          
             labels={'State': 'State', 'Polled (%)': 'Voter Turnout (%)'},
             title='Average Voter Turnout by State')

fig.update_layout(xaxis={'categoryorder': 'total descending'},
                 xaxis_tickangle=-90,
                 width=1000,
                 height=600)

fig.show()


# In[8]:


#looking at the top 5 parties by ad spend:
advertisers['Amount spent (INR)'] = pd.to_numeric(advertisers['Amount spent (INR)'], errors='coerce')

advertisers.dropna(subset=['Amount spent (INR)'], inplace=True)

party_ad_spend = advertisers.groupby('Page name')['Amount spent (INR)'].sum().sort_values(ascending=False)

top_5_parties = party_ad_spend.head(5).reset_index()

colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

fig = px.pie(top_5_parties, values='Amount spent (INR)', names='Page name',
             title='Top 5 Parties by Ad Spend', color_discrete_sequence=colors,
             labels={'Page name': 'Political Party', 'Amount spent (INR)': 'Ad Spend (INR)'})

fig.update_traces(textinfo='percent')

fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=-0.3
    ),
    title=dict(
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    margin=dict(l=200, r=50, t=100, b=50) 
)

fig.show()


# In[20]:


#checking the correlation between ad spend and voter turnout:
correlation = merged_data[['Amount spent (INR)', 'Polled (%)']].corr()
print(correlation)


# In[7]:


#checking the relationship between ad spend and voter turnout by parliamentary constituency:
merged_constituency_data = results.merge(
    locations,
    left_on='State',
    right_on='Location name',
    how='left'
)

fig = px.scatter(merged_constituency_data, x='Amount spent (INR)', y='Polled (%)',
                 color='State',
                 labels={'Amount spent (INR)': 'Ad Spend (INR)', 'Polled (%)': 'Voter Turnout (%)'},
                 title='Ad Spend and Voter Turnout by Parliamentary Constituency')

fig.update_layout(width=800, height=600)

fig.show()


# In[6]:


# distribution of ad spending:
fig = px.histogram(merged_data, x='Amount spent (INR)', nbins=30, marginal='box',
                   labels={'Amount spent (INR)': 'Ad Spend (INR)'},
                   title='Distribution of Ad Spend')
fig.update_traces(marker=dict(line=dict(color='black', width=1)))
fig.update_layout(bargap=0.1, width=800, height=600)

fig.show()


# In[5]:


#analyzing ad spending and voter turnout by election phase
import plotly.graph_objects as go

phase_analysis = merged_data.groupby('Phase').agg({
    'Amount spent (INR)': 'sum',
    'Polled (%)': 'mean'
}).reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=phase_analysis['Phase'],
    y=phase_analysis['Amount spent (INR)'],
    name='Ad Spend (INR)',
    marker_color='indianred',
    yaxis='y1'
))

fig.add_trace(go.Scatter(
    x=phase_analysis['Phase'],
    y=phase_analysis['Polled (%)'],
    name='Voter Turnout (%)',
    marker_color='lightsalmon',
    yaxis='y2'
))

fig.update_layout(
    title='Ad Spend and Voter Turnout by Election Phase',
    xaxis=dict(title='Election Phase'),
    yaxis=dict(
        title='Ad Spend (INR)',
        titlefont=dict(color='indianred'),
        tickfont=dict(color='indianred')
    ),
    yaxis2=dict(
        title='Voter Turnout (%)',
        titlefont=dict(color='lightsalmon'),
        tickfont=dict(color='lightsalmon'),
        overlaying='y',
        side='right'
    ),
    legend=dict(x=0.1, y=1.1, orientation='h'),
    width=800,
    height=600
)

fig.show()


# In[ ]:




