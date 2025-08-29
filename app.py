from flask import Flask, render_template, request, jsonify, render_template_string
from datetime import datetime, timezone
import pytz
from professional_astro import ProfessionalAstrologyEngine

# Import precision validation framework
from precision_validation import PrecisionValidationFramework, validate_astrology_app, get_app_health_status

# Import our enhanced engine
try:
    from engines.base_engine import EnhancedBaseEngine
    ENHANCED_ENGINE_AVAILABLE = True
except ImportError:
    ENHANCED_ENGINE_AVAILABLE = False
    print("Enhanced engine not available - using standard calculations")

app = Flask(__name__)

# Initialize global validation framework
validation_framework = None

def initialize_validation():
    """Initialize validation framework on startup"""
    global validation_framework
    try:
        # Try to connect with professional calculator
        calc = ProfessionalAstrologyEngine()
        validation_framework = PrecisionValidationFramework(calc)
        print("Validation framework initialized with professional calculator")
    except Exception as e:
        # Fallback to basic validation
        validation_framework = PrecisionValidationFramework()
        print(f"Validation framework initialized without calculator: {e}")

# Initialize validation on startup
initialize_validation()

@app.route('/health', methods=['GET'])
def health():
    """Simple health endpoint for uptime pings"""
    try:
        stamp = datetime.utcnow().isoformat() + "Z"
        status = 'OK'
        if validation_framework:
            hc = validation_framework.quick_health_check()
            status = hc.get('status', 'OK')
        return jsonify(ok=True, status=status, ts=stamp), 200
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 200

@app.route('/')
def index():
    """Enhanced homepage with system health status"""
    try:
        # Get system health for display
        health_status = 'UNKNOWN'
        health_details = None
        
        if validation_framework:
            health_check = validation_framework.quick_health_check()
            health_status = health_check.get('status', 'UNKNOWN')
            health_details = health_check
        
        return render_template('index.html', 
                             system_health=health_status,
                             health_details=health_details)
        
    except Exception as e:
        print(f"Error getting health status: {e}")
        return render_template('index.html', 
                             system_health='UNKNOWN',
                             health_details=None)

@app.route('/system-validation')
def system_validation():
    """System validation page"""
    try:
        if not validation_framework:
            return render_template('validation_results.html',
                                 error="Validation framework not initialized",
                                 title="Validation Error")
        
        # Run comprehensive validation
        results = validation_framework.run_comprehensive_validation()
        
        return render_template('validation_results.html', 
                             validation_results=results,
                             title="System Validation Results")
        
    except Exception as e:
        return render_template('validation_results.html',
                             error=str(e),
                             title="Validation Error")

@app.route('/api/health-check')
def api_health_check():
    """Quick health check API endpoint"""
    try:
        if not validation_framework:
            return jsonify({
                'status': 'error',
                'error': 'Validation framework not available',
                'timestamp': datetime.now().isoformat()
            })
        
        # Get health status
        health = validation_framework.quick_health_check()
        return jsonify({
            'status': 'success',
            'health': health,
            'timestamp': health['timestamp']
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })

@app.route('/run-validation')
def run_validation():
    """Manual validation trigger"""
    try:
        if not validation_framework:
            return jsonify({
                'status': 'error',
                'error': 'Validation framework not available'
            })
        
        # Run validation
        results = validation_framework.run_comprehensive_validation()
        
        # Return JSON results for AJAX calls
        return jsonify({
            'status': 'success',
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'error': str(e)
        })

