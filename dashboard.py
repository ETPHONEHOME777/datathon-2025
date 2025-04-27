import streamlit as st
import pandas as pd
from Analysis_Methods import monthly_report
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import calendar


df = pd.read_csv('/Users/rj/Documents/Datathon 2025/Mode_Craft_Ecommerce_Data - Online_Retail.csv')

#Sidebar filters
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%y %H:%M')

df['month'] = df['InvoiceDate'].dt.month
df['year'] = df['InvoiceDate'].dt.year

month_options = [f"{i} - {calendar.month_name[i]}" for i in sorted(df['month'].unique())]

year = st.sidebar.selectbox('Select Year', sorted(df['year'].unique()))
selectedMonth = st.sidebar.selectbox('Select Month', month_options)
month = int(selectedMonth.split('-')[0])

if not((df['year'] == year) & (df['month'] == month)).any():
    st.error(f'No data available for {month}/{year}. Please select a different month or year.')
    st.stop()

analysisType = st.sidebar.selectbox('Select Analysis Type',
                                        ("Top Products Sold by Quantity",
                                        "Top Revenue Products",
                                        "Bottom Revenue Products",
                                        "Customer Who Bought The Most by Pound Value",
                                        "Customer Who Bought The Least by Pound Value",
                                        "Customer Who Bought The Most by Quantity",
                                        "Customer Who Bought The Least by Quantity",
                                        "Most Popular Days",
                                        "Most Popular Times of The Day by Money Spent",
                                        "Most Popular Times of The Day by Invoices",
                                        "Top Earning Regions",
                                        "Most Returned Items by Quantity")
                                     )

report = monthly_report(df, year, month)

#display
st.title(f"Monthly Analysis: {month}/{year} - {analysisType}")

if(analysisType == "Top Products Sold by Quantity"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Top Products Sold by Quantity"])
    with col2:
        fig, ax = plt.subplots()
        report["Top Products Sold by Quantity"].plot(kind='barh', ax=ax)
        ax.invert_yaxis()
        ax.set_xlabel('Quantity Sold')
        ax.set_title('Top 10 Products Sold by Quantity')
        st.pyplot(fig)

elif(analysisType == "Top Revenue Products"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Top Revenue Products"])
    with col2:
        fig, ax = plt.subplots()
        report["Top Revenue Products"].plot(kind='barh', ax=ax)
        ax.invert_yaxis()
        ax.set_xlabel('Total Revenue')
        ax.set_title('Top 10 Products by Revenue')
        st.pyplot(fig)

elif(analysisType == "Bottom Revenue Products"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Bottom Revenue Products"])
    with col2:
        fig, ax = plt.subplots()
        report["Bottom Revenue Products"].plot(kind='barh', ax=ax)
        ax.set_xlabel('Total Revenue')
        ax.set_title('Bottom 10 Products by Revenue')
        st.pyplot(fig)

elif(analysisType == "Customer Who Bought The Most by Pound Value"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Customer Who Bought The Most by Dollar Value"])
    with col2:
        fig, ax = plt.subplots()
        report["Customer Who Bought The Most by Dollar Value"].plot(kind='bar', ax=ax)
        ax.set_ylabel('Total Amount Bought ($)')
        ax.set_title('Top 10 Customers by Pound Value')
        plt.xticks(rotation=45)
        st.pyplot(fig)

elif(analysisType == "Customer Who Bought The Least by Pound Value"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Customer Who Bought The Least by Dollar Value"])
    with col2:
        fig, ax = plt.subplots()
        report["Customer Who Bought The Least by Dollar Value"].plot(kind='bar', ax=ax)
        ax.set_ylabel('Total Amount Bought ($)')
        ax.set_title('Bottom 10 Customers by Pound Value')
        plt.xticks(rotation=45)
        st.pyplot(fig)

elif(analysisType == "Customer Who Bought The Most by Quantity"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Customer Who Bought The Most by Quantity"])
    with col2:
        fig, ax = plt.subplots()
        report["Customer Who Bought The Most by Quantity"].plot(kind='bar', ax=ax)
        ax.set_ylabel('Total Amount by Quantity')
        ax.set_title('Top 10 Customers by Quantity')
        plt.xticks(rotation=45)
        st.pyplot(fig)

elif(analysisType == "Customer Who Bought The Least by Quantity"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Customer Who Bought The Least by Quantity"])
    with col2:
        fig, ax = plt.subplots()
        report["Customer Who Bought The Least by Quantity"].plot(kind='bar', ax=ax)
        ax.set_ylabel('Total Amount by Quantity')
        ax.set_title('Bottom 10 Customers by Quantity')
        plt.xticks(rotation=45)
        st.pyplot(fig)

elif(analysisType == "Most Popular Days"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Most Popular Days"])
    with col2:
        popDays = report["Most Popular Days"]
        order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        popDays = popDays.reindex(order)
        fig, ax = plt.subplots()
        popDays.plot(kind='bar', ax=ax)
        ax.set_ylabel('Total Quantity Sold')
        ax.set_title('Most Popular Days by Quantity Sold')
        st.pyplot(fig)

elif(analysisType == "Most Popular Times of The Day by Money Spent"):
    pivot = report["Most Popular Times of The Day by Money Spent"].pivot_table(index='DayOfWeek', columns='Hour',values='Revenue')
    order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    pivot = pivot.reindex(order)
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot, cmap="YlGnBu", ax=ax)
    plt.title('Purchase Frequency by Day and Hour by Pound Value')
    plt.xlabel('Hour of The Day')
    plt.ylabel('Day of The Week')
    st.pyplot(fig)

elif(analysisType == "Most Popular Times of The Day by Invoices"):
    pivot = report["Most Popular Times of The Day by Invoices"].pivot_table(index='DayOfWeek', columns='Hour', values='InvoiceNo')
    order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    pivot = pivot.reindex(order)
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot, cmap="YlGnBu", ax=ax)
    plt.title('Purchase Frequency by Day and Hour by Invoices')
    plt.xlabel('Hour of The Day')
    plt.ylabel('Day of The Week')
    st.pyplot(fig)

elif(analysisType == "Top Earning Regions"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Top Earning Regions"])
    with col2:
        fig = px.choropleth(
            report["Top Earning Regions"],
            locations='Country',
            locationmode='country names',
            color='Revenue',
            color_continuous_scale='Blues',
            #range_color=[report["Top Earning Regions"]['Revenue'].min(), report["Top Earning Regions"]['Revenue'].max()/2],
            color_continuous_midpoint=report["Top Earning Regions"]['Revenue'].median(),
            title='Revenue by Country'
        )
        st.plotly_chart(fig)

elif(analysisType == "Most Returned Items by Quantity"):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(report["Most Returned Items by Quantity"])
    with col2:
        fig, ax = plt.subplots()
        report["Most Returned Items by Quantity"].plot(kind='barh', ax=ax)
        ax.invert_yaxis()
        ax.set_xlabel('Quantity Returned')
        ax.set_title('Top 10 Products Returned')
        st.pyplot(fig)