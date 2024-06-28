import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -%(levelname)s - %(message)s')
def load_data(city):
    logging.info(f"Loading data for {city}")
    file_path = f"{city}.csv"
    return pd.read_csv(file_path)
def clean_data(df):
    logging.info("Cleaning data")
    df.dropna(inplace=True)
    return df
def most_popular_start_station(df):
    logging.info("Calculating the most popular start station")
    return df['Start Station'].mode()[0]
def trip_duration_stats(df):
    logging.info("Calculating trip duration statistics")
    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()
    median_duration = np.median(df['Trip Duration'])
    return total_duration, mean_duration, median_duration
def user_stats(df):
    logging.info("Calculating user statistics")
    user_types = df['User Type'].value_counts()
    genders = df['Gender'].value_counts() if 'Gender' in df.columns else "No gender data"
    return user_types, genders
def plot_trip_duration_distribution(df, city):
    logging.info(f"Plotting trip duration distribution for{city}")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Trip Duration'], bins=30, kde=False)
    plt.title(f'Distribution of Trip Durations in {city.title()}')
    plt.xlabel('Trip Duration')
    plt.ylabel('Frequency')
    plt.savefig(f'{city}_trip_duration_distribution.png')
def plot_user_types(df, city):
    logging.info(f"Plotting user types for {city}")
    plt.figure(figsize=(8, 5))
    user_types = df['User Type'].value_counts()
    user_types.plot(kind='bar')
    plt.title(f'User Types in {city.title()}')
    plt.xlabel('User Type')
    plt.ylabel('Count')
    plt.savefig(f'{city}_user_types.png')
def plot_gender_distribution(df, city):
    logging.info(f"Plotting gender distribution for {city}")
    if 'Gender' in df.columns:
        plt.figure(figsize=(8, 5))
        genders = df['Gender'].value_counts()
        genders.plot(kind='bar')
        plt.title(f'Gender Distribution in {city.title()}')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.savefig(f'{city}_gender_distribution.png')
def generate_word_cloud(df, city):
    logging.info(f"Generating word cloud for {city}")
    text = ' '.join(df['Start Station'].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400,
    background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud of Start Stations in {city.title()}')
    plt.savefig(f'{city}_word_cloud.png')
def generate_report(city):
    df = load_data(city)
    df = clean_data(df)
    start_station = most_popular_start_station(df)
    total_duration, mean_duration, median_duration = trip_duration_stats(df)
    user_types, genders = user_stats(df)
    plot_trip_duration_distribution(df, city)
    plot_user_types(df, city)
    plot_gender_distribution(df, city)
    generate_word_cloud(df, city)
    report = (
    f"City: {city}\n"
    f"Most Popular Start Station: {start_station}\n"
    f"Trip Duration (Total/Mean/Median):{total_duration}/{mean_duration}/{median_duration}\n"
    f"User Types:\n{user_types}\n"
    f"Genders:\n{genders}\n"
    )
    print(report)
    with open(f"{city}_report.txt", 'w') as f:
        f.write(report)
    logging.info(f"Report generated for {city}")
if __name__ == "__main__":
    cities = ['chicago', 'new_york_city', 'washington']
    for city in cities:
        generate_report(city)
