# WeatherWear Advisor - AI Agent

This project provides a LangChain-based agent that combines weather data retrieval and clothing suggestions based on the current weather conditions and temperature. It uses the OpenWeatherMap API for weather data and uses LangChain's tools to integrate functionalities.

## Features
- **Weather Tool**: Retrieves the current weather and temperature for a given location using the OpenWeatherMap API.
- **Clothing Suggestion Tool**: Provides clothing recommendations based on the weather conditions and temperature.
- **Interactive Agent**: Combines the tools into a LangChain agent for dynamic responses.

## Prerequisites
- Python 3.8 or higher
- An API key from [OpenWeatherMap](https://openweathermap.org/api)

## Installation
1. Clone the repository or copy the script.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Replace `YOUR_WEATHER_API_KEY` in the script with your OpenWeatherMap API key.
2. Run the script:
   ```bash
   python wwa.py
   ```
3. The agent will provide weather information and clothing suggestions based on the input location.

## Example
**Input:**
```
What's the weather in Dubai? Suggest what to wear.
```

**Output:**
```
Clear, 25°C
A light t-shirt and sunglasses would be great for sunny weather. A light jacket or sweater is recommended.
```

## Files
- `wwa.py`: Contains the main implementation of the agent.
- `requirements.txt`: Specifies the required Python packages.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author
Pradeep Kumar