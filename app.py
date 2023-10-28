import plotly.express as px
import streamlit as st
import pandas as pd
import preprocesser,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import numpy as np
# from * import preprocesser
st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio(
    'Select An Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete Wise Analysis')
)
df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')
df = preprocesser.preprocess(df,df_region)

if user_menu=='Medal Tally':
    st.sidebar.title('Medal Tally')
    year,country = helper.get_country_year(df)
    selectec_year =st.sidebar.selectbox('Select Year',year)
    selected_country =st.sidebar.selectbox('Select Country',country)
    medal_tally = helper.fetch_medal_tally(df,selectec_year,selected_country)
    if selectec_year=='Overall' and selected_country =='Overall':
        st.title('Overall Tally')
    if selectec_year!='Overall' and selected_country =='Overall':
        st.title(f'Overall Tally In Year {selectec_year}')
    if selectec_year=='Overall' and selected_country !='Overall':
        st.title(f'Overall Tally Of Country {selected_country}')
    if selectec_year !='Overall' and selected_country !='Overall':
        st.title(f'Overall Tally Of {selected_country} In Year {selectec_year}')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title('Top Statistics')
    athletes=df.Name.unique().shape[0]
    country=df.region.unique().shape[0]
    events=df.Event.unique().shape[0]
    sports=df.Sport.unique().shape[0]
    cities=df.City.unique().shape[0]
    editions=df.Year.unique().shape[0]-1
    
    col1,col2,col3,=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3,=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(country)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    
    st.title('Participating Nations Over The Year')
    nations_over_time_df = helper.data_over_time(df,'region','countries')
    fig = px.line(nations_over_time_df,x='year',y='countries')
    st.plotly_chart(fig)
    st.title('Events Over The Year')
    nations_over_time_df = helper.data_over_time(df,'Event','events')
    fig = px.line(nations_over_time_df,x='year',y='events')
    st.plotly_chart(fig)
    st.title('Athlet Over The Year')
    nations_over_time_df = helper.data_over_time(df,'Name','athletes')
    fig = px.line(nations_over_time_df,x='year',y='athletes')
    st.plotly_chart(fig)
    st.title('No Of Events Overtime Of Sports')
    fig,ax = plt.subplots(figsize=(25,20))
    x =df.drop_duplicates(['Year','Sport','Event'])
    ax =sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)
    st.title('Most Successful Players')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport =  st.selectbox('Select A Sport',sport_list)
    st.table(helper.most_successful(df,selected_sport))
    
if user_menu == 'Country-Wise Analysis':
    year,country = helper.get_country_year(df)
    country = country[1:]
    selected_country = st.sidebar.selectbox('Select Country',country)
    st.title('Medal Analysis Of {}'.format(selected_country))
    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y=['Gold','Silver','Bronze'],color_discrete_sequence=['Gold', 'Silver','#cd7f32'])
    st.plotly_chart(fig)
    try :
        st.title('{} Sport Heatmap'.format(selected_country))
        sport_country_df = helper.country_event_heatmap(df,selected_country)
        fig,ax = plt.subplots(figsize=(25,20))
        sns.heatmap(sport_country_df,annot=True)
        st.pyplot(fig)
    except:
        st.text("{} Not Win Any Game So Heatmap Can't Be Show".format(selected_country))
    st.title('Most Successful Player In {}'.format(selected_country))
    top_temp_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top_temp_df)
if user_menu == 'Athlete Wise Analysis':
    
    st.title('Distrubution Of Age')
    player_df =df.drop_duplicates(['Name','region'])
    x1 =player_df['Age'].dropna()
    x2= player_df[player_df['Medal']=='Gold']['Age'].dropna()
    x3= player_df[player_df['Medal']=='Silver']['Age'].dropna()
    x4= player_df[player_df['Medal']=='Bronze']['Age'].dropna()
    fig =ff.create_distplot([x1,x2,x3,x4],['Age Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.plotly_chart(fig)
    
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                    'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                    'Tennis', 'Golf', 'Softball', 'Archery',
                    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                    'Rhythmic Gymnastics', 'Rugby Sevens',
                    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    x = []
    name = []
    for sport in famous_sports:
        temp_df = player_df[player_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig =ff.create_distplot(x,name,show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.header('Distribution Of Age With Respect To Sport Who Won Gold Medal')
    st.plotly_chart(fig)
    
    x = []
    name = []
    for sport in famous_sports:
        temp_df = player_df[player_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig =ff.create_distplot(x,name,show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.header('Distribution Of Age With Respect To Sport Who Won Silver Medal')
    st.plotly_chart(fig)
    
    x = []
    name = []
    for sport in famous_sports:
        temp_df = player_df[player_df['Sport'] == sport]
        temp_df=temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna()
        if temp_df.shape[0] != 0:
            x.append(temp_df)
            name.append(sport)

    fig =ff.create_distplot(x,name,show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.header('Distribution Of Age With Respect To Sport Who Bronze Medal')
    st.plotly_chart(fig)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport =  st.selectbox('Select A Sport',sport_list)
    temp_df = helper.create_v_height(df,selected_sport)
    fig,ax = plt.subplots(figsize=(20,20))
    ax =sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=350)
    st.pyplot(fig)

    st.title('Men Vs Women Participation')
    final =helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Female','Male'])
    fig.update_layout(autosize=False,width=880,height=600)
    st.plotly_chart(fig)
    
    