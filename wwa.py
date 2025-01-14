from langchain.tools import BaseTool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

# Define the Weather Tool
class WeatherTool(BaseTool):
    name: str = "Weather Tool"
    description: str = "Get the current weather and temperature for a given location."
    
    def _run(self, location: str) -> str:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
            response = requests.get(url).json()
            if response["cod"] != 200:
                return f"Error: {response['message']}"
            weather = response["weather"][0]["main"]
            temperature = response["main"]["temp"]
            return f"{weather}, {temperature}°C"
        except Exception as e:
            return f"Failed to retrieve weather: {str(e)}"

class ClothingSuggestionTool(BaseTool):
    name: str = "Clothing Suggestion Tool"
    description: str = "Suggest appropriate clothing based on weather conditions and temperature."
    
    def _run(self, weather_and_temp: str) -> str:
        try:
            # Split the input into parts and clean whitespace
            parts = [p.strip() for p in weather_and_temp.split(",")]
            if len(parts) != 2:
                return "Invalid input format. Expected 'weather, temperature' or 'temperature, weather'."

            # Identify weather and temperature regardless of order
            weather = None
            temperature = None
            for part in parts:
                if "°c" in part.lower():  # Check for temperature part
                    try:
                        temperature = float(part.lower().replace("°c", "").strip())
                    except ValueError:
                        return f"Invalid temperature value: {part}"
                else:
                    weather = part.strip()

            # Validate parsed weather and temperature
            if weather is None or temperature is None:
                return "Invalid input format. Ensure both weather and temperature are provided."

            # Normalize weather input to lowercase for consistency
            weather = weather.lower()

            # Provide clothing suggestions based on weather
            if "rain" in weather:
                suggestion = "Wear a waterproof jacket and carry an umbrella."
            elif "clear" in weather:
                suggestion = "A light t-shirt and sunglasses would be great for sunny weather."
            elif "clouds" in weather or "cloudy" in weather:
                suggestion = "Wear comfortable layers as it might feel cool."
            elif "snow" in weather:
                suggestion = "Bundle up with a heavy coat, gloves, and a scarf."
            elif "haze" in weather:
                suggestion = "Wear light and breathable clothing, and consider using a mask if the air quality is poor."
            else:
                suggestion = "Dress comfortably for unique or uncommon weather conditions."

            # Adjust clothing suggestions based on temperature
            if temperature < 10:
                suggestion += " Also, wear warm clothing as it's quite cold."
            elif 10 <= temperature <= 20:
                suggestion += " A light jacket or sweater is recommended."
            elif temperature > 30:
                suggestion += " Stay cool with breathable fabrics like cotton or linen."

            return suggestion
        except Exception as e:
            return f"Failed to provide clothing suggestion: {str(e)}"



# Instantiate tools
weather_tool = WeatherTool()
clothing_tool = ClothingSuggestionTool()

# Initialize LangChain Agent
tools = [weather_tool, clothing_tool]
llm = ChatOpenAI(api_key=openai_api_key, temperature=0)  # Pass the API key from env variables

# Create the agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Run the agent with the input
place = input("Where are you travelling?\n")
response = agent.run(f"What's the weather in {place}? Suggest what to wear.")
print(response)