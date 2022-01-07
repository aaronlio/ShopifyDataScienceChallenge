#<------------------------ SHOPIFY DATA SCIENCE TECHNICAL CHALLENGE ------------------------>
#<------------ Question 1a ------------>
"""Think about what could be going wrong with our calculation. Think about a better way to evaluate this data. """

import pandas as pd
import matplotlib.pyplot as plt

order_amounts = []

df = pd.read_csv('2019 Winter Data Science Intern Challenge Data Set - Sheet1.csv')

# Initial Conditions
print("The number of missing data points", df.isnull().sum()) # Shows the completeness of the dataset
print(f"The initial mean {df['order_amount'].mean()}") # Initial Mean
print(f"The initial median {df['order_amount'].median()}") # Initial Median
print(df['order_amount'].describe(),'\n') # Other metrics

# Visualizing the data
ax1=df.plot.scatter(x = 'total_items', y= 'order_amount')
#plt.show() 

# As you can see, there are a few orders, 63 to be precise, that are over 10,000, this skews the mean of the dataset by a significant amount.
# To correct for this, we can use the outlier formula to eliminate outliers. The formula is:
# Threshold = 1.5 * IQR, where IQR = 75th%ile - 25th%ile
q1 = df['order_amount'].quantile(0.25)
q3 = df['order_amount'].quantile(0.75)
IQR = q3-q1
maxthreshold = df['order_amount'].median() + (1.5*IQR)
minthreshold = df['order_amount'].median() - (1.5*IQR) # Negative value


print(f"Using the full dataset, the current number of orders above $100000 is: {df['order_amount'][df['order_amount'] > 100000 ].count()}")
print(f"\nUsing the full dataset, the current number of orders above $20000 is: {df['order_amount'][df['order_amount'] > 20000 ].count()}")

### These lines of code can be used to observe the spread of the data, but were not used in the final analysis
#df2 = df[(df['order_amount'] <= 100000)]
#print(f"\nAfter removing orders > 100000, the current number of orders above $20000 is: {df2['order_amount'][df2['order_amount'] > 20000 ].count()}")
#print(f"\nThe mean is now {df2['order_amount'].mean()}")

#df3 = df[(df['order_amount'] <= 20000)]
#print(f"\nAfter removing orders > 20000, the current number of orders above $10000 is: {df3['order_amount'][df3['order_amount'] > 10000 ].count()}\n")
#print(f"The mean is now {df3['order_amount'].mean()}")
#print(f"The median is now {df3['order_amount'].median()}")

df2 = df[df['order_amount'] <= maxthreshold]
print(f"\nThe mean is now {df2['order_amount'].mean()}")
print(f"\nThe median is now {df2['order_amount'].median()}")
print(f"\nThe number of orders is now {df2['order_amount'].count()}")

"""Based on the results presented above, there is a clear issue with the initial data analysis. There were a number of values, 262, or about 5% of 
the data, should have been considered as outliers. This isn't necessarily problematic if the intended result was to include bulk orders.
Yet, based on the problem statement, it appears as though the analysis was intended to capture the Average Order Value of
standard consumer orders. Thus, these bulk orders, which were mathematically considered outliers, had to be eliminated to accurately gauge
the AOV. Though, in place of this analysis, a different metric could have simply been used."""

#<------------ Question 1b ------------>
"""Once outliers have been eliminated, the mean is 283.81 and the median is 272. Initially, before outlier removal, the median was 284. This is 
effectively the same as the mean following outlier removal. As is standard with datasets with large standard deviations/variances,
the median can be used to more accurately gauge the AOV of the initial data."""

#<------------ Question 1c ------------>
"""The value of the median before outlier removal is 284, and 272 after removal."""

#<------------ Question 2a ------------>
"""Using the following SQL Code, it was found that Speedy Express shipped 54 orders"""

"""SELECT ShipperName, Count(ShipperName) as NumberOfOrders 
FROM Shippers
INNER JOIN Orders ON Shippers.ShipperID = Orders.ShipperID
WHERE ShipperName is 'Speedy Express'
"""


#<------------ Question 2b ------------>
"""Using the following SQL Code, it was found that Peacock shipped 40 orders"""

"""
SELECT LastName, MAX(OrderCount) as NumberOfOrders from
    (SELECT LastName, Count(LastName) as OrderCount FROM Orders
    INNER JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
    GROUP BY LastName);
    """


#<------------ Question 2c ------------>
"""Using the following SQL Code, it was found that Gorgonzola Telino was the most ordered product in Germany, being ordered 5 times."""
"""
SELECT ProductName as MostPopularProduct, Max(ProductCount) as NumberOfOrders from 	
  (SELECT ProductName, count(ProductName) as ProductCount
  from Orders
  INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID
  INNER JOIN OrderDetails ON Orders.OrderID=OrderDetails.OrderID
  INNER JOIN Products ON OrderDetails.ProductID=Products.ProductID
  WHERE Country = 'Germany'
  GROUP BY ProductName
  """
