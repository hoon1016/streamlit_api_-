import streamlit as st 
import yfinance as yf 
import matplotlib.pyplot as plt 
from datetime import datetime
import pandas as pd
import numpy as np 
import requests
from fbprophet import Prophet
from eda_app import run_eda_app
from ML_app import run_ML_app
def main():
    st.title('주식 차트 보기')
    #사이드바 메뉴
    menu = ['Home','EDA','ML']
    choice = st.sidebar.selectbox('MENU',menu)

    if choice == 'Home':
        st.write('보고싶은 주식차트 보기.')
        st.write('보고싶은 주식차트 예측하기')
        st.write('왼쪽의 사이드바에서 선택하세요.')

    elif choice =='EDA':
        run_eda_app()

    elif choice =='ML':
        run_ML_app()
    




if __name__=='__main__':
    main()