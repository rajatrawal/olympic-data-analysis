import numpy as np
# def medal_tally(df):
    # medal_tally = df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Medal','Event',])
    # medal_tally = medal_tally.groupby('region').sum()[['Gold',"Silver",'Bronze']].sort_values('Gold',ascending=False).reset_index()
    # medal_tally['total']=medal_tally['Gold']+medal_tally['Bronze']+medal_tally['Silver']
    # medal_tally[['Gold',"Silver",'Bronze','total']] = medal_tally[['Gold',"Silver",'Bronze','total']].astype(int)
    # return medal_tally

def fetch_medal_tally(df,year,country):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Medal','Event',])
    flag =0
    if year=='Overall' and country == "Overall":
        temp_df = medal_tally
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_tally[medal_tally['Year'] == int(year)]
    elif year == 'Overall' and country != 'Overall':
        flag =1
        temp_df = medal_tally[medal_tally['region'] == country]
    elif year != 'Overall' and country != 'Overall':
        temp_df = medal_tally[(medal_tally['Year'] == int(year)) & (medal_tally['region']==country)]
    if flag ==1:
        x= temp_df.groupby('Year').sum()[['Gold',"Silver",'Bronze']].sort_values('Year',ascending=True).reset_index()
    else:        
        x= temp_df.groupby('region').sum()[['Gold',"Silver",'Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total']=x['Gold']+x['Bronze']+x['Silver']
    x[['Gold',"Silver",'Bronze','total']] = x[['Gold',"Silver",'Bronze','total']].astype(int)
    
    return x


def get_country_year(df):
    year = sorted(df['Year'].unique().tolist())
    year.insert(0,'Overall')
    country = np.unique(df['region'].dropna().values)
    country = sorted(country)
    country.insert(0,'Overall')
    return year,country
    
def data_over_time (df,column,name):

    data_over_time_df = df.drop_duplicates(['Year',column])['Year'].value_counts().reset_index()

    data_over_time_df.rename(columns={'Year':'year','count':name},inplace=True)
    return data_over_time_df

def most_successful(df,sport):
    temp_df =df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x =temp_df.groupby('Name').sum()[['Gold','Silver','Bronze']]
    x['total']=x['Gold']+x['Bronze']+x['Silver']
    x =x.sort_values(['total','Gold','Silver','Bronze'],ascending=False)
    return x.reset_index().head(15)

def year_wise_medal_tally(df,country):
    temp_df =df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Medal','Event',])
    temp_df = temp_df[temp_df['region']==country]
    temp_df =temp_df.groupby('Year').sum().reset_index()
    return temp_df

def country_event_heatmap(df,country):
    temp_df =df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Medal','Event',])
    temp_df = temp_df[temp_df['region']==country]
    temp_df =temp_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return temp_df

def most_successful_countrywise(df,Country):
    temp_df =df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == Country]
    temp_df =temp_df['Name'].value_counts().reset_index().head(15).merge(df,on='Name',how='left')[['Name','Sport','count']].drop_duplicates('Name')
    temp_df.rename(columns={'count':'Medal'},inplace=True)
    return temp_df


def create_v_height(df,sport):

    temp_df =df.drop_duplicates(['Name','region'])
    temp_df['Medal'].fillna('No Medal',inplace=True)
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    return temp_df
    
def men_vs_women(df):
    temp_df =df.drop_duplicates(['Name','region'])
    men = temp_df[temp_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women = temp_df[temp_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final =women.merge(men,on='Year',how='right')
    final.fillna(0,inplace=True)
    final.rename(columns={'Name_x':'Female','Name_y':'Male'},inplace=True)
    return final