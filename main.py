from datetime import datetime
import json
import requests
import random

# First section we are going to define the "nostalgia years" for each user.
# We hypothesize that people tend to romanticize music from their early- to mid-teen years.
# For this reason, we calculate what those years are for each user given their current age
# and the current year, which we pull using datetime.

number_of_songs_per_year = int(input("\n\nHow many songs per year would you like? Please type an integer (max 100): \n\n"))
age = int(input("\n\nWhat is your current age?:\n\n"))
prime_age_start = int(11)
prime_age_end = int(15)
prime_age_diff_counter = (prime_age_end - prime_age_start)
prime_age_range = prime_age_end - prime_age_start
current_year = int(datetime.now().year)
nostalgia_years_diff = age - prime_age_start
nostalgia_years_start = int(current_year) - nostalgia_years_diff

def nostalgia_years_generator():
    nostalgia_years_list = []
    if nostalgia_years_start < 1958:
        print("\n\nSorry! You're too old for Billboard Hot 100 charts! Congratulations!")
        quit()
    elif age <= prime_age_end:
        print("\n\nSorry! You are too young for nostalgia! Enjoy your youth!")
        quit()
    print(f"\n\nThe beginning of your Golden Age in Music is {nostalgia_years_start}.") 
    print("\n\nCongratulations! A lot of bangers from back then. Let's see what we can get...")

    for prime_years_counters in range(prime_age_range):
        if nostalgia_years_list == []:
            nostalgia_years_list.append(int(nostalgia_years_start))
        else:
            nostalgia_years_list.append(
                nostalgia_years_start + prime_years_counters
            )
    print(f"\n\nYour Golden Age of music are the years {nostalgia_years_list[0]}, {nostalgia_years_list[1]}, {nostalgia_years_list[2]}, and {nostalgia_years_list[3]}.")
    return nostalgia_years_list

# Now, we are going to determine what the specific date for the
# Year End Billboard Hot 100 release was for a given year.

valid_dates_db = requests.get('https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/valid_dates.json') # This is a database of valid dates for Billboard entries

def dates_finder(year):
    loaded_data = valid_dates_db.json()
    valid_dates_in_year = []
    for dates in loaded_data:
        if dates.startswith(f"{year}"):
            valid_dates_in_year.append(dates)
    
    last_date = max(valid_dates_in_year)
    return last_date

# This is a random number generator, which spits out a non-repeating
# selection from the top 100 songs in a given year. It's just a way of getting values as a list.

random_numbers = (random.sample(range(100), int(f"{number_of_songs_per_year}")))

years_list = nostalgia_years_generator() # list of the Nostalgia Years.

selected_date = []

# This pulls song data given an index number from a particular year, using the date
# we pulled above as "last_date", or the return output from "dates_finder()"

def song_selector(random_numbers, selected_date):
    song_list_for_given_year = []
    chart_req = requests.get(f'https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/date/{selected_date}.json')
    chart_data = chart_req.json()
    song_rank_list = chart_data.get("data")
    for random_number in random_numbers:
        song_selection = song_rank_list[random_number]['song']
        song_artist = song_rank_list[random_number]['artist']
        song_list_for_given_year.append(f"\"{song_selection}\" by {song_artist}")
    return (song_list_for_given_year)

# This gives us the list of valid dates we should draw from for our billboard entries,
# and compiles it tidily into a list we can work with.

def dates_maker(years_list):
    board_dates_list = []
    for year in years_list:
        new_date = dates_finder(year)
        board_dates_list.append(new_date)
    return board_dates_list

specific_dates_for_hot_100 = dates_maker(years_list)

# This compiles our selected entries into a nice list.

def final_list_compiler(specific_dates_for_hot_100):
    final_list = []
    for dates in specific_dates_for_hot_100:
        selected_date = dates
        final_entries = song_selector(random_numbers, selected_date)
        final_list.append(final_entries)
    return final_list

final_list = final_list_compiler(specific_dates_for_hot_100)

print("\n\nHere is your selection of Nostalgia Jams: \n")

# Tidily formats our list for printing.

def list_printer(final_list, years_list):
    for x in range(prime_age_diff_counter):
        print(f"\n{years_list[x]}\n")
        for y in range(number_of_songs_per_year):
            print(f"{final_list[x][y]}\n")
        


list_printer(final_list, years_list)