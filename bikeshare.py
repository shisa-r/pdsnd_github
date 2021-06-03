import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    
    valid_city = ['chicago','new york city','washington']
    while True: 
        user_city = input("\nWhich city would you like to see the data? %s\n" % valid_city)
        if user_city.lower() not in valid_city:
            print("\nSorry!..invalid city")
        else: 
            user_city = user_city.lower()
            break
            
    valid_month = ['all','january','february','march','april','may','june']
    while True: 
        user_month = input("\nWhich month would you like to see the data? %s\n" % valid_month)
        if user_month.lower() not in valid_month:
            print("\nSorry!..invalid month")
        else:
            user_month = user_month.lower()
            break
    
    valid_day = ['all', 'monday', 'tuesday', 'wednesday','thursday', 'friday','saturday','sunday']
    while True: 
        user_day = input("\nWhich day of week would you like to see the data? %s\n" % valid_day)
        if user_day.lower() not in valid_day:
            print("\nSorry!..invalid day of week")
        else:
            user_day = user_day.lower()
            break

    return user_city, user_month, user_day

def load_data(city, month, day):    
    """
    Loads data for the specified city from get_filters function and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['start_time'] = pd.to_datetime(df['Start Time'])
    df['start_month'] = df.start_time.dt.month_name()
    df['start_day']   = df.start_time.dt.day_name()
    
    if month == 'all':
        df = df
    else:
        df = df[df.start_month == month.title()]

    if day == 'all':
        df = df
    else: 
        df = df[df.start_day == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time() 

    # display the most common month
    # display the most common day of week
    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name()
    df['dayname'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    print('Most Common Month of Travel:',df.month.mode()[0])
    print('Most Common Day of Travel:',df.dayname.mode()[0])
    print('Most Common Start Hour of Travel:', df['hour'].mode()[0])

    t = round((time.time() - start_time),2)

    print("\nThis took %s seconds" % t)
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # display most commonly used end station
    # display most frequent combination of start station and end station trip
    df['trip'] = 'FROM ' + df['Start Station'] + ' TO ' + df['End Station']

    print('Most Common Start Station:',df['Start Station'].mode()[0])
    print('Total counts: ',df['Start Station'].value_counts()[df['Start Station'].mode()][0])
    print('Most Common End Station:',df['End Station'].mode()[0])
    print('Total counts: ', df['End Station'].value_counts()[df['End Station'].mode()][0])
    print('Most Common Trip:',df.trip.mode()[0])
    print('Total counts: ',df.trip.value_counts()[df.trip.mode()][0])

    t = round((time.time() - start_time),2)

    print("\nThis took %s seconds" % t)
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # display mean travel time
    print('Total Travel Time: ',df['Trip Duration'].sum().round(2),'seconds')
    print('Average Travel Time: ',round(df['Trip Duration'].mean(),2),'seconds')

    t = round((time.time() - start_time),2)

    print("\nThis took %s seconds" % t)
    print('-'*40)

def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    print("User Type Breakdown:\n%s" % df['User Type'].value_counts())    
    if city.lower() in ['chicago','new york city']:
        print("\nGender Breakdown:\n%s" % df['Gender'].value_counts())
        print("\nYear of Birth Breakdown:")
        print("Earliest Year is %d" % df['Birth Year'].min())
        print("Most Recent Year is %d" % df['Birth Year'].max())
        print("Most Common Year is %d" % df['Birth Year'].mode()[0])
    elif city.lower() == 'washington':
        print("\nPlease note that Gender and Year of Birth data is not available for Washington")

    t = round((time.time() - start_time),2)

    print("\nThis took %s seconds" % t)
    print('-'*40)

def sample_data(df):
    sample = 'yes'
    while sample.lower() != 'no':
        sample = input('\nWould you like to see sample of raw data? Please enter yes or no\n')  
        if sample.lower() not in ('yes','no'):
            print('\nSorry!..invalid answer')
        elif sample.lower() == 'yes':
            i=5
            print(df.head(i))
            while True:
                sample_more = input('\nWould you like to see more data? Please enter yes or no\n')
                if sample_more.lower() not in ('yes','no'):
                    print('\nSorry!..invalid answer')
                elif sample_more.lower() == 'yes':
                    print(df[i:i+5])
                    i+=5
                elif sample_more.lower() == 'no':
                    sample = 'no'
                    break 

def main():
    restart = 'yes'
    while restart == 'yes': 
        city, month, day = get_filters()
        filter_data = load_data(city, month, day)
    
        time_stats(filter_data)
        station_stats(filter_data)
        trip_duration_stats(filter_data)
        user_stats(city,filter_data)
        sample_data(filter_data)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no\n')
            if restart.lower() not in ('yes','no'):
                print('\nSorry!..invalid answer')
            elif restart.lower() == 'yes':
                restart = 'yes'
                break
            elif restart.lower() == 'no':
                restart = 'no'
                break

if __name__ == "__main__":
    main()


