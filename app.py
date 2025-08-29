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
        birth_location = request.form.get('birth_location', 'UTC')
        
        # Parse date and time
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        # Create calculator instance
        calc = AstrologyCalculator()
        
        # Calculate astrology data
        sun_sign = calc.get_sun_sign(birth_datetime)
        moon_sign = calc.get_moon_sign(birth_datetime)
        ascendant = calc.get_ascendant(birth_datetime)
        planetary_positions = calc.get_planetary_positions(birth_datetime)
        
        chart_data = {
            'birth_date': birth_date,
            'birth_time': birth_time,
            'sun_sign': sun_sign,
            'moon_sign': moon_sign,
            'ascendant': ascendant,
            'planets': planetary_positions
        }
        
        return render_template('results.html', chart=chart_data)
        
    except Exception as e:
        return render_template('error.html', error=str(e))

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
