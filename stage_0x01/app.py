from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask('HGN Project1')
app.config['MY_WEATHER_KEY'] = os.getenv('MY_WEATHER_KEY')


def get_geolocation(client_ip):
    request_url = 'http://ip-api.com/json/' + str(client_ip)
    response = requests.get(request_url)

    if response.status_code == 200:
        response_data = response.json()
    else:
        return jsonify({"error": "your city was not loaded successfully"})
    return response_data


def get_weather_temperature(long, lat):
    request_url = f"https://www.meteosource.com/api/v1/free/point?lat={lat}&lon={long}&sections=current&language=en&units=auto&key={app.config['MY_WEATHER_KEY']}"
    response = requests.get(request_url)
    print(f"Weather response status: {response.status_code}")
    if response.status_code != 200:
        return {}
    result = json.loads(response.content)
    return result


@app.route('/api/hello')
def index():
    try:
        visitor_name = request.args.get('visitor_name', 'Anonymous').strip('"')
    except Exception as e:
        visitor_name = 'Anonymous'

    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    geo_location = get_geolocation(client_ip)

    if 'lon' not in geo_location or 'lat' not in geo_location:
        return jsonify({"error": "Failed to get geolocation data"}), 500

    weather = get_weather_temperature(geo_location['lon'], geo_location['lat'])

    if 'current' not in weather or 'temperature' not in weather['current']:
        return jsonify({"error": "Failed to get weather data"}), 500

    output = {
        "client_ip": client_ip,
        "location": geo_location.get('city', 'N/A'),
        "greeting": f"Hello, {visitor_name}!, the temperature is {weather['current']['temperature']} degrees Celsius in {geo_location.get('city', 'N/A')}"
    }

    return jsonify(output)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