@app.route('/test')
def test_enhanced():
    """Enhanced test route with validation integration"""
    if not ENHANCED_ENGINE_AVAILABLE:
        return """
        <h1>Enhanced Engine Not Available</h1>
        <p>The enhanced engine could not be loaded.</p>
        <p>Please check that the engines/base_engine.py file exists.</p>
        <p><a href="/">Back</a></p>
        """
    
    try:
        engine = EnhancedBaseEngine({'precision': 'HIGH', 'enable_logging': True})
        test_date = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        
        jd = engine.precise_julian_day(test_date)
        sun_lon = engine.enhanced_sun_longitude(jd)
        moon_lon = engine.enhanced_moon_longitude(jd)
        ayanamsa = engine.calculate_ayanamsa(jd, 'LAHIRI')
        sidereal_sun = engine.tropical_to_sidereal(sun_lon, jd, 'LAHIRI')
        planets = engine.enhanced_planetary_positions(jd)
        stats = engine.get_performance_stats()
        
        # Run quick validation test
        validation_summary = "Not tested"
        if validation_framework:
            try:
                health = validation_framework.quick_health_check()
                validation_summary = f"System Health: {health['status']} ({health['summary']['passed']}/{health['summary']['total']} tests passed)"
            except Exception as e:
                validation_summary = f"Validation error: {str(e)}"
        
        results_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enhanced Engine Test Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                .success {{ color: green; }}
                .validation-status {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                .test-result {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .planet {{ margin: 5px 0; }}
                h1, h2, h3 {{ color: #333; }}
                a {{ color: #007bff; text-decoration: none; margin: 0 10px; }}
                a:hover {{ text-decoration: underline; }}
                .nav-links {{ text-align: center; margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <h1>Enhanced Astrology Engine Test Results</h1>
            
            <div class="validation-status">
                <h3>Validation Status</h3>
                <p>{validation_summary}</p>
            </div>
            
            <div class="test-result">
                <h3>Basic Calculations</h3>
                <p><strong>Test Date:</strong> {test_date.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p><strong>Precise Julian Day:</strong> {jd:.8f}</p>
            </div>
            
            <div class="test-result">
                <h3>Enhanced Astronomical Positions</h3>
                <p><strong>Enhanced Sun Longitude:</strong> {sun_lon:.6f}°</p>
                <p><strong>Enhanced Moon Longitude:</strong> {moon_lon:.6f}°</p>
                <p><strong>Lahiri Ayanamsa:</strong> {ayanamsa:.6f}°</p>
                <p><strong>Sidereal Sun Position:</strong> {sidereal_sun:.6f}°</p>
            </div>
            
            <div class="test-result">
                <h3>Enhanced Planetary Positions</h3>
        """
        
        sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        for planet, longitude in planets.items():
            sign_index = int(longitude // 30)
            sign_degrees = longitude % 30
            results_html += f"""
                <p class="planet"><strong>{planet.capitalize()}:</strong> 
                {longitude:.4f}° ({sign_degrees:.2f}° {sign_names[sign_index]})</p>
            """
        
        results_html += f"""
            </div>
            
            <div class="test-result">
                <h3>Performance Statistics</h3>
                <p>{stats}</p>
            </div>
            
            <div class="success">
                <h2>Enhanced Engine Working Successfully!</h2>
                <p>All precision calculations are functioning correctly.</p>
                <p>Ready to integrate with your birth chart calculator!</p>
            </div>
            
            <div class="nav-links">
                <h3>Navigation</h3>
                <a href="/">Main Calculator</a>
                <a href="/calculate-enhanced">Enhanced Chart</a>
                <a href="/rectify-time">Time Rectification</a>
                <a href="/system-validation">System Validation</a>
            </div>
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
            <h1>Enhanced Engine Test Failed</h1>
            <div class="error">
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Error Type:</strong> {type(e).__name__}</p>
            </div>
            <p><a href="/">Back to Birth Chart Calculator</a></p>
        </body>
        </html>
        """

@app.route('/calculate', methods=['POST'])
def calculate_chart():
    """Enhanced calculate route with validation tracking"""
    try:
        birth_date = request.form.get('birth_date')
        birth_time = request.form.get('birth_time')
        birth_city = request.form.get('birth_city', '').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        timezone_str = request.form.get('timezone', 'UTC')
        house_system = request.form.get('house_system', 'placidus')
        
        if not birth_date or not birth_time:
            raise ValueError("Birth date and time are required")
        
        if not birth_city and (not latitude or not longitude):
            raise ValueError("Birth location or coordinates are required")
        
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        calc = ProfessionalAstrologyEngine()
        
        if latitude and longitude:
            try:
                lat, lon = float(latitude), float(longitude)
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    raise ValueError("Invalid coordinates: Latitude must be -90 to 90, Longitude must be -180 to 180")
                location_name = f"{lat:.3f}°, {lon:.3f}°"
            except ValueError as e:
                raise ValueError(f"Invalid coordinates: {str(e)}")
        else:
            if len(birth_city) < 2:
                raise ValueError("Please enter a valid city name (at least 2 characters)")
            
            lat, lon, location_name = calc.get_coordinates_for_city(birth_city)
            
            if "coordinates needed" in location_name.lower():
                raise ValueError(f"Could not find coordinates for '{birth_city}'. Please try a different city name or use coordinates directly.")
        
        chart_data = calc.calculate_professional_chart(birth_datetime, lat, lon, house_system)
        
        chart_data.update({
            'birth_date': birth_date,
            'birth_time': birth_time,
            'birth_location': location_name,
            'coordinates': f"{lat:.4f}, {lon:.4f}",
            'timezone': timezone_str
        })
        
        if 'planets' in chart_data:
            chart_data['sun_sign'] = chart_data['planets'].get('sun', {}).get('sign', 'Unknown')
            chart_data['moon_sign'] = chart_data['planets'].get('moon', {}).get('sign', 'Unknown')
            
            if chart_data.get('houses'):
                chart_data['ascendant'] = chart_data['houses'][0].get('sign', 'Unknown')
            else:
                chart_data['ascendant'] = 'Calculating...'
        
        # Add validation status to results
        if validation_framework:
            try:
                health = validation_framework.quick_health_check()
                chart_data['system_validation'] = {
                    'status': health['status'],
                    'score': f"{health['summary']['passed']}/{health['summary']['total']}",
                    'timestamp': health['timestamp']
                }
            except:
                chart_data['system_validation'] = {'status': 'Unknown'}
        
        return render_template('professional_results.html', chart=chart_data)
        
    except ValueError as e:
        return render_template('error.html', error=str(e))
    except Exception as e:
        try:
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
                'calculation_method': 'Basic (Professional engine unavailable)',
                'system_validation': {'status': 'Basic mode - validation unavailable'}
            }
            
            return render_template('results.html', chart=chart_data)
            
        except Exception:
            error_msg = f"Calculation error: {str(e)}"
            return render_template('error.html', error=error_msg)

@app.route('/calculate-enhanced', methods=['GET', 'POST'])
def calculate_enhanced_chart():
    """Enhanced calculation endpoint using precision engine"""
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
            <h1>Enhanced Precision Chart Calculator</h1>
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
            <p><a href="/">Back to Standard Calculator</a></p>
        </body>
        </html>
        """
    
    if not ENHANCED_ENGINE_AVAILABLE:
        return "Enhanced engine not available. Please check the installation."
    
    try:
        birth_date = request.form.get('birth_date')
        birth_time = request.form.get('birth_time')
        birth_city = request.form.get('birth_city', '').strip()
        ayanamsa_system = request.form.get('ayanamsa', 'LAHIRI')
        
        birth_datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')
        
        from astro_calc import AstrologyCalculator
        basic_calc = AstrologyCalculator()
        lat, lon, location_name = basic_calc.get_coordinates_for_city(birth_city or "London")
        
        engine = EnhancedBaseEngine({'precision': 'HIGH'})
        jd = engine.precise_julian_day(birth_datetime.replace(tzinfo=timezone.utc))
        
        sun_tropical = engine.enhanced_sun_longitude(jd)
        moon_tropical = engine.enhanced_moon_longitude(jd)
        planets_tropical = engine.enhanced_planetary_positions(jd)
        planets_tropical['sun'] = sun_tropical
        planets_tropical['moon'] = moon_tropical
        
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
            
            trop_sign_idx = int(tropical_lon // 30)
            trop_degrees = tropical_lon % 30
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
            <h1>Enhanced Precision Birth Chart</h1>
            
            <div class="chart-section">
                <h2>Birth Information</h2>
                <p><strong>Date:</strong> {{ chart.birth_info.date }}</p>
                <p><strong>Time:</strong> {{ chart.birth_info.time }}</p>
                <p><strong>Location:</strong> {{ chart.birth_info.location }}</p>
                <p><strong>Coordinates:</strong> {{ chart.birth_info.coordinates }}</p>
                <p><strong>Ayanamsa:</strong> {{ chart.birth_info.ayanamsa_system }} ({{ chart.birth_info.ayanamsa_value }})</p>
                <p class="success">{{ chart.calculation_method }}</p>
            </div>
            
            <div class="chart-section">
                <h2>Planetary Positions Comparison</h2>
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
            </div ]
            
            <p><a href="/test">Test Enhanced Engine</a> | <a href="/">Main Calculator</a> | <a href="/rectify-time">Birth Time Rectification</a></p>
        </body>
        </html>
        """, chart=enhanced_chart)
        
    except Exception as e:
        return f"<h1>Error in Enhanced Calculation</h1><p>{str(e)}</p><p><a href='/calculate-enhanced'>Back</a></p>"

@app.route('/predictions', methods=['POST'])
def get_predictions():
    """Generate predictions based on transits - FIXED ROUTE"""
    try:
        chart_data = request.get_json()
        prediction_date_str = chart_data.get('prediction_date') if chart_data else None
        
        if not prediction_date_str:
            prediction_date = datetime.now()
        else:
            prediction_date = datetime.strptime(prediction_date_str, '%Y-%m-%d')
        
        calc = ProfessionalAstrologyEngine()
        birth_chart = chart_data.get('birth_chart', {}) if chart_data else {}
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
    """Enhanced API endpoint with professional features (accepts camelCase or snake_case)"""
    try:
        data = request.get_json(force=True, silent=True) or {}

        # Accept both naming styles
        birth_date = data.get('birth_date') or data.get('birthDate')
        birth_time = data.get('birth_time') or data.get('birthTime')
        house_system = data.get('house_system') or data.get('houseSystem') or 'placidus'
        timezone_str = data.get('timezone') or data.get('tz') or 'UTC'

        # Location: either coords or city name
        birth_city = (data.get('birth_city') or data.get('birthPlace') or '').strip()
        lat = data.get('latitude', data.get('lat', None))
        lon = data.get('longitude', data.get('lon', None))
        use_coords = data.get('useCoords', None)

        if not birth_date or not birth_time:
            return jsonify({'error': 'birth_date/birthDate and birth_time/birthTime are required'}), 400

        # Build datetime (expects 'YYYY-MM-DD' and 'HH:MM' or 'HH:MM:SS')
        bt = birth_time.strip()
        if len(bt) == 5:  # HH:MM
            fmt = '%Y-%m-%d %H:%M'
        else:            # HH:MM:SS
            fmt = '%Y-%m-%d %H:%M:%S'
        birth_datetime = datetime.strptime(f"{birth_date} {bt}", fmt)

        calc = ProfessionalAstrologyEngine()

        # Decide source of coordinates
        lat_val = None
        lon_val = None

        # If explicit coords requested OR present, use them
        if (use_coords is True) or (lat is not None and lon is not None):
            try:
                lat_val = float(lat)
                lon_val = float(lon)
                if not (-90.0 <= lat_val <= 90.0) or not (-180.0 <= lon_val <= 180.0):
                    return jsonify({'error': 'lat must be -90..90 and lon must be -180..180'}), 400
                location_name = f"{lat_val:.3f}°, {lon_val:.3f}°"
            except Exception as e:
                return jsonify({'error': f'invalid coordinates: {e}'}), 400
        else:
            # Otherwise resolve city name
            if not birth_city or len(birth_city) < 2:
                return jsonify({'error': 'Provide birthPlace/birth_city or lat+lon'}), 400
            lat_val, lon_val, location_name = calc.get_coordinates_for_city(birth_city)
            if isinstance(location_name, str) and 'coordinates needed' in location_name.lower():
                return jsonify({'error': f"Could not find coordinates for '{birth_city}'. Try another city or provide coordinates."}), 400

        # Do the professional calculation
        result = calc.calculate_professional_chart(birth_datetime, lat_val, lon_val, house_system)

        # Echo back some context (non-breaking)
        result.update({
            'birth_date': birth_date,
            'birth_time': birth_time,
            'birth_location': location_name,
            'coordinates': f"{lat_val:.4f}, {lon_val:.4f}",
            'timezone': timezone_str,
            'house_system': house_system
        })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ---------------------------------------------------------------------------
# NEW: Full Report API (JSON + prebuilt HTML sections for interpretation/predictions)
# ---------------------------------------------------------------------------
def _mk_interpretation_html(chart):
    sun  = chart.get('sun_sign', '—')
    moon = chart.get('moon_sign', '—')
    asc  = chart.get('ascendant', '—')

    # Optional aspect bullets (limit 3 to keep it short)
    aspects = chart.get('aspects') or []
    lines = []
    for a in aspects[:3]:
        p1 = (a.get('p1') or a.get('planet1') or 'Body1').title()
        p2 = (a.get('p2') or a.get('planet2') or 'Body2').title()
        typ = (a.get('aspect') or a.get('type') or 'Aspect').title()
        lines.append(f"<li>{p1} <strong>{typ}</strong> {p2}</li>")
    aspects_html = ("<ul>" + "\n".join(lines) + "</ul>") if lines else "<p>No major aspects detected.</p>"

    return f"""
    <h2>Professional Interpretation</h2>
    <p><strong>Your Sun in {sun}</strong> represents your core identity, vitality, and life purpose.</p>
    <p><strong>Your Moon in {moon}</strong> reflects your emotional nature, instincts, and inner needs.</p>
    <p><strong>Your Rising sign (Ascendant) in {asc}</strong> describes your persona and first impressions.</p>
    <h3>Key Aspect Patterns</h3>
    {aspects_html}
    """.strip()

def _mk_predictions_html(predictions, date_str):
    items = []
    for p in predictions or []:
        title = (p.get('title') or p.get('name') or 'Transit').title()
        desc  = p.get('description') or p.get('summary') or ''
        typ   = p.get('type') or ''
        strength = p.get('strength') or ''
        meta = " • ".join([x for x in [typ, strength] if x])
        meta_html = f"<div class='muted' style='opacity:.8'>{meta}</div>" if meta else ""
        items.append(f"""
        <div class="card" style="margin:10px 0;padding:12px;border-radius:10px;border:1px solid #eee">
          <div style="font-weight:700;margin-bottom:4px">{title}</div>
          {meta_html}
          <div>{desc}</div>
        </div>
        """)
    body = "".join(items) or "<p>No predictions available.</p>"
    return f"<h2>Current Predictions ({date_str})</h2>{body}"

@app.post('/api/report')
def api_full_report():
    """
    Return a single JSON with:
      - chart (same fields as /api/calculate)
      - interpretation_html (prebuilt)
      - predictions_html (prebuilt)
    Accepts camelCase or snake_case input keys.
    """
    try:
        data = request.get_json(force=True, silent=True) or {}

        # Inputs (both styles)
        birth_date   = data.get('birth_date') or data.get('birthDate')
        birth_time   = data.get('birth_time') or data.get('birthTime')
        house_system = data.get('house_system') or data.get('houseSystem') or 'placidus'
        timezone_str = data.get('timezone') or data.get('tz') or 'UTC'

        birth_city   = (data.get('birth_city') or data.get('birthPlace') or '').strip()
        lat          = data.get('latitude', data.get('lat', None))
        lon          = data.get('longitude', data.get('lon', None))
        use_coords   = data.get('useCoords', None)

        if not birth_date or not birth_time:
            return jsonify({'ok': False, 'error': 'birthDate/birth_date and birthTime/birth_time are required'}), 400

        bt = birth_time.strip()
        fmt = '%Y-%m-%d %H:%M' if len(bt) == 5 else '%Y-%m-%d %H:%M:%S'
        birth_dt = datetime.strptime(f"{birth_date} {bt}", fmt)

        calc = ProfessionalAstrologyEngine()

        # Coordinates resolution
        if (use_coords is True) or (lat is not None and lon is not None):
            lat_val = float(lat); lon_val = float(lon)
            if not (-90 <= lat_val <= 90) or not (-180 <= lon_val <= 180):
                return jsonify({'ok': False, 'error': 'lat must be -90..90 and lon must be -180..180'}), 400
            location_name = f"{lat_val:.4f}, {lon_val:.4f}"
        else:
            if not birth_city or len(birth_city) < 2:
                return jsonify({'ok': False, 'error': 'Provide birthPlace/birth_city or lat+lon'}), 400
            lat_val, lon_val, location_name = calc.get_coordinates_for_city(birth_city)

        # Core chart
        chart = calc.calculate_professional_chart(birth_dt, lat_val, lon_val, house_system)

        # Echo helpful context
        chart.update({
            'birth_date': birth_date,
            'birth_time': birth_time,
            'birth_location': location_name,
            'coordinates': f"{lat_val:.4f}, {lon_val:.4f}",
            'timezone': timezone_str,
            'house_system': house_system
        })

        # Ensure summary fields exist
        if 'planets' in chart:
            chart['sun_sign']  = chart['planets'].get('sun',  {}).get('sign',  chart.get('sun_sign',  'Unknown'))
            chart['moon_sign'] = chart['planets'].get('moon', {}).get('sign',  chart.get('moon_sign', 'Unknown'))
        if not chart.get('ascendant'):
            chart['ascendant'] = (chart.get('houses') or [{}])[0].get('sign', 'Unknown')

        # HTML sections
        interpretation_html = _mk_interpretation_html(chart)

        # Predictions
        prediction_date = datetime.now()
        predictions = calc.get_transit_predictions(chart, prediction_date)
        predictions_html = _mk_predictions_html(predictions, prediction_date.strftime('%Y-%m-%d'))

        return jsonify({
            'ok': True,
            'report': {
                'chart': chart,
                'interpretation_html': interpretation_html,
                'predictions_html': predictions_html
            }
        }), 200

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("Starting Astrology App with Precision Validation Framework...")
    print("System Validation available at: /system-validation")
    print("Health Check API available at: /api/health-check")
    app.run(debug=True, host='0.0.0.0', port=5000)
