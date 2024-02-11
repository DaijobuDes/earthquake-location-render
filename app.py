from flask import Flask, render_template, request, redirect, url_for, jsonify
from driver import Driver
import sys
import time
import json

app = Flask(__name__)

def check_lat_long_mag(lat, long, mag):
    try:
        lat, long, mag = map(float, (lat, long, mag))

        valid_lat = -90 <= lat <= 90
        valid_long = -180 <= long <= 180
        valid_mag = mag >= 0

        return not (valid_lat and valid_long and valid_mag)
    except Exception:
        return False


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/render')
def render():
    latitude = request.args.get('lat', None)
    longitude = request.args.get('long', None)
    zoom = request.args.get('zoom', 8)
    magnitude = request.args.get('mag', None)

    if not (latitude or longitude or magnitude):
        return jsonify({'error': 'Invalid arguments'}), 500

    if check_lat_long_mag(latitude, longitude, magnitude):
        return jsonify({'error': 'Invalid arguments'}), 500

    latitude, longitude, magnitude = map(float, (latitude, longitude, magnitude))

    try:
        browser = Driver()
        browser.window_size()

        browser.fetch_page(
            f"http://flask-app:5000/capture?lat={latitude}&long={longitude}&mag={magnitude}&zoom={zoom}"
        )
        time.sleep(2)

        output_file = f"{latitude}-{longitude}-{magnitude}.png"
        browser.save_screenshot(f"./img/{output_file}")
        browser.quit()
    except Exception as e:
        browser.quit()
        return jsonify({'error': "Browser error."}), 500

    return redirect(url_for('capture',
                            lat=latitude,
                            long=longitude,
                            zoom=zoom,
                            mag=magnitude
                           ),
                    code=302
                   )

@app.route('/capture', methods=['GET'])
def capture():
    latitude = request.args.get('lat')
    longitude = request.args.get('long')
    zoom = request.args.get('zoom', 8)
    magnitude = request.args.get('mag')

    if not (latitude or longitude or magnitude):
        return render_template('capture.html', flag=False)

    if check_lat_long_mag(latitude, longitude, magnitude):
        return jsonify({'error': 'Invalid arguments'}), 500

    magnitude_colors = {
        7: '{color: "#ff0000", fillColor: "#7f0000", fillOpacity: 0.2, radius: 400000}',
        6: '{color: "#ffff00", fillColor: "#7f7f00", fillOpacity: 0.2, radius: 300000}',
        5: '{color: "#ff00bf", fillColor: "#ff00bf", fillOpacity: 0.2, radius: 200000}',
        4: '{color: "#00bfff", fillColor: "#00bfff", fillOpacity: 0.2, radius: 100000}',
        3: '{color: "#00ff00", fillColor: "#00ff00", fillOpacity: 0.01, radius: 50000}',
    }
    default_color = '{color: "#00ff00", fillColor: "#00ff00", fillOpacity: 0.01, radius: 50000}'

    for i in range(8, 12):
        magnitude_colors[i] = magnitude_colors[7]

    color = magnitude_colors.get(int(round(float(magnitude))), default_color)

    latitude, longitude, magnitude = map(float, (latitude, longitude, magnitude))

    return render_template('capture.html',
                           longitude=longitude,
                           latitude=latitude,
                           zoom=zoom,
                           color=color,
                           magnitude=magnitude,
                           flag=True
                          )


if  __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
