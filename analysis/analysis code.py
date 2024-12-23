import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the dataset
data_path = '/Data-Analytics-Intern-Project/data/cleaned marged data.xlsx'
data = pd.read_excel(data_path)

# Clean missing values
data['session_id'].fillna('Unknown', inplace=True)
data['dish_name_x'].fillna('Unknown', inplace=True)
data['meal_type_x'].fillna('Unknown', inplace=True)
data['order_status'].fillna('Unknown', inplace=True)
data['meal_type_y'].fillna('Unknown', inplace=True)
data['dish_name_y'].fillna('Unknown', inplace=True)

datetime_cols = ['session_start', 'session_end', 'order_date']
for col in datetime_cols:
    data[col] = pd.to_datetime(data[col], errors='coerce')
    data[col].fillna(method='ffill', inplace=True)

data['duration_(mins)'].fillna(data['duration_(mins)'].median(), inplace=True)
data['session_rating'].fillna(data['session_rating'].mean(), inplace=True)
data['amount_(usd)'].fillna(data['amount_(usd)'].mean(), inplace=True)
data['rating'].fillna(data['rating'].mean(), inplace=True)

# Check for missing data after cleaning
print(data.isnull().sum())

# Create images folder if not exists
if not os.path.exists('images'):
    os.makedirs('images')

# Popular dishes by total orders
popular_dishes = data.groupby('dish_name_x').agg(
    total_orders=('order_id', 'count')
).sort_values(by='total_orders', ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(popular_dishes.index, popular_dishes['total_orders'], color='skyblue')
plt.title('Top 10 Popular Dishes by Total Orders')
plt.xlabel('Total Orders')
plt.ylabel('Dish Name')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('images/popular_dishes.png')
plt.show()

# Age vs order amount
age_analysis = data.groupby('age').agg(
    avg_order_amount=('amount_(usd)', 'mean')
).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(age_analysis['age'], age_analysis['avg_order_amount'], marker='o', color='green')
plt.title('Average Order Amount by User Age')
plt.xlabel('User Age')
plt.ylabel('Average Order Amount (USD)')
plt.grid(True)
plt.tight_layout()
plt.savefig('images/age_vs_order_amount.png')
plt.show()

# Orders by location
orders_by_location = data.groupby('location').agg(
    total_orders=('order_id', 'count')
).sort_values(by='total_orders', ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(orders_by_location.index, orders_by_location['total_orders'], color='lightcoral')
plt.title('Top 10 Locations by Total Orders')
plt.xlabel('Total Orders')
plt.ylabel('Location')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('images/orders_by_location.png')
plt.show()

# Favorite meal vs total orders
favorite_meal_analysis = data.groupby('favorite_meal').agg(
    total_orders=('order_id', 'count')
).reset_index()

plt.figure(figsize=(8, 6))
plt.bar(favorite_meal_analysis['favorite_meal'], favorite_meal_analysis['total_orders'], color='lightgreen')
plt.title('Favorite Meal vs Total Orders')
plt.xlabel('Favorite Meal')
plt.ylabel('Total Orders')
plt.tight_layout()
plt.savefig('images/favorite_meal_vs_orders.png')
plt.show()

# Session ratings vs total orders
session_rating_vs_orders = data.groupby('session_rating').agg(
    total_orders=('order_id', 'count')
).reset_index()

plt.figure(figsize=(8, 6))
plt.bar(session_rating_vs_orders['session_rating'], session_rating_vs_orders['total_orders'], color='dodgerblue')
plt.title('Session Ratings vs Total Orders')
plt.xlabel('Session Rating')
plt.ylabel('Total Orders')
plt.tight_layout()
plt.savefig('images/session_ratings_vs_orders.png')
plt.show()

# Session duration vs total orders
session_duration_vs_orders = data.groupby('duration_(mins)').agg(
    total_orders=('order_id', 'count')
).reset_index()

plt.figure(figsize=(8, 6))
plt.plot(session_duration_vs_orders['duration_(mins)'], session_duration_vs_orders['total_orders'], marker='o', color='green')
plt.title('Duration of Sessions vs Total Orders')
plt.xlabel('Session Duration (Minutes)')
plt.ylabel('Total Orders')
plt.grid(True)
plt.tight_layout()
plt.savefig('images/duration_vs_orders.png')
plt.show()

print("Data analysis complete!")
