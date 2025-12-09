import csv
import requests

access_key = 'f3c20c646e0b053e9927c2c15c9f346f'
BASE_URL = 'https://api.aviationstack.com/v1/flights'
params = {'access_key': access_key}  # Adjust limit as needed

response = requests.get(BASE_URL, params=params)
data = response.json()
print(data)

flights = data.get('data', [])

with open('flights_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
   writer = csv.writer(csvfile)
   # Write header
   writer.writerow([
       'Flight Number', 'Airline', 'Departure Airport', 'Arrival Airport',
       'Departure Scheduled', 'Departure Actual',
       'Arrival Scheduled', 'Arrival Actual', 'Status'
   ])
   # Write flight data
   for flight in flights:
       writer.writerow([
           flight.get('flight', {}).get('iata', ''),
           flight.get('airline', {}).get('name', ''),
           flight.get('departure', {}).get('airport', ''),
           flight.get('arrival', {}).get('airport', ''),
           flight.get('departure', {}).get('scheduled', ''),
           flight.get('departure', {}).get('actual', ''),
           flight.get('arrival', {}).get('scheduled', ''),
           flight.get('arrival', {}).get('actual', ''),
           flight.get('flight_status', '')
       ])
