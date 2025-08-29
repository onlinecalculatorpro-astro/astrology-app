from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import pytz
from professional_astro import ProfessionalAstrologyEngine

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
        timezone_str = request.form.get('timezone', 'UTC')
        house_system = request.form.get('house_system', 'placidus')
        
        # Validate required fields
        if not birth_date or not birth_time:
            raise ValueError("Birth date and time are required")
        
        if not birth_city and (not latitude or not longitude):
            raise ValueError("Birth location or coordinates are required")
        
        # Parse date and time
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        # Create professional calculator instance
        calc = ProfessionalAstrologyEngine()
        
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
            if "coordinates needed" in location_name.lower():
                raise ValueError(f"Could not find coordinates for '{birth_city}'. Please try a different city name or use coordinates directly.")
        
        # Calculate professional birth chart
        chart_data = calc.calculate_professional_chart(
            birth_datetime, lat, lon, house_system
        )
        
        # Add metadata
        chart_data.update({
            'birth_date': birth_date,
            'birth_time': birth_time,
            'birth_location': location_name,
            'coordinates': f"{lat:.4f}, {lon:.4f}",
            'timezone': timezone_str
        })
        
        # Extract traditional fields for compatibility
        if 'planets' in chart_data:
            chart_data['sun_sign'] = chart_data['planets'].get('sun', {}).get('sign', 'Unknown')
            chart_data['moon_sign'] = chart_data['planets'].get('moon', {}).get('sign', 'Unknown')
            
            # Calculate ascendant from first house cusp
            if chart_data.get('houses'):
                chart_data['ascendant'] = chart_data['houses'][0].get('sign', 'Unknown')
            else:
                chart_data['ascendant'] = 'Calculating...'
        
        return render_template('professional_results.html', chart=chart_data)
        
    except ValueError as e:
        # User input errors
        return render_template('error.html', error=str(e))
    except Exception as e:
        # System errors - try fallback
        try:
            # Fallback to basic calculation
            from astro_calc import AstrologyCalculator
            basic_calc = AstrologyCalculator()
            
            lat, lon, location_name = basic_calc.get_coordinates_for_city(birth_city or "London")
            
            chart_data = {
                'birth_date': birth_date,
                'birth_time': birth_time,
                'birth_location': location_name,
                'sun_sign': basic_calc.get_sun_sign(birth_datetime),
                'moon_sign': basic_calc.get_moon_sign(birth_datetime),
                'ascendant': basic_calc.get_ascendant(birth_datetime, lat, lon),
                'planets': basic_calc.get_planetary_positions(birth_datetime),
                'calculation_method': 'Basic (Professional engine unavailable)'
            }
            
            return render_template('results.html', chart=chart_data)
            
        except Exception:
            error_msg = f"Calculation error: {str(e)}"
            return render_template('error.html', error=error_msg)

@app.route('/predictions', methods=['POST'])
def get_predictions():
    """Generate predictions based on transits"""
    try:
        # Get stored birth chart data (in real app, this would come from database)
        chart_data = request.get_json()
        prediction_date_str = chart_data.get('prediction_date')
        
        if not prediction_date_str:
            prediction_date = datetime.now()
        else:
            prediction_date = datetime.strptime(prediction_date_str, '%Y-%m-%d')
        
        calc = ProfessionalAstrologyEngine()
        
        # Get birth chart from session or database
        birth_chart = chart_data.get('birth_chart', {})
        
        predictions = calc.get_transit_predictions(birth_chart, prediction_date)
        
        return jsonify({
            'predictions': predictions,
            'prediction_date': prediction_date.strftime('%Y-%m-%d'),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """Enhanced API endpoint with professional features"""
    try:
        data = request.get_json()
        birth_date = data.get('birth_date')
        birth_time = data.get('birth_time')
        latitude = data.get('latitude', 0)
        longitude = data.get('longitude', 0)
        house_system = data.get('house_system', 'placidus')
        
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        calc = ProfessionalAstrologyEngine()
        
        result = calc.calculate_professional_chart(
            birth_datetime, latitude, longitude, house_system
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
