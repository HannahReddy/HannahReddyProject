import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Import data as sales using pd.read_csv
sales = pd.read_csv(r"C:\Users\hreddy\Documents\E_Comm_Sales.csv")

separator = '\n*******************************\n'

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
quantity = sales.pivot_table(index=['StockCode', 'Description'], values='Quantity', aggfunc='sum').sort_values(
    by='Quantity', ascending=False)

print(quantity.head(10))

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

print('The top 10 customers with most number of orders')
customer_best = sales.groupby(by=['CustomerID', 'Country'], as_index=False)['InvoiceNo'].count()
print(customer_best.sort_values(by='InvoiceNo', ascending=False).head(10))

print(separator)


# Visualation 1: Sales by Country - log scale

TotalPriceGrouped = sales.groupby(by=['CustomerID','Country'], as_index=False)['TotalPrice'].sum()

total_price_country = TotalPriceGrouped.groupby(by=['Country'], as_index=False)['TotalPrice'].sum().sort_values(by='TotalPrice', ascending=False)
plt.subplots(figsize=(20,6))
sns.barplot(total_price_country.Country, total_price_country.TotalPrice,palette="Blues_r")
plt.xlabel('Country', fontsize=15)
plt.ylabel('Total Sales',fontsize=15)
plt.title('Total Sales from each country', fontsize=15)
plt.xticks(rotation=60)
plt.yscale("log")

# Visualisation 2: Orders by month

sales['Month'] = sales.InvoiceDate.dt.to_period('M').astype(str)
order_per_month = sales.groupby(by='Month', as_index=False).TotalPrice.sum()
plt.figure(figsize = (12,5))
ax = sns.lineplot(x="Month", y = "TotalPrice", data=order_per_month)
ax.set_title('Orders per month');

# Visualisation 3. Find out the most common stockcodes and descriptions using seaborn

stockcode_frequency = sales.StockCode.value_counts().sort_values(ascending=False)
description_frequency = sales.Description.value_counts().sort_values(ascending=False)

fig, ax = plt.subplots(2,1,figsize=(15,8))

# 1st subplot - most common stockcodes
sns.barplot(stockcode_frequency.iloc[0:10].index,
            stockcode_frequency.iloc[0:10].values,
            ax = ax[0], palette="Blues_r")
ax[0].set_ylabel("Frequency")
ax[0].set_xlabel("Stockcode")
ax[0].set_title("Most Common Stockcodes");

# 2nd subplot - most common descriptions
sns.barplot(description_frequency.iloc[0:10].index,
            description_frequency.iloc[0:10].values,
            ax = ax[1], palette="Purples_r")
ax[1].set_ylabel("Frequency")
ax[1].set_xlabel("Description",fontsize=15)
ax[1].tick_params(labelrotation=60)
ax[1].set_title("Most Common Descriptions")

# Visualisation 4. Find out the most common customers using seaborn

customer_frequency = sales.CustomerID.value_counts().sort_values(ascending=False).iloc[0:19]
plt.figure(figsize=(15,10))
customer_frequency.index = customer_frequency.index.astype('Int64')
sns.barplot(customer_frequency.index, customer_frequency.values, order=customer_frequency.index, palette="Blues_r")
plt.ylabel("Frequency")
plt.xlabel("CustomerID")
plt.title("Which customers are most common?");


#Visualisaiton 5: Price analysis

plt.subplots(figsize =(12,6))
sns.boxplot(sales.UnitPrice);

plt.show()


