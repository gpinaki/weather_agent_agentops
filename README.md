# AI Agent Observatory: Travel Planning Demo System 🤖

A demonstration project showcasing multi-agent AI system architecture, agent interactions, and monitoring capabilities. Uses a travel planning scenario to illustrate agent cooperation, error handling, and system observability.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-LLM%20Agent-green.svg)](https://openai.com/)
[![WeatherAPI](https://img.shields.io/badge/WeatherAPI-External%20Agent-yellow.svg)](https://www.weatherapi.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Visualization-red.svg)](https://streamlit.io/)

## Agent System Architecture 🎯

This project demonstrates how multiple AI agents can work together in a coordinated system:

```mermaid
graph TD
    A[TravelPlannerAgent] --> B[WeatherAgent]
    A --> C[FlightAgent]
    A --> D[HotelAgent]
    B --> E[Weather API]
    C --> F[LLM/OpenAI]
    D --> F[LLM/OpenAI]
    A --> G[Error Handling]
    A --> H[Monitoring]
```

### Agent Roles and Interactions

1. **Orchestrator Agent** (`TravelPlannerAgent`)
   - Coordinates all sub-agents
   - Handles error propagation
   - Manages parallel execution
   - Consolidates results

2. **API Integration Agent** (`WeatherAgent`)
   - Interfaces with external weather API
   - Validates city names
   - Handles real-world data

3. **LLM-Powered Agents** (`FlightAgent`, `HotelAgent`)
   - Use OpenAI for simulated data generation
   - Structured output formatting
   - Context-aware responses

4. **Monitoring System**
   - Tracks agent interactions
   - Measures response times
   - Logs errors and validations
   - Provides observability

## Agent Communication Flow 🔄

```mermaid
sequenceDiagram
    participant User
    participant TravelPlanner
    participant WeatherAgent
    participant FlightAgent
    participant HotelAgent
    participant Monitoring

    User->>TravelPlanner: Search Request
    TravelPlanner->>Monitoring: Start Tracking
    par Parallel Execution
        TravelPlanner->>WeatherAgent: Get Weather
        WeatherAgent-->>TravelPlanner: Weather Data
        and
        TravelPlanner->>FlightAgent: Get Flights
        FlightAgent-->>TravelPlanner: Flight Options
        and
        TravelPlanner->>HotelAgent: Get Hotels
        HotelAgent-->>TravelPlanner: Hotel Options
    end
    TravelPlanner->>Monitoring: Log Results
    TravelPlanner-->>User: Combined Results
```

## Educational Purpose ⚠️

**Note**: This is a demonstration project designed to illustrate:
- Multi-agent system architecture
- Agent communication patterns
- Error handling in distributed systems
- System monitoring and observability
- LLM integration techniques

**This is not a real travel planning system** - flight and hotel data are simulated using LLM for educational purposes.

## Key Learning Points 📚

1. **Agent Design Patterns**
   - Base agent abstraction
   - Specialized agent implementations
   - Agent coordination strategies

2. **Error Handling**
   - Graceful degradation
   - Error propagation
   - User feedback

3. **Monitoring Implementation**
   - Agent performance tracking
   - Error rate monitoring
   - System health metrics

4. **LLM Integration**
   - Structured prompt design
   - Response parsing
   - Error handling

[Rest of the installation and usage instructions remain the same...]

## System Components 🔧

### 1. Agent Layer
```python
class BaseAgent(ABC):
    """Base agent interface"""
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass

class TravelPlannerAgent(BaseAgent):
    """Orchestrator agent"""
    async def execute(self):
        # Coordinate other agents
        # Handle errors
        # Monitor performance
```

### 2. Monitoring Layer
```python
# Monitor agent interactions
with monitoring.trace("agent_execution"):
    result = await agent.execute()
    monitoring.log_metrics({
        "response_time": result.duration,
        "success": result.success
    })
```

### 3. Error Handling
```python
try:
    await agent.execute()
except CityValidationError:
    # Handle validation errors
except ServiceError:
    # Handle service errors
```

## Use Cases for Learning 📖

1. **Agent System Design**
   - Study multi-agent architecture
   - Learn coordination patterns
   - Understand error propagation

2. **LLM Integration**
   - Prompt engineering
   - Response handling
   - Error management

3. **System Monitoring**
   - Performance tracking
   - Error rate monitoring
   - System health checks

## Future Learning Opportunities 🎓

- [ ] Add more agent types
- [ ] Implement different coordination patterns
- [ ] Enhance monitoring capabilities
- [ ] Add more complex error scenarios
- [ ] Implement agent memory
- [ ] Add agent learning capabilities

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-planner-pro.git
cd travel-planner-pro
```

2. Create and activate virtual environment:
```bash
python -m venv weather-agent
source weather-agent/bin/activate  # On Windows: weather-agent\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_openai_key
# WEATHER_API_KEY=your_weather_api_key
```

## Usage 💻

### Web Interface
```bash
streamlit run streamlit/app.py
```
![Streamlit Interface](path_to_screenshot.png)

### Command Line Interface
```bash
# Basic usage
python -m travel_planner

# Custom search
python -m travel_planner -o "London" -d "Paris" -D 2024-12-01

# See all options
python -m travel_planner --help
```

For detailed CLI usage, see [USAGE.md](USAGE.md)

## Project Structure 📁
```
travel_planner/
├── src/
│   └── travel_planner/
│       ├── __init__.py
│       ├── __main__.py        # CLI entry point
│       ├── agents/            # Core logic
│       ├── schemas/           # Data models
│       └── utils/             # Helpers
├── streamlit/                 # Web interface
├── requirements.txt
└── .env
```

## Technologies Used 🛠️

- **Python 3.10+**: Core programming language
- **OpenAI API**: Flight and hotel recommendations
- **WeatherAPI**: Real weather data
- **Streamlit**: Web interface
- **Pydantic**: Data validation
- **Plotly**: Data visualization
- **Colorama**: CLI formatting

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Getting API Keys 🔑

1. **OpenAI API Key**:
   - Sign up at [OpenAI](https://openai.com/)
   - Create an API key in your dashboard
   - Add to `.env` file

2. **WeatherAPI Key**:
   - Register at [WeatherAPI](https://www.weatherapi.com/)
   - Get your API key
   - Add to `.env` file

## Future Improvements 🚀

- [ ] Add more travel services
- [ ] Implement caching
- [ ] Add more analytics
- [ ] Support more cities
- [ ] Add trip planning features
- [ ] Enhance error handling
- [ ] Add unit tests

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

This project was developed by Pinaki Guha, with supplementary support from AI-based code assistance tools like ChatGPT, Claude, and GitHub Copilot, to streamline specific parts of the development process.

## Support 💪

If you like this project, please give it a ⭐️!

## Contact 📧

Your Name - [Your Email](mailto:pinaki.guha@gmail.com)

Project Link: [https://github.com/yourusername/travel-planner-pro](https://github.com/yourusername/travel-planner-pro)