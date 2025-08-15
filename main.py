import os
import index as index

prompt = "Book a flight from New York to San Francisco on Sunny day of this month"

# 1.) Function call to get response from LLM (to extract entities)
# data = promptToData.get_response_from_llm(prompt)
print("Fetching response from LLM for the prompt:")
data = index.get_response_from_llm(prompt)
print("Response from LLM:")
print(data)
print("\n")

# # 2.) Function call to get relevant date based on the weather by calling weather API
# dates = index.get_relevant_dates_based_on_weather(data['destination'], data['condition'])
# print("Relevant dates based on weather condition:")
# print(dates)
# print("\n")

# # 3.) Function to Query your calendar (stored in Postgres or Oracle) to find available dates.
# available_dates = index.get_available_dates(data['source'], data['destination'], dates)
# print("Available dates based on your calendar:")
# print(available_dates)
# print("\n")

# # 4.) Function to Search for hotels with rating > 4 on available sunny days.
# hotels = index.search_hotels(data['destination'], available_dates)
# print("Hotels with rating > 4 on available sunny days:")
# print(hotels)
# print("\n")

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