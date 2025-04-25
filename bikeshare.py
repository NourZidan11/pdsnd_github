import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = input('Enter the city you want see data for Chicago , New York City or Washington : ')
    city = city.casefold()
    while city not in CITY_DATA:
        city = input('Invalid city name. Please Try Again! ')
        city = city.casefold()
        
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Enter the month from January to June OR Enter "all" for no month filter : ')
    month = month.casefold()
    while month not in months:
        month = input('Invalid month name. Please Try Again! ')
        month = month.casefold()
        
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Enter the day from Monday to Sunday OR Enter "all" for no day filter : ')
    day = day.casefold()
    while day not in days:
        day = input('Invalid day name. Please Try Again! ')
        day = day.casefold()

    print('='*50)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Popular Month:', months[popular_month-1])

    df['day_of_week'] = df['Start Time'].dt.dayofweek
    popular_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('Most Popular Day:', days[popular_day])

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Popular Start Station: ', df['Start Station'].mode()[0])
    print('Most Popular End Station: ', df['End Station'].mode()[0])
    print('\nMost Frequent Combination of Start and End Station Trips:\n\n',
          df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Trip Duration:', df['Trip Duration'].sum())
    print('Mean Trip Duration:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types, '\n')

    if 'Gender' in df.columns:    
        gender = df['Gender'].value_counts()
        print(gender, '\n')

    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', df['Birth Year'].min())
        print('Most Recent year of Birth:', df['Birth Year'].max())
        print('Most Common year of Birth:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)

# This is the main function that controls the flow of the program

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        valid_responses = ['yes', 'no']
        user_input = input('Would you like to see more data? (Enter: Yes/No)\n')
        
        while user_input.lower() not in valid_responses:
            user_input = input('Please enter Yes or No:\n')
        
        n = 0        
        while user_input.lower() == 'yes':
            print(df.iloc[n: n + 5])
            n += 5
            user_input = input('Would you like to see more data? (Enter: Yes/No)\n')
            while user_input.lower() not in valid_responses:
                user_input = input('Please enter Yes or No:\n')

        restart = input('Would you like to restart? (Enter: Yes/No)\n')
        while restart.lower() not in valid_responses:
            restart = input('Please enter Yes or No:\n')

        if restart.lower() != 'yes':
            print('BYE!')
            break


if __name__ == "__main__":
    main()
