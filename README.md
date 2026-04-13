# Wildlife Telemetry Dashboard 🛰️

Interactive web dashboard for visualizing animal GPS tracking data in real time, built with Flask and Leaflet.js.

## Features
- Interactive dark map with individual trajectories
- Click on individual to filter trajectory and see speed chart
- Real-time statistics per individual (records, avg/max speed)
- CSV data download
- REST API endpoints for tracks, stats and speed data

## Tech Stack
- Python · Flask · pandas
- Leaflet.js · Chart.js · CartoDB tiles

## Setup
```bash
git clone https://github.com/toshi-taz/telemetry-dashboard.git
cd telemetry-dashboard
pip install flask pandas
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## API Endpoints
- `GET /api/tracks` — GPS trajectories per individual
- `GET /api/stats` — movement statistics per individual  
- `GET /api/speed/<id>` — speed over time for one individual
- `GET /api/download` — full dataset as CSV

## Data
Fregata magnificens tracking data from MPIAB PNIC Hurricane Frigate Tracking study (Movebank).

## Author
Alexander Toshiro Bataz López  
Ingeniería en Sistemas Energéticos y Redes Inteligentes — UPIEM–IPN  
Conservation Technology | Wildlife Telemetry | IoT Sensor Networks
