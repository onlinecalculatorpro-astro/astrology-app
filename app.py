from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import pytz
from professional_astro import ProfessionalAstrologyEngine

# Import our enhanced engine
try:
    from engines.base_engine import EnhancedBaseEngine
    ENHANCED_ENGINE_AVAILABLE = True
except ImportError:
    ENHANCED_ENGINE_AVAILABLE = False
    print("Enhanced engine not available - using standard calculations")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_enhanced():
    """Test route to verify enhanced calculations work"""
    if not ENHANCED_ENGINE_AVAILABLE:
        return """
        <h1>❌ Enhanced Engine Not Available</h1>
        <p>The enhanced engine could not be loaded.</p>
        <p>Please check that the engines/base_engine.py file exists.</p>
        <p><a href="/">← Back</a></p>
        """
    
    try:
        # Create enhanced engine
        engine = EnhancedBaseEngine({
            'precision': 'HIGH',
            'enable_logging': True
        })
        
        # Test date - January 1, 2024 at noon UTC
        test_date = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        
        # Run enhanced calculations
        jd = engine.precise_julian_day(test_date)
        sun_lon = engine.enhanced_sun_longitude(jd)
        moon_lon = engine.enhanced_moon_longitude(jd)
        ayanamsa = engine.calculate_ayanamsa(jd, 'LAHIRI')
        sidereal_sun = engine.tropical_to_sidereal(sun_lon, jd, 'LAHIRI')
        planets = engine.enhanced_planetary_positions(jd)
        stats = engine.get_performance_stats()
        
        # Format results as HTML
        results_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Engine Test Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                .success {{ color: green; }}
                .test-result {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .planet {{ margin: 5px 0; }}
                h1, h2, h3 {{ color: #333; }}
                a {{ color: #007bff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>🧪 Enhanced Astrology Engine Test Results</h1>
            
            <div class="test-result">
                <h3>✅ Basic Calculations</h3>
                <p><strong>Test Date:</strong> {test_date.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p><strong>Precise Julian Day:</strong> {jd:.8f}</p>
            </div>
            
            <div class="test-result">
                <h3>🌟 Enhanced Astronomical Positions</h3>
                <p><strong>Enhanced Sun Longitude:</strong> {sun_lon:.6f}°</p>
                <p><strong>Enhanced Moon Longitude:</strong> {moon_lon:.6f}°</p>
                <p><strong>Lahiri Ayanamsa:</strong> {ayanamsa:.6f}°</p>
                <p><strong>Sidereal Sun Position:</strong> {sidereal_sun:.6f}°</p>
            </div>
            
            <div class="test-result">
                <h3>🪐 Enhanced Planetary Positions</h3>
        """
        
        for planet, longitude in planets.items():
            # Convert to sign
            sign_index = int(longitude // 30)
            sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
            sign_degrees = longitude % 30
            
            results_html += f"""
                <p class="planet"><strong>{planet.capitalize()}:</strong> 
                {longitude:.4f}° ({sign_degrees:.2f}° {sign_names[sign_index]})</p>
            """
        
        results_html += f"""
            </div>
            
            <div class="test-result">
                <h3>📊 Performance Statistics</h3>
                <p>{stats}</p>
            </div>
            
            <div class="success">
                <h2>🎉 Enhanced Engine Working Successfully!</h2>
                <p>All precision calculations are functioning correctly.</p>
                <p>Ready to integrate with your birth chart calculator!</p>
            </div>
            
            <p><a href="/">← Back to Birth Chart Calculator</a></p>
            <p><a href="/calculate-enhanced">→ Try Enhanced Chart Calculation</a></p>
        </body>
        </html>
        """
        
        return results_html
        
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Engine Test Failed</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; color: #d32f2f; }}
                .error {{ background: #ffebee; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>❌ Enhanced Engine Test Failed</h1>
            <div class="error">
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Error Type:</strong> {type(e).__name__}</p>
            </div>
            <p><a href="/">← Back to Birth Chart Calculator</a></p>
        </body>
        </html>
        """

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

@app.route('/calculate-enhanced', methods=['GET', 'POST'])
def calculate_enhanced_chart():
    """New enhanced calculation endpoint using precision engine"""
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Chart Calculator</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                input, select { margin: 10px; padding: 8px; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🌟 Enhanced Precision Chart Calculator</h1>
            <form method="POST">
                <p>
                    <label>Birth Date:</label><br>
                    <input type="date" name="birth_date" required>
                </p>
                <p>
                    <label>Birth Time:</label><br>
                    <input type="time" name="birth_time" required>
                </p>
                <p>
                    <label>Birth City:</label><br>
                    <input type="text" name="birth_city" placeholder="e.g. New York, London, Mumbai">
                </p>
                <p>
                    <label>Ayanamsa System:</label><br>
                    <select name="ayanamsa">
                        <option value="LAHIRI">Lahiri (Standard)</option>
                        <option value="RAMAN">Raman</option>
                        <option value="KP">Krishnamurti Paddhati</option>
                    </select>
                </p>
                <p>
                    <button type="submit">Calculate Enhanced Chart</button>
                </p>
            </form>
            <p><a href="/">← Back to Standard Calculator</a></p>
        </body>
        </html>
        """
    
    # POST request - calculate chart
    if not ENHANCED_ENGINE_AVAILABLE:
        return "Enhanced engine not available. Please check the installation."
    
    try:
        birth_date = request.form.get('birth_date')
        birth_time = request.form.get('birth_time')
        birth_city = request.form.get('birth_city', '').strip()
        ayanamsa_system = request.form.get('ayanamsa', 'LAHIRI')
        
        # Parse date and time
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        # Get coordinates
        from astro_calc import AstrologyCalculator
        basic_calc = AstrologyCalculator()
        lat, lon, location_name = basic_calc.get_coordinates_for_city(birth_city or "London")
        
        # Create enhanced engine
        engine = EnhancedBaseEngine({'precision': 'HIGH'})
        
        # Calculate with enhanced precision
        jd = engine.precise_julian_day(birth_datetime.replace(tzinfo=timezone.utc))
        
        # Get enhanced planetary positions
        sun_tropical = engine.enhanced_sun_longitude(jd)
        moon_tropical = engine.enhanced_moon_longitude(jd)
        planets_tropical = engine.enhanced_planetary_positions(jd)
        planets_tropical['sun'] = sun_tropical
        planets_tropical['moon'] = moon_tropical
        
        # Convert to sidereal using selected ayanamsa
        ayanamsa_value = engine.calculate_ayanamsa(jd, ayanamsa_system)
        
        enhanced_chart = {
            'birth_info': {
                'date': birth_date,
                'time': birth_time,
                'location': location_name,
                'coordinates': f"{lat:.4f}, {lon:.4f}",
                'ayanamsa_system': ayanamsa_system,
                'ayanamsa_value': f"{ayanamsa_value:.6f}°"
            },
            'planets_tropical': {},
            'planets_sidereal': {},
            'calculation_method': 'Enhanced Precision Engine'
        }
        
        sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        for planet, tropical_lon in planets_tropical.items():
            sidereal_lon = engine.tropical_to_sidereal(tropical_lon, jd, ayanamsa_system)
            
            # Tropical position
            trop_sign_idx = int(tropical_lon // 30)
            trop_degrees = tropical_lon % 30
            
            # Sidereal position  
            sid_sign_idx = int(sidereal_lon // 30)
            sid_degrees = sidereal_lon % 30
            
            enhanced_chart['planets_tropical'][planet] = {
                'longitude': tropical_lon,
                'sign': sign_names[trop_sign_idx],
                'degrees': trop_degrees,
                'formatted': f"{trop_degrees:.2f}° {sign_names[trop_sign_idx]}"
            }
            
            enhanced_chart['planets_sidereal'][planet] = {
                'longitude': sidereal_lon,
                'sign': sign_names[sid_sign_idx], 
                'degrees': sid_degrees,
                'formatted': f"{sid_degrees:.2f}° {sign_names[sid_sign_idx]}"
            }
        
        # Generate HTML response
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Chart Results</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                .chart-section { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; }
                .planet-row { display: flex; justify-content: space-between; margin: 10px 0; }
                .planet-name { font-weight: bold; width: 100px; }
                .planet-pos { flex: 1; margin: 0 10px; }
                h1, h2 { color: #333; }
                .success { color: #28a745; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>🌟 Enhanced Precision Birth Chart</h1>
            
            <div class="chart-section">
                <h2>📍 Birth Information</h2>
                <p><strong>Date:</strong> {{ chart.birth_info.date }}</p>
                <p><strong>Time:</strong> {{ chart.birth_info.time }}</p>
                <p><strong>Location:</strong> {{ chart.birth_info.location }}</p>
                <p><strong>Coordinates:</strong> {{ chart.birth_info.coordinates }}</p>
                <p><strong>Ayanamsa:</strong> {{ chart.birth_info.ayanamsa_system }} ({{ chart.birth_info.ayanamsa_value }})</p>
                <p class="success">{{ chart.calculation_method }}</p>
            </div>
            
            <div class="chart-section">
                <h2>🪐 Planetary Positions Comparison</h2>
                <div style="display: flex; justify-content: space-between;">
                    <div style="flex: 1; margin-right: 20px;">
                        <h3>Tropical (Western)</h3>
                        {% for planet, data in chart.planets_tropical.items() %}
                        <div class="planet-row">
                            <span class="planet-name">{{ planet.title() }}:</span>
                            <span class="planet-pos">{{ data.formatted }}</span>
                        </div>
                        {% endfor %}
                    </div>
                    <div style="flex: 1; margin-left: 20px;">
                        <h3>Sidereal (Vedic)</h3>
                        {% for planet, data in chart.planets_sidereal.items() %}
                        <div class="planet-row">
                            <span class="planet-name">{{ planet.title() }}:</span>
                            <span class="planet-pos">{{ data.formatted }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            
            <p><a href="/test">← Test Enhanced Engine</a> | <a href="/">← Main Calculator</a></p>
        </body>
        </html>
        """, chart=enhanced_chart)
        
    except Exception as e:
        return f"<h1>Error in Enhanced Calculation</h1><p>{str(e)}</p><p><a href='/calculate-enhanced'>← Back</a></p>"

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
