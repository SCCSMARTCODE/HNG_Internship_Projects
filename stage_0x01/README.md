# HNG 11 Backend Stage 1


This project sets up a basic Flask web server with an API endpoint to greet visitors and provide weather information.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- requests

### Installation

1. Clone the repository:

    ```bash
    git https://github.com/SCCSMARTCODE/HNG_Internship_Projects.git
    cd HNG_Internship_Projects
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Set your API keys for geolocation and weather in the `app.config`:

    ```python
    app.config['MY_GEOLOCATION_KEY'] = 'your_geolocation_api_key'
    app.config['MY_WEATHER_KEY'] = 'your_weather_api_key'
    ```

2. Run the Flask application:

    ```bash
    python app.py
    ```

3. Access the API endpoint in your browser or using `curl`:

    ```
    http://localhost:5000/api/hello?visitor_name="Mark"
    ```
