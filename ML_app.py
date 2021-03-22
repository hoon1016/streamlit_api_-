import streamlit as st 
import yfinance as yf 
import matplotlib.pyplot as plt 
from datetime import datetime
import pandas as pd
import numpy as np 
import requests
from fbprophet import Prophet

def run_ML_app():
    st.header('Online Stock Price Ticker')

    #yfinace 실행
    
    symbol = st.text_input('주식이름 검색 : ')

    # symbol = 'AAPL'
    data = yf.Ticker(symbol)

    today = datetime.now().date().isoformat()
    print(today)

    df = data.history(start='2010-06-01',end=today)

    res = requests.get('https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(symbol))

    res_data = res.json()

    p_df = df.reset_index()
    p_df.rename(columns = {'Date':'ds','Close':'y'},inplace =True)

    m = Prophet()
    m.fit(p_df)

    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    fig1 = m.plot(forecast)
    st.pyplot(fig1)
    

    fig2 = m.plot_components(forecast)
    st.pyplot(fig2)
