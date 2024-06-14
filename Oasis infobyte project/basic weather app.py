import requests

def get_weather_data(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        F = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        return F, humidity, description
    else:
        print(f"Error: Unable to fetch weather data for '{location}'.")
        return None, None, None


if __name__ == "__main__":
    api_key = "6ddec2f560686e41e571e8cd7fe99e48"
    location = input("Enter the city name or ZIP code: ")

    F, humidity, description = get_weather_data(api_key, location)

    if F is not None:
        print(f"Fahrenheit: {F}°F")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description.capitalize()}")

        C = (F - 32) * 5/9
        print(f"Celsius: {C}°C")