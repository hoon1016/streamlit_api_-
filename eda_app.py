import streamlit as st 
import yfinance as yf 
import matplotlib.pyplot as plt 
from datetime import datetime
import pandas as pd
import numpy as np 
import requests
from fbprophet import Prophet
from sklearn.preprocessing import MinMaxScaler

def run_eda_app():
    
    

    symbol = st.text_input('보고싶은 주식 입력 : ')
    data = yf.Ticker(symbol)

    today = datetime.now().date().isoformat()
    print(today)

    df = data.history(start='2010-06-01',end=today)

    st.dataframe(df)

    st.subheader('종가')
    if st.button('종가 보기'):
        st.line_chart(df['Close'])
        
    st.subheader('거래량')
    if st.button('거래량 보기'):
        st.line_chart(df['Volume'])

    div_df=data.dividends
    
    st.dataframe(div_df.resample('Y').sum())

    new_df = div_df.reset_index()
    new_df['Year'] = new_df['Date'].dt.year

    st.dataframe(new_df)
    
    if st.button('차트보기'):
    
        fig = plt.figure()
        plt.bar(new_df['Year'],new_df['Dividends'])
        st.pyplot(fig)
    # 여러 주식 데이터를 한번에 보여주기.
    
    favorites = ['msft','INTC','nvda','aapl','amzn']

    f_df = pd.DataFrame()
    
    for stock in favorites :
        f_df[stock] = yf.Ticker(stock).history(start='2010-01-01',end=today)['Close']

    st.dataframe(f_df)
    
    corr_columns = f_df.columns[f_df.dtypes != object]
    corr_list = st.multiselect('차트를 볼 컬럼을 선택하세요',corr_columns)
    
    if len(corr_list) != 0 :
        st.dataframe(f_df[corr_list].corr())
        st.line_chart(f_df[corr_list])
    
    #스탁트윗의 API를 호출!!
    res = requests.get('https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(symbol))

    #JSON 형식이므로, .json()이용.
    res_data = res.json()

    #파이썬의 딕셔너리와 리스트의 조합으로 사용가능
    # st.write(res_data)

    for message in res_data['messages']:
        
        col1,col2 = st.beta_columns([1,4])

        with col1 : 
            st.image(message['user']['avatar_url'])
        with col2 :
            st.write('유저 이름 : ' +message ['user']['username'])
            st.write('트윗 내용 : ' +message ['body'])
            st.write('올린 시간 : ' +message ['created_at'])

