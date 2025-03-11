import requests

api_key = "e751ccdcb271475045e5d6b91e247185"

url = f"https://api.openweathermap.org/data/2.5/weather?lat=59.4370&lon=24.7535&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    time = data['dt']
    temperature = data['main']['temp']

    print(f"Время: {time} | Температура: {temperature}°C")
else:
    print(f"Ошибка при запросе: {response.status_code}")
