from flask import Flask, request, jsonify
import requests
import json

app = Flask('HGN Project1')
app.config['MY_GEOLOCATION_KEY'] = '2b11e989f2254cbe9b8de6c751514a5e'
app.config['MY_WEATHER_KEY'] = 'f7l11gptamt54sc6gdg9cmtqxh2t9ro571a4uced'


@app.route('/api/hello')
def index():
    visitor_name = request.args.get('visitor_name').strip('"') or 'Anonymous'
    geo_location = get_geolocation()
    weather = get_weather_temperature(geo_location['longitude'], geo_location['latitude'])

    output = {
         "client_ip": f"{geo_location['ip_address']}",
          "location": f"{geo_location['city']}",
          "greeting": f"Hello, {visitor_name}!, the temperature is {weather['current']['temperature']} degrees Celcius in {geo_location['city']}"
    }
    print(output)
    return jsonify(output)


def get_geolocation():
    request_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + app.config['MY_GEOLOCATION_KEY']
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
