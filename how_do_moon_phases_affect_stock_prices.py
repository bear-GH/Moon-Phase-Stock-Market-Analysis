from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import ephem
import sys

# Changing either SPX and VIX
SPX_or_VIX = "VIX"

# Loading a comma-separated values (csv) file into a pandas DataFrame
VIX_df = pd.read_csv(r"C:/Users/raymo/Downloads/" + SPX_or_VIX + ".csv")

# Changing column names
VIX_df.columns = ["Date", "Adjusted Close"]

# Converting 'Date' column data type to datetime data type
VIX_df["Date"] = pd.to_datetime(VIX_df["Date"])

# Sorting DataFrame in ascending order by date
VIX_df = VIX_df.sort_values("Date")
#pd.set_option("display.max_row", None, "display.max_columns", None)

# Creating lists from DataFrame columns
dates = VIX_df["Date"].tolist()
adjusted_closes = VIX_df["Adjusted Close"].tolist()

# Finding the earliest and latest dates
earliest_date = min(VIX_df["Date"])
latest_date = max(VIX_df["Date"])

# Finding the first full moon
first_full_moon = ephem.next_full_moon(earliest_date)

# Converting from ephem date data type to datetime data type
first_full_moon = first_full_moon.datetime()

# Finding all full moon dates within the earliest date and lastest date
full_moons = [first_full_moon]
while True:
    full_moon = ephem.next_full_moon(full_moons[-1]).datetime()
    if full_moon > latest_date:
        break
    full_moons.append(full_moon)

# Converting from datetime data type to date data type
full_moons = [date.date() for date in full_moons]
dates = [date.date() for date in dates]

# Removing all full moon dates which are not in the initial DataFrame
full_moons = [date for date in full_moons if date in dates]

# Setting the number of days surrounding the full moon which are to be investigated
before_and_after = 10

# Finding the average percentage change of every day, relative to the adjusted close of the full moon day
average_percentage_changes = []
for i in range(before_and_after * 2 + 1):
    percentage_changes = []
    for date in full_moons:
        new_date = date - timedelta(before_and_after) + timedelta(i)
        full_moon_price = adjusted_closes[dates.index(date)]
        try:
            price = adjusted_closes[dates.index(new_date)]
        except:
            price = math.nan
        else:
            percentage_changes.append((price - full_moon_price) / full_moon_price * 100)
    average_percentage_changes.append(sum(percentage_changes) / len(percentage_changes))

# Creating a list of the days 
days_before_and_after = [i for i in range(- before_and_after, before_and_after + 1)]

# exporting all the data as a csv file 
full_moon_data = {
    "Days until full moon" : days_before_and_after,
    "Average Percentage Changes (in relation to full moon day price)" : average_percentage_changes,
    "If the full moon day price was $100" : [round(100 + i, 2) for i in average_percentage_changes]
    }
full_moon_df = pd.DataFrame(full_moon_data)
full_moon_df.to_csv(SPX_or_VIX + "_full_moon_data.csv")

# Creating an identifier for a new figure
plt.figure(0)

# Normal line graph
plt.plot(days_before_and_after, average_percentage_changes, color = "orange")

# Bar chart
plt.bar(days_before_and_after, average_percentage_changes, color = "blue")

# X-axis label
plt.xlabel("Days Before and After Full Moon")

# Y-axis label
plt.ylabel("Average Percentage Change")

# Graph title
plt.title("Percentage Change Relative to Full Moon Day")

# Display gridlines
plt.grid()

# Show the graph 
plt.show()


## A section of the above code is repeated but for the new moon instead
first_new_moon = ephem.next_new_moon(earliest_date)

first_new_moon = first_new_moon.datetime()

new_moons = [first_new_moon]
while True:
    new_moon = ephem.next_new_moon(new_moons[-1]).datetime()
    if new_moon > latest_date:
        break
    new_moons.append(new_moon)

new_moons = [date.date() for date in new_moons]

new_moons = [date for date in new_moons if date in dates]

before_and_after = 10

average_percentage_changes = []
for i in range(before_and_after * 2 + 1):
    percentage_changes = []
    for date in new_moons:
        new_date = date - timedelta(before_and_after) + timedelta(i)
        new_moon_price = adjusted_closes[dates.index(date)]
        try:
            price = adjusted_closes[dates.index(new_date)]
        except:
            price = math.nan
        else:
            percentage_changes.append((price - new_moon_price) / new_moon_price * 100)
    average_percentage_changes.append(sum(percentage_changes) / len(percentage_changes))

days_before_and_after = [i for i in range(- before_and_after, before_and_after + 1)]
new_moon_data = {
    "Days until full moon" : days_before_and_after,
    "Average Percentage Changes (in relation to new moon day price)" : average_percentage_changes,
    "If the new moon day price was $100" : [round(100 + i, 2) for i in average_percentage_changes]
    }

new_moon_df = pd.DataFrame(new_moon_data)
new_moon_df.to_csv(SPX_or_VIX + "_new_moon_data.csv")

plt.figure(1)
plt.plot(days_before_and_after, average_percentage_changes, color = "pink")
plt.bar(days_before_and_after, average_percentage_changes, color = "green")
plt.xlabel("Days Before and After New Moon")
plt.ylabel("Average Percentage Change")
plt.title("Percentage Change Relative to New Moon Day")
plt.grid()
plt.show()
