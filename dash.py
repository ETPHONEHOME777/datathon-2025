import streamlit as st
import pandas as pd


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Parse InvoiceDate
    df['InvoiceDate'] = pd.to_datetime(
        df['InvoiceDate'],
        format='%m/%d/%y %H:%M',
        errors='coerce'
    )
    return df


def timeFilterHelper(df, year, month, date_col='InvoiceDate'):
    mask = (
        (df[date_col].dt.year == year) &
        (df[date_col].dt.month == month)
    )
    return df.loc[mask]

# Functions

def get_product_high_seller(df):
    sales = df[df['Quantity'] > 0]
    summary = (
        sales
        .groupby('Description')['Quantity']
        .sum()
        .sort_values(ascending=False)
    )
    return summary


def get_product_low_seller(df):
    sales = df[df['Quantity'] > 0]
    summary = (
        sales
        .groupby('Description')['Quantity']
        .sum()
        .sort_values(ascending=True)
    )
    return summary


def get_most_revenue(df):
    sales = df[df['Quantity'] > 0].copy()
    sales['Revenue'] = sales['Quantity'] * sales['UnitPrice']
    summary = (
        sales
        .groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=False)
    )
    return summary


def get_least_revenue(df):
    sales = df[df['Quantity'] > 0].copy()
    sales['Revenue'] = sales['Quantity'] * sales['UnitPrice']
    summary = (
        sales
        .groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=True)
    )
    return summary


def get_top_customers(df):
    sales = df[df['Quantity'] > 0]
    summary = (
        sales
        .groupby('CustomerID')['Quantity']
        .sum()
        .sort_values(ascending=False)
    )
    return summary

# Dashboard with Streamlit
def main():
    st.title("Monthly Sales Dashboard")
    st.sidebar.header("Filter Settings (Dec 2010 through Dec 2011)")
    
    year = st.sidebar.number_input("Year", min_value=2010, max_value=2025, value=2011, step=1)
    month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=11, step=1)
    top_n = st.sidebar.slider("Number of items to display", 1, 100, 10)

    df = load_data("data/Mode_Craft_Ecommerce_Data - Online_Retail.csv")
    df_month = timeFilterHelper(df, year, month)
    df_cull = df_month.dropna(subset=['InvoiceDate', 'CustomerID'])
    df_cull2 = df_cull[(df_cull['Quantity'] > 0) & (df_cull['UnitPrice'] > 0)]
    
    st.subheader(f"Data for {month}/{year}")
    st.write(f"Total transactions: {len(df_cull2)}")
    
    st.markdown("---")
    st.subheader(f"Top {top_n} Products by Units Sold")
    st.dataframe(get_product_high_seller(df_cull2).head(top_n))
    
    st.subheader(f"Bottom {top_n} Products by Units Sold")
    st.dataframe(get_product_low_seller(df_cull2).head(top_n))
    
    st.subheader(f"Top {top_n} Products by Revenue")
    st.dataframe(get_most_revenue(df_cull2).head(top_n))
    
    st.subheader(f"Bottom {top_n} Products by Revenue")
    st.dataframe(get_least_revenue(df_cull2).head(top_n))
    
    st.subheader(f"Top {top_n} Customers by Units Purchased")
    st.dataframe(get_top_customers(df_cull2).head(top_n))

if __name__ == "__main__":
    main()