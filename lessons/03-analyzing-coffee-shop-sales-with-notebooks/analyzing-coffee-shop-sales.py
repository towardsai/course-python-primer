# Data Setup

coffee_sales = {
    "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "coffee_sold": [50, 55, 60, 52, 70, 90, 85],
    "tea_sold": [20, 18, 25, 22, 30, 35, 33],
    "revenue": [250, 270, 300, 260, 350, 450, 430]
}

print(coffee_sales)  # You should see the entire dictionary displayed.

# Average Daily Revenue

revenue_list = coffee_sales["revenue"]

total_revenue = 0
for amount in revenue_list:
    total_revenue = total_revenue + amount

average_revenue = total_revenue / len(revenue_list)
print(average_revenue)  # Expected result: 330.0

# Most Popular Day for Coffee Sales

coffee_list = coffee_sales["coffee_sold"]
day_list = coffee_sales["day"]

max_coffee = 0
max_day = ""

index = 0
while index < len(coffee_list):
    if coffee_list[index] > max_coffee:
        max_coffee = coffee_list[index]
        max_day = day_list[index]
    index = index + 1

print(max_day, "with", max_coffee, "coffees sold")
# Expected result: Saturday with 90 coffees sold

# Total Weekly Revenue

revenue_list = coffee_sales["revenue"]

weekly_revenue = 0
for amount in revenue_list:
    weekly_revenue = weekly_revenue + amount

print(weekly_revenue)  # Expected result: 2310

# Simple “Correlation” Between Coffee Sales and Revenue

coffee_list = coffee_sales["coffee_sold"]
revenue_list = coffee_sales["revenue"]

# Compute average coffee sold
total_coffee_sold = 0
for cups in coffee_list:
    total_coffee_sold = total_coffee_sold + cups

average_coffee_sold = total_coffee_sold / len(coffee_list)

# We already have average_revenue from the step where we computed the daily average revenue.
# But let's recompute it here to be self-contained.
total_revenue = 0
for amount in revenue_list:
    total_revenue = total_revenue + amount

average_revenue = total_revenue / len(revenue_list)

# Count how many days have above-average coffee and also above-average revenue
days_coffee_above_average = 0
days_coffee_and_revenue_above_average = 0

index = 0
while index < len(coffee_list):
    if coffee_list[index] > average_coffee_sold:
        days_coffee_above_average = days_coffee_above_average + 1
        if revenue_list[index] > average_revenue:
            days_coffee_and_revenue_above_average = days_coffee_and_revenue_above_average + 1
    index = index + 1

print(days_coffee_and_revenue_above_average, "out of", days_coffee_above_average)
# This tells us how many above-average coffee days also have above-average revenue.
# 3 out of 3

if days_coffee_above_average > 0:
    ratio = days_coffee_and_revenue_above_average / days_coffee_above_average
    print("Ratio of above-average coffee days also having above-average revenue:", ratio)
# You can interpret ratio close to 1.0 as a stronger positive relationship.
# Ratio of above-average coffee days also having above-average revenue: 1.0

# Average Sales on Weekdays vs Weekend

coffee_list = coffee_sales["coffee_sold"]
day_list = coffee_sales["day"]

weekday_total = 0
weekday_count = 0
weekend_total = 0
weekend_count = 0

index = 0
while index < len(day_list):
    current_day = day_list[index]
    current_coffee_sales = coffee_list[index]

    if current_day == "Saturday" or current_day == "Sunday":
        weekend_total = weekend_total + current_coffee_sales
        weekend_count = weekend_count + 1
    else:
        weekday_total = weekday_total + current_coffee_sales
        weekday_count = weekday_count + 1

    index = index + 1

if weekday_count != 0:
    average_weekday_coffee = weekday_total / weekday_count
else:
    average_weekday_coffee = 0

if weekend_count != 0:
    average_weekend_coffee = weekend_total / weekend_count
else:
    average_weekend_coffee = 0

print("Average weekday coffee sales:", average_weekday_coffee)
print("Average weekend coffee sales:", average_weekend_coffee)
# Expected result: 57.4 for weekdays, 87.5 for weekends

# Days Exceeding a Coffee Sales Threshold

coffee_list = coffee_sales["coffee_sold"]

threshold = 60
days_exceeding_threshold = 0

for cups in coffee_list:
    if cups >= threshold:
        days_exceeding_threshold = days_exceeding_threshold + 1

print("Days that exceeded threshold:", days_exceeding_threshold)
# Now you see 4, as expected, after re-running the cell.