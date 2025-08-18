import os
import random
import json
import index as index
from Services.hotel_service import load_and_index_preferences, retrieve_context, generate_hotel_preferences

prompt = "Book a flight from Banglore to Amritsar on rainy day of this month"
# prompt = "What is the capital of India ?"

print('\n')
print('\n')
print('\n')
print("=========================================")
print("Welcome to the AI Travel Planner!")
print("=========================================")
print('\n')

# ------------------------------------------------------------------------------------------------
# 1.) Function call to get response from LLM (to extract entities)
print("Fetching response from LLM for the prompt:")
data = index.get_response_from_llm(prompt)
print("Response from LLM:")
print(data)
print("\n")
# Check if the response is a valid trip planning JSON
if isinstance(data, str):
    exit()
# Returns: 
"""
    For Success Case:
    {
        "status": "success",
        "data": {
            "source": "New York"
            "destination": "California",
            "weather_preference": "sunny",
            "travel_dates": "weekend",
            "hotel_preferences": null,
            "other_info": "family trip",
        }
    }

    For Case other than trip planning:
    {
        "status": "success",
        "data": "This AI agent is designed specifically to help plan trips. Please ask something like 'Plan a trip to CA on a sunny day'."
    }
"""

print("------------------------------------------------------------------------------------------------")
# 2.) Function call to get relevant date based on the weather by calling weather API
destination = data['destination']
weather_preference = data['weather_preference']
dates = index.get_relevant_dates_based_on_weather(destination, weather_preference, days=30)
print("Relevant dates based on weather condition:")
print(dates)
print("\n")
# return ['2025-08-18', '2025-08-20', '2025-08-21']

print("------------------------------------------------------------------------------------------------")
# 3.) Function to Query your calendar (stored in Postgres or Oracle) to find available dates.
EMPLOYEE_ID = 1001  # Harcharanpreet's ID
available_dates = index.get_available_dates(EMPLOYEE_ID)

print("📅 Upcoming holidays:")
for holiday in available_dates:
    print("→", holiday)
print("\n")
# return ['2025-08-18', '2025-08-20', '2025-08-21']

print("------------------------------------------------------------------------------------------------")

# 4.1) Get Hotel Preferences based on the user's query using RAG (Retrieval-Augmented Generation).
load_and_index_preferences("hotel_preferences.txt")
context = retrieve_context()
hotel_preference = generate_hotel_preferences(context)

print(" Final structured hotel preferences:")
print(hotel_preference)
print(json.dumps(hotel_preference, indent=4))

# 4.1) Function to Search for hotels with rating > 4 on available sunny days.
selected_date = random.choice(['2025-08-18', '2025-08-20', '2025-08-21'])
hotels = index.search_hotels(destination, selected_date, hotel_preference) 
print("Hotels with rating > 4 on available sunny days:")
print(hotels)
print("\n")

print("------------------------------------------------------------------------------------------------")
# 4.2) Function to Book hotel on available dates.
selected_hotel = random.choice(hotels)
print("Booking ", selected_hotel, " on ", selected_date)
print("\n")

print("------------------------------------------------------------------------------------------------")
# # 5.) Function to book a flight from source to destination on available dates.
# flight_booking = index.book_flight(data['source'], data['destination'], available_dates)
# print("Flight booking details:")
# print(flight_booking)
# print("\n")

# # 6.) Function to book a hotel on available dates.
# hotel_booking = index.book_hotel(data['destination'], available_dates)
# print("Hotel booking details:")
# print(hotel_booking)
# print("\n")

# # 7.) Function to send confirmation email with flight and hotel details.
# confirmation_email = index.send_confirmation_email(data['source'], data['destination'], flight_booking, hotel_booking)
# print("Confirmation email details:")
# print(confirmation_email)
# print("\n")

# Deleted lard file