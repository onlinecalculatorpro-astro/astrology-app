from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import pytz
from astro_calc import AstrologyCalculator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_chart():
    try:
        # Get form data
        birth_date = request.form.get('birth_date')
        birth_time = request.form.get('birth_time')
        birth_city = request.form.get('birth_city', '').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        timezone = request.form.get('timezone', 'UTC')
        
        # Validate required fields
        if not birth_date or not birth_time:
            raise ValueError("Birth date and time are required")
        
        if not birth_city and (not latitude or not longitude):
            raise ValueError("Birth location or coordinates are required")
        
        # Parse date and time
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        # Create calculator instance
        calc = AstrologyCalculator()
        
        # Get coordinates - use provided coordinates or geocode city
        if latitude and longitude:
            try:
                lat, lon = float(latitude), float(longitude)
                # Validate coordinate ranges
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    raise ValueError("Invalid coordinates: Latitude must be -90 to 90, Longitude must be -180 to 180")
                location_name = f"{lat:.3f}°, {lon:.3f}°"
            except ValueError as e:
                raise ValueError(f"Invalid coordinates: {str(e)}")
        else:
            # Geocode the city name
            if len(birth_city) < 2:
                raise ValueError("Please enter a valid city name (at least 2 characters)")
            
            lat, lon, location_name = calc.get_coordinates_for_city(birth_city)
            
            # Check if location was found
            if "location not found" in location_name.lower():
                raise ValueError(f"Could not find coordinates for '{birth_city}'. Please try a different city name or use coordinates directly.")
        
        # Calculate astrology data
        sun_sign = calc.get_sun_sign(birth_datetime)
        moon_sign = calc.get_moon_sign(birth_datetime)
        ascendant = calc.get_ascendant(birth_datetime, lat, lon, timezone)
        planetary_positions = calc.get_planetary_positions(birth_datetime)
        
        chart_data = {
            'birth_date': birth_date,
            'birth_time': birth_time,
            'birth_location': location_name,
            'coordinates': f"{lat:.4f}, {lon:.4f}",
            'sun_sign': sun_sign,
            'moon_sign': moon_sign,
            'ascendant': ascendant,
            'planets': planetary_positions
        }
        
        return render_template('results.html', chart=chart_data)
        
    except ValueError as e:
        # User input errors
        return render_template('error.html', error=str(e))
    except Exception as e:
        # System errors
        error_msg = f"Calculation error: {str(e)}"
        return render_template('error.html', error=error_msg)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        birth_date = data.get('birth_date')
        birth_time = data.get('birth_time')
        
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        calc = AstrologyCalculator()
        
        result = {
            'sun_sign': calc.get_sun_sign(birth_datetime),
            'moon_sign': calc.get_moon_sign(birth_datetime),
            'ascendant': calc.get_ascendant(birth_datetime),
            'planets': calc.get_planetary_positions(birth_datetime)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
