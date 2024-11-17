# Travel Planner CLI Usage Guide

## Overview

Travel Planner is a command-line tool that provides weather information, flight options, and hotel recommendations for your travel plans.

## Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd travel_planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Basic Usage

```bash
# Using all default values (San Francisco to New York, 7 days from today)
python -m travel_planner

# Specify origin and destination
python -m travel_planner -o "London" -d "Paris"

# Specify travel date
python -m travel_planner -o "Tokyo" -d "Singapore" -D 2024-12-25
```

## Command Line Options

### Required Environment Variables

```bash
OPENAI_API_KEY=your_openai_key
WEATHER_API_KEY=your_weather_api_key
```

### Core Arguments

```bash
-o, --origin        Origin city (default: San Francisco)
-d, --destination   Destination city (default: New York)
-D, --date         Travel date in YYYY-MM-DD format (default: 7 days from today)
```

### Service Selection

```bash
# Skip weather information
python -m travel_planner --no-weather

# Skip flight search
python -m travel_planner --no-flights

# Skip hotel search
python -m travel_planner --no-hotels

# Only get weather
python -m travel_planner --no-flights --no-hotels
```

### Output Options

```bash
# Quiet mode (errors only)
python -m travel_planner -q

# JSON output
python -m travel_planner --json
```

## Examples

1. Basic search:

```bash
python -m travel_planner
```

2. International trip:

```bash
python -m travel_planner -o "London" -d "Paris" -D 2024-12-01
```

3. JSON output for automation:

```bash
python -m travel_planner --json > travel_plan.json
```

4. Weather only for a destination:

```bash
python -m travel_planner -d "Tokyo" --no-flights --no-hotels
```

5. Quiet mode with specific date:

```bash
python -m travel_planner -o "Berlin" -d "Rome" -D 2024-06-15 -q
```

## Error Codes

- 0: Success
- 1: General error (invalid input, service error)
- 130: User interrupted (Ctrl+C)

## Tips

1. Use proper city names (e.g., "New York" instead of "NY")
2. For cities with common names, add country (e.g., "Paris, France")
3. Dates must be between today and one year in the future
4. Use quotes around city names that contain spaces

## Common Issues and Solutions

1. Invalid City Name:

```bash
# Wrong
python -m travel_planner -o NY -d LA

# Correct
python -m travel_planner -o "New York" -d "Los Angeles"
```

2. Date Format:

```bash
# Wrong
python -m travel_planner -D 12-25-2024

# Correct
python -m travel_planner -D 2024-12-25
```

3. Cities with Same Names:

```bash
# Be specific
python -m travel_planner -o "Paris, France" -d "Paris, Texas"
```

## Advanced Usage

1. Combine multiple options:

```bash
python -m travel_planner \
  -o "London" \
  -d "Paris" \
  -D 2024-12-25 \
  --no-hotels \
  --json
```

2. Pipeline usage:

```bash
# Save to file
python -m travel_planner --json > travel_plan.json

# Process with jq (if installed)
python -m travel_planner --json | jq '.weather_forecast'
```

## Getting Help

```bash
# Show all options
python -m travel_planner --help
```
