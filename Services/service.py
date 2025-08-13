import os 
from dotenv import load_dotenv 
from openai import OpenAI 
import httpx 

#Load environment variables from .env file 
load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY") 

# Create client with custom timeout settings 
client = OpenAI( api_key=api_key, timeout=httpx.Timeout(60.0, connect=10.0) ) 

# Function to get response from LLM
def get_response_from_llm(prompt): 
    # Right now, I'm returning static response without calling LLM to build my app
    # In future, I will call LLM to get the response
    try: 
        result =  {
            "destination": "San Francisco",
            "source": "New York",
            "condition": "Sunny Day of this month"
        }
        return result
        response = client.chat.completions.create( 
            model="gpt",
            messages = [
                 {"role": "user","content": prompt} 
                ], timeout=30 ) 
        print("Response of the prompt is ", response) 
        return response 
    except Exception as e: 
        print(f"Error occurred: {e}") 
        return None 


# Function to get relevant dates based on weather condition
# This function receives a destination and a weather condition in string format
# and returns a list of relevant dates.
def get_relevant_dates_based_on_weather(destination, condition):
    # Right now, I'm returning static response without calling weather API to build my app
    # In future, I will call weather API to get the relevant dates
    try:
        # Here you would typically call a weather API to get the relevant dates
        # For example, you might use OpenWeatherMap or similar service
        print(f"2.) Fetching relevant dates for {destination} with condition {condition}")
        return ["2023-10-15", "2023-10-16", "2023-10-17"]
    except Exception as e:
        print(f"Error occurred while fetching dates: {e}")
        return []


# Function to get available dates from your calendar
def get_available_dates(source, destination, dates):
    # Right now, I'm returning static response without querying calendar to build my app
    # In future, I will query calendar to get the available dates
    try:
        print(f"3.) Fetching available dates from calendar for travel from {source} to {destination}")
        # Here you would typically query your calendar database (Postgres or Oracle)
        return ["2023-10-15", "2023-10-16"]
    except Exception as e:
        print(f"Error occurred while fetching available dates: {e}")
        return []
    

# Function to search for hotels with rating > 4 on available sunny days
def search_hotels(destination, available_dates):
    # Right now, I'm returning static response without searching hotels to build my app
    # In future, I will search hotels to get the available hotels
    try:
        print(f"4.) Searching for hotels in {destination} on available dates: {available_dates}")
        # Here you would typically call a hotel booking API or database
        return [
            {"hotel_name": "Hotel Sunshine", "rating": 4.5},
            {"hotel_name": "Sunny Stay", "rating": 4.2}
        ]
    except Exception as e:
        print(f"Error occurred while searching for hotels: {e}")
        return []
    
# Function to book a flight from source to destination on available dates
def book_flight(source, destination, available_dates):
    # Right now, I'm returning static response without booking flight to build my app
    # In future, I will book flight to get the booking details
    try:
        print(f"5.) Booking flight from {source} to {destination} on available dates: {available_dates}")
        return {"flight_number": "AA123", "departure": "2023-10-15", "arrival": "2023-10-15"}
    except Exception as e:
        print(f"Error occurred while booking flight: {e}")
        return None
    
# Function to book a hotel on available dates
def book_hotel(destination, available_dates):
    # Right now, I'm returning static response without booking hotel to build my app
    # In future, I will book hotel to get the booking details
    try:
        print(f"6.) Booking hotel in {destination} on available dates: {available_dates}")
        return {"hotel_name": "Hotel Sunshine", "check_in": "2023-10-15", "check_out": "2023-10-16"}
    except Exception as e:
        print(f"Error occurred while booking hotel: {e}")
        return None
    
# Function to send confirmation email with flight and hotel details
def send_confirmation_email(source, destination, flight_booking, hotel_booking):
    # Right now, I'm returning static response without sending email to build my app
    # In future, I will send email to get the confirmation details
    try:
        print(f"7.) Sending confirmation email for travel from {source} to {destination}")
        return {
            "email_to": source,
            "subject": "Travel Confirmation",
            "body": f"Flight booked: {flight_booking}, Hotel booked: {hotel_booking}"
        }
    except Exception as e:
        print(f"Error occurred while sending confirmation email: {e}")
        return None


