from flask import Flask, render_template, jsonify, Response
import pandas as pd
import numpy as np
import os
import math

app = Flask(__name__)

DATA_PATH = os.path.expanduser("~/wildlife-telemetry-pipeline/data/frigate_tracking.csv")

def cargar_datos():
    df = pd.read_csv(DATA_PATH)
    df = df[df["visible"] == True].dropna(subset=["location-lat", "location-long", "ground-speed"])
    df = df[np.isfinite(df["location-lat"]) & np.isfinite(df["location-long"]) & np.isfinite(df["ground-speed"])]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tracks")
def tracks():
    df = cargar_datos()
    individuos = []
    colores = ["red", "blue", "green", "purple", "orange"]
    for i, ind in enumerate(df["individual-local-identifier"].unique()):
        df_ind = df[df["individual-local-identifier"] == ind].sort_values("timestamp")
        df_sample = df_ind.iloc[::10]
        puntos = [[round(float(r["location-lat"]), 5), round(float(r["location-long"]), 5)]
                  for _, r in df_sample.iterrows()
                  if math.isfinite(r["location-lat"]) and math.isfinite(r["location-long"])]
        ultimo = df_ind.iloc[-1]
        individuos.append({
            "id": str(ind),
            "color": colores[i % len(colores)],
            "puntos": puntos,
            "ultimo": {
                "lat": round(float(ultimo["location-lat"]), 5),
                "lon": round(float(ultimo["location-long"]), 5),
                "timestamp": str(ultimo["timestamp"]),
                "speed": round(float(ultimo["ground-speed"]), 2)
            }
        })
    return jsonify(individuos)

@app.route("/api/stats")
def stats():
    df = cargar_datos()
    result = []
    for ind in df["individual-local-identifier"].unique():
        df_ind = df[df["individual-local-identifier"] == ind]
        result.append({
            "id": str(ind),
            "registros": len(df_ind),
            "vel_promedio": round(float(df_ind["ground-speed"].mean()), 2),
            "vel_max": round(float(df_ind["ground-speed"].max()), 2),
        })
    return jsonify(result)

@app.route("/api/speed/<individual_id>")
def speed(individual_id):
    df = cargar_datos()
    df_ind = df[df["individual-local-identifier"] == int(individual_id)].sort_values("timestamp")
    df_sample = df_ind.iloc[::20]
    result = [{"t": str(r["timestamp"]), "v": round(float(r["ground-speed"]), 2)}
              for _, r in df_sample.iterrows()]
    return jsonify(result)

@app.route("/api/download")
def download():
    df = cargar_datos()
    cols = ["individual-local-identifier", "timestamp", "location-lat", "location-long", "ground-speed"]
    csv = df[cols].to_csv(index=False)
    return Response(csv, mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=telemetry_data.csv"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
