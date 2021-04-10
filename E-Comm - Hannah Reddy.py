mport numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import data as sales using pd.read_csv
sales = pd.read_csv(r"C:\Users\hreddy\Documents\E_Comm_Sales.csv")

separator = '\n*******************************\n'

print("a")

# print top 5 rows
print(sales.head(5))

print(separator)

# print shape of dataset
print(sales.shape)

print(separator)

# understand data types by using info function
print(sales.info())

print(separator)

# obtain data description
sales.describe()

print(separator)

# Date is an object - change to date time format using pandas
sales['InvoiceDate'] = pd.to_datetime(sales['InvoiceDate'])

print(separator)

# check updated information
print(sales.info())

print(separator)

# count the number of missing values in each column
missing_rows = sales.isnull().sum().sort_values(ascending=False)
print(missing_rows)

print(separator)

# Replace missing values with a default value
sales.Description.fillna('No description', inplace=True)

print(separator)

# Drop duplicates
sales.drop_duplicates(inplace=True)

# create new columns - total sales, year, month

sales['Month'] = sales['InvoiceDate'].apply(lambda x: x.month)

sales['Year'] = sales['InvoiceDate'].apply(lambda x: x.year)

sales['Day']=sales['InvoiceDate'].apply(lambda x: x.day)

sales['TotalPrice'] = sales['Quantity'] * sales['UnitPrice']

print(sales.head())

# Sort Values by year and month
sales = sales.sort_values(by=['Year', 'Month'])

# Find out highest and lowest unit price
print(sales['UnitPrice'].max())
print(sales['UnitPrice'].min())
print(sales['UnitPrice'].mean())
print(sales['TotalPrice'].sum())

# demonstrate knowledge of loop function to list column names
for col in sales.columns:
    print(col)

print(separator)

#demonstrate knowledge of lists using list function to list column names

countries_list = list(sales.Country.unique())
print(countries_list)

print(separator)

#find list of countries having more than 1000 entries
for key, value in dict(sales.Country.value_counts()[:6]).items():

    if value > 10000:
        print("More than 10k")
    elif value <= 10000 and value >= 2000:
        print("Between 10k and 2k ")
    else:
        print("Less than 2k")

# Discovering what are the most and least popular products based on the quantity
qty = sales.pivot_table(index=['StockCode', 'Description'], values='Quantity', aggfunc='sum').sort_values(
    by='Quantity', ascending=False)

print(qty.head(10))

print(separator)

# Find top 10 countries in terms of number of transactions using a dictionary

country_dict = dict(sales.Country.value_counts()[:10])
print(country_dict)
print("Key: ", country_dict.keys())
print("Values: ", country_dict.values())

# Enumerating a dictionary
for key, value in country_dict.items():
    print(key, "=", value)

print(separator)

# Find out the 'CustomerID' that placed the most orders

print('The TOP 10 customers with most number of orders')
customer_best = sales.groupby(by=['CustomerID', 'Country'], as_index=False)['InvoiceNo'].count()
print(customer_best.sort_values(by='InvoiceNo', ascending=False).head(10))

print(separator)

# Visualation 1: Top 10 countries by number of sales

sales.Country.value_counts().head().plot(kind='bar')

# Visualation 2: Top 10 countries by amount of sales

gross_sales = sales.groupby(['Country'])['TotalPrice'].agg('sum').reset_index().sort_values(by=['TotalPrice'],ascending=False).head()
print(gross_sales)
print(gross_sales.plot(x='Country', y='TotalPrice',kind='bar',))

# Visualation 3: Orders by month

sales['Month_str'] = sales.InvoiceDate.dt.to_period('M').astype(str)
order_per_month = sales.groupby(by='Month_str', as_index=False).TotalPrice.sum()
plt.figure(figsize = (12,5))
ax = sns.lineplot(x="Month_str", y = "TotalPrice", data=order_per_month)
ax.set_title('Orders per month');

# Visualisation 4. Find out the most common stockcodes and descriptions using seaborn

stockcode_frequency = sales.StockCode.value_counts().sort_values(ascending=False)
description_frequency = sales.Description.value_counts().sort_values(ascending=False)

fig, ax = plt.subplots(2,1,figsize=(20,15))

# 1st subplot - most common stockcodes
sns.barplot(stockcode_frequency.iloc[0:19].index,
            stockcode_frequency.iloc[0:19].values,
            ax = ax[0], palette="Blues_r")
ax[0].set_ylabel("Frequency")
ax[0].set_xlabel("Stockcode")
ax[0].set_title("20 most common stockcodes");

# 2nd subplot - most common descriptions
sns.barplot(description_frequency.iloc[0:19].index,
            description_frequency.iloc[0:19].values,
            ax = ax[1], palette="Purples_r")
ax[1].set_ylabel("Frequency")
ax[1].set_xlabel("Description")
ax[1].tick_params(labelrotation=90)
ax[1].set_title("20 most common descriptions")


# Visualisation 2: Find out the number of orders made by the customers using Matplotlib

orders = sales.groupby(by=['CustomerID','Country'], as_index=False)['InvoiceNo'].count()

plt.subplots(figsize=(10,6))
plt.plot(orders.CustomerID, orders.InvoiceNo)
plt.xlabel('Customers ID')
plt.ylabel('Number of Orders')
plt.title('Number of Orders for different Customers')

#most popular stock code

fig, ax = plt.subplots(figsize=(15,4))
grouped = sales.groupby("StockCode")['Description'].unique()
grouped_counts = grouped.apply(lambda x: len(x)).sort_values(ascending=False)
grouped_counts.head(50).plot.bar(ax=ax)

#Regionwise analysis

reg = sales[sales['TotalPrice']>=0].groupby('Country').agg({'TotalPrice':'sum',
                                                  'Quantity': 'sum',
                                                  'CustomerID': 'count'})

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10,30))
g1 = sns.barplot(x=reg['TotalPrice'], y=reg.index, alpha=1, ax=ax[0],palette='Reds', orient='h')
g2 = sns.barplot(x=reg['Quantity'], y=reg.index, alpha=1, ax=ax[1], palette='Blues',orient='h')
g3 = sns.barplot(x=reg['CustomerID'], y=reg.index, alpha=1, ax=ax[2], palette='Greens', orient='h')
ax[2].title.set_text('Customers Count by Country')
ax[2].set_xlabel("Customers")
ax[1].title.set_text('Quantity Sold by Country')
ax[1].set_xlabel("Quantity")
ax[0].title.set_text('Revenue by Country')
ax[0].set_xlabel("Revenue")

plt.show()

#product with most cancellations
fig, ax = plt.subplots(figsize=(7,10))
neg_qty = sales[sales["Quantity"]<0]
neg_qty["TotalPrice"] = abs(neg_qty["TotalPrice"])
x = neg_qty[["ProductName","TotalPrice"]]
x.groupby("ProductName")["TotalPrice"].sum().sort_values(ascending=True).tail(30).plot.barh(ax=ax)

#who is most likely to return goods
Item_retured = df[df['Quantity'] < 0].groupby('CustomerID')[['Revenue',
                                              'Quantity']].agg(['sum']).sort_values(by=[('Quantity', 'sum')], ascending=True).head(10)

sns.barplot(x=Item_retured.index, y=abs(Item_retured[('Quantity','sum')]))
plt.ylabel('A number of Quantity returned')
plt.xticks(rotation=90)
plt.show()

Print("a")




