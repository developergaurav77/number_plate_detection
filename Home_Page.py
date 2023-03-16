# from sqlalchemy.engine import create_engine,URL
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.graph_objects as go


def connection():
    password = "****"
    engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/anpr')
    return engine

engine = connection()

def plot(x,y):
    fig = go.Figure()
    fig.add_trace(go.Line(x=x, y=y,line=dict(color='firebrick', width=1)))
    return fig

st.markdown("# Dashboard")
st.sidebar.markdown("# Dashboard")


query = 'SELECT * from anpr.car_check_in order by id desc;'
with engine.begin() as conn:
    df = pd.read_sql_query(sql=text(query), con=conn)  
df['id'] = df['id'].astype(int) 
df = df.reset_index(drop=True)

daily_agg_df = df.groupby([pd.Grouper(key='check_in',freq="1D")]).agg(count=("id","count"),amount=("amount","sum")).reset_index()
daily_agg_df.sort_values("check_in",inplace=True,ascending=False)
daily_agg_df.reset_index(drop=True,inplace=True)

col1, col2 = st.columns( [0.5, 0.5])
with col1:
    total_count = df['id'].count()
    st.subheader("Total Vehicle Entry")
    st.write(total_count)


with col2:
    total_amount = df['amount'].sum()    
    st.subheader("Total Amount Earned")
    st.write(total_amount)

df_home = df.head(20)
print(df_home)
st.write("Latest Vehicle Entry:")
st.dataframe(df_home)

st.subheader("Vechile Entry Distribution")
count_plot = plot(daily_agg_df['check_in'],daily_agg_df['count'])
st.plotly_chart(count_plot, theme=None, use_container_width=True)

st.subheader("Amount Distibution")
amt_plot = plot(daily_agg_df['check_in'],daily_agg_df['amount'])
st.plotly_chart(amt_plot, theme=None, use_container_width=True)
