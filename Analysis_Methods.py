import pandas as pd
import matplotlib.pyplot as plt

def monthly_report(df, year, month):
    df = df.copy()
    #Put into correct date/time format
    #df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%y %H:%M')

    #Select according to date and year
    if not pd.api.types.is_datetime64_any_dtype(df['InvoiceDate']):
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%y %H:%M')

    monthlyData = df[(df['InvoiceDate'].dt.month == month) & (df['InvoiceDate'].dt.year == year)]
    non_product = ['DOT', 'BANK CHARGES', 'D', 'AMAZONFEE', 'M', 'S', 'POST', 'm', 'S', 'CRUK', 'PADS', 'C2']
    monthlyData = monthlyData[~monthlyData.StockCode.isin(non_product)]
    monthlyData['CustomerID'] = monthlyData['CustomerID'].apply(lambda x: int(x) if pd.notnull(x) else x)
    monthlyData['CustomerID'] = monthlyData['CustomerID'].astype(str)

    #Add new cols
    #Revenue column
    monthlyData['Revenue'] = monthlyData.Quantity * monthlyData.UnitPrice
    #Day of week column
    monthlyData['DayOfWeek'] = monthlyData['InvoiceDate'].dt.day_name()
    #Week period column
    monthlyData['Week'] = monthlyData['InvoiceDate'].dt.to_period('W')
    #Hour of day column
    monthlyData['Hour'] = monthlyData['InvoiceDate'].dt.hour
    #Time of day column
    monthlyData['TimeOfDay'] = monthlyData['Hour'].apply(timeOfDay)

    report = {}

    #Top and bottom 10 sold products
    noReturns = monthlyData[monthlyData['Quantity'] >= 0]
    top10Sold = noReturns.groupby('StockCode')['Quantity'].sum().sort_values(ascending=False).head(10)

    #Highest and lowest 10 revenue products
    productRevenue = monthlyData.groupby('StockCode')['Revenue'].sum().sort_values(ascending=False).reset_index()
    highRevenue = productRevenue.head(10).reset_index(drop=True)
    lowRevenue = productRevenue.tail(10).reset_index(drop=True)

   # Top and bottom 10 customers by dollar
    customerDollar = monthlyData.groupby('CustomerID', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=False)
    customerDollar['CustomerID'] = customerDollar['CustomerID'].apply(lambda x: int(float(x)) if pd.notnull(x) and str(x).lower() != 'nan' else x)
    customerDollar['CustomerID'] = customerDollar['CustomerID'].astype(str)
    customerHighDollar = customerDollar.head(10)
    customerLowDollar = customerDollar.tail(10)

    # Top and bottom 10 customers by quantity bought
    customerQuantity = monthlyData.groupby('CustomerID', as_index=False)['Quantity'].sum().sort_values('Quantity', ascending=False)
    customerQuantity['CustomerID'] = customerQuantity['CustomerID'].apply(lambda x: int(float(x)) if pd.notnull(x) and str(x).lower() != 'nan' else x)
    customerQuantity['CustomerID'] = customerQuantity['CustomerID'].astype(str)
    customerHighQuantity = customerQuantity.head(10)
    customerLowQuantity = customerQuantity.tail(10)


    #Most popular day of the week
    popularDay = monthlyData.groupby('DayOfWeek')['Quantity'].sum()

    #Most popular times for purchase by dollar (heat map)
    popularTimeDollar = monthlyData.groupby(['Hour', 'DayOfWeek'])['Revenue'].sum().reset_index()

    #Most popular times for purchase by invoices (heat map)
    popularTimeInvoice = monthlyData.groupby(['Hour', 'DayOfWeek'])['InvoiceNo'].nunique().reset_index()
    
    #Regions that made the most
    regionRevenue = monthlyData.groupby('Country')['Revenue'].sum().sort_values(ascending=False).reset_index()

    #Most returned items
    returned = monthlyData[monthlyData['Quantity'] < 0]
    returned = returned.groupby('StockCode')['Quantity'].sum().sort_values(ascending=False)
    highReturned = returned.tail(10)


    report['Top Products Sold by Quantity'] = top10Sold
    report['Top Revenue Products'] = highRevenue
    report['Bottom Revenue Products'] = lowRevenue
    report['Customer Who Bought The Most by Dollar Value'] = customerHighDollar
    report['Customer Who Bought The Least by Dollar Value'] = customerLowDollar
    report['Customer Who Bought The Most by Quantity'] = customerHighQuantity
    report['Customer Who Bought The Least by Quantity'] = customerLowQuantity
    report['Most Popular Days'] = popularDay
    report['Most Popular Times of The Day by Money Spent'] = popularTimeDollar
    report['Most Popular Times of The Day by Invoices'] = popularTimeInvoice
    report['Top Earning Regions'] = regionRevenue
    report['Most Returned Items by Quantity'] = highReturned

    return report



def timeOfDay(hour):
    if(6 <= hour < 12):
        return 'Morning'
    elif(12 <= hour < 17):
        return 'Afternoon'
    else:
        return 'Evening'