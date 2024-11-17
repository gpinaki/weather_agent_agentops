#!/bin/bash

# Activate virtual environment
source weather-agent/bin/activate

# Run Streamlit app
streamlit run src/travel_planner/ui/app.py