from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask('HGN Project1')
app.config['MY_GEOLOCATION_KEY'] = os.getenv('MY_GEOLOCATION_KEY')
app.config['MY_WEATHER_KEY'] = os.getenv('MY_WEATHER_KEY')


@app.route('/api/hello')
def index():
    try:
        visitor_name = request.args.get('visitor_name', 'Anonymous').strip('"')
    except Exception as e:
        visitor_name = 'Anonymous'
    geo_location = get_geolocation()
    weather = get_weather_temperature(geo_location['longitude'], geo_location['latitude'])

    output = {
        "client_ip": geo_location['ip_address'],
        "location": geo_location['city'],
        "greeting": f"Hello, {visitor_name}!, the temperature is {weather['current']['temperature']} degrees Celsius in {geo_location['city']}"
    }
    print(output)
    return jsonify(output)


def get_geolocation():
    request_url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={app.config["MY_GEOLOCATION_KEY"]}'
    response = requests.get(request_url)
    result = json.loads(response.content)
    return result


def get_weather_temperature(long, lat):
    request_url = f"https://www.meteosource.com/api/v1/free/point?lat={lat}&lon={long}&sections=current&language=en&units=auto&key={app.config['MY_WEATHER_KEY']}"
    response = requests.get(request_url)
    result = json.loads(response.content)
    return result


if __name__ == '__main__':
    app.run(debug=True)
