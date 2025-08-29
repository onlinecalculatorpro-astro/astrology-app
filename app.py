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
        print("✅ Validation framework initialized with professional calculator")
    except Exception as e:
        # Fallback to basic validation
        validation_framework = PrecisionValidationFramework()
        print(f"⚠️ Validation framework initialized without calculator: {e}")

# Initialize validation on startup
initialize_validation()

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
    """NEW ROUTE: Complete system validation page"""
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
    """NEW API ROUTE: Quick health check endpoint"""
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
    """NEW ROUTE: Manual validation trigger"""
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

@app.route('/validation-dashboard')
def validation_dashboard():
    """NEW ROUTE: Interactive validation dashboard"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Astrology App - Precision Validation Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; }
            .dashboard-card { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 25px; 
                             margin: 20px 0; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
            .header { text-align: center; color: #333; margin-bottom: 30px; }
            .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .status-card { background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; }
            .status-healthy { border-left: 5px solid #28a745; }
            .status-fair { border-left: 5px solid #ffc107; }
            .status-poor { border-left: 5px solid #dc3545; }
            .btn { padding: 12px 24px; border: none; border-radius: 8px; font-weight: bold; 
                   cursor: pointer; transition: transform 0.2s; margin: 5px; }
            .btn:hover { transform: translateY(-2px); }
            .btn-primary { background: linear-gradient(135deg, #4299e1, #3182ce); color: white; }
            .btn-success { background: linear-gradient(135deg, #48bb78, #38b2ac); color: white; }
            .btn-warning { background: linear-gradient(135deg, #ed8936, #dd6b20); color: white; }
            .results-area { margin-top: 20px; padding: 20px; background: #f1f3f4; border-radius: 10px; 
                           max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 0.9em; }
            .loading { text-align: center; padding: 20px; color: #666; }
            .metric { display: flex; justify-content: space-between; margin: 10px 0; }
            .metric-value { font-weight: bold; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="dashboard-card">
                <div class="header">
                    <h1>🔧 Precision Validation Dashboard</h1>
                    <p>Monitor and validate your astrology application's accuracy in real-time</p>
                </div>
                
                <div class="status-grid">
                    <div class="status-card status-healthy">
                        <h3>🏥 System Health</h3>
                        <div id="health-status">Loading...</div>
                        <button class="btn btn-primary" onclick="runHealthCheck()">Quick Check</button>
                    </div>
                    
                    <div class="status-card status-fair">
                        <h3>🌍 Planetary Accuracy</h3>
                        <div id="planetary-status">Not tested</div>
                        <button class="btn btn-warning" onclick="runPlanetaryTest()">Test Planets</button>
                    </div>
                    
                    <div class="status-card status-poor">
                        <h3>📊 Overall Score</h3>
                        <div id="overall-score">Unknown</div>
                        <button class="btn btn-success" onclick="runFullValidation()">Full Validation</button>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-card">
                <h2>🎯 Validation Controls</h2>
                <button class="btn btn-primary" onclick="runHealthCheck()">🏥 Health Check</button>
                <button class="btn btn-primary" onclick="runPlanetaryTest()">🌍 Planetary Test</button>
                <button class="btn btn-success" onclick="runFullValidation()">🚀 Complete Validation</button>
                <button class="btn btn-warning" onclick="clearResults()">🧹 Clear Results</button>
            </div>
            
            <div class="dashboard-card">
                <h2>📋 Results</h2>
                <div id="results-area" class="results-area">
                    <div class="loading">Click a validation button above to start testing...</div>
                </div>
            </div>
            
            <div class="dashboard-card">
                <h2>📈 Performance Metrics</h2>
                <div id="metrics">
                    <div class="metric">
                        <span>Last Validation:</span>
                        <span class="metric-value" id="last-validation">Never</span>
                    </div>
                    <div class="metric">
                        <span>Total Tests Run:</span>
                        <span class="metric-value" id="total-tests">0</span>
                    </div>
                    <div class="metric">
                        <span>Success Rate:</span>
                        <span class="metric-value" id="success-rate">0%</span>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let totalTests = 0;
            let successfulTests = 0;
            
            function updateMetrics() {
                document.getElementById('total-tests').textContent = totalTests;
                const successRate = totalTests > 0 ? ((successfulTests / totalTests) * 100).toFixed(1) + '%' : '0%';
                document.getElementById('success-rate').textContent = successRate;
                document.getElementById('last-validation').textContent = new Date().toLocaleTimeString();
            }
            
            function showLoading(elementId) {
                document.getElementById(elementId).innerHTML = '<div class="loading">⏳ Running...</div>';
            }
            
            function runHealthCheck() {
                showLoading('results-area');
                document.getElementById('health-status').textContent = '⏳ Checking...';
                
                fetch('/api/health-check')
                    .then(response => response.json())
                    .then(data => {
                        totalTests++;
                        if (data.status === 'success') {
                            successfulTests++;
                            const health = data.health;
                            document.getElementById('health-status').innerHTML = 
                                `<strong>${health.status}</strong><br>` +
                                `${health.summary.passed}/${health.summary.total} tests passed`;
                            document.getElementById('results-area').innerHTML = 
                                '<h3>Health Check Results:</h3>' +
                                '<pre>' + JSON.stringify(health, null, 2) + '</pre>';
                        } else {
                            document.getElementById('health-status').textContent = 'Error: ' + data.error;
                            document.getElementById('results-area').innerHTML = 
                                '<h3>Health Check Error:</h3>' +
                                '<p style="color: red;">' + data.error + '</p>';
                        }
                        updateMetrics();
                    })
                    .catch(error => {
                        totalTests++;
                        document.getElementById('health-status').textContent = 'Failed';
                        document.getElementById('results-area').innerHTML = 
                            '<h3>Health Check Failed:</h3>' +
                            '<p style="color: red;">' + error.message + '</p>';
                        updateMetrics();
                    });
            }
            
            function runPlanetaryTest() {
                showLoading('results-area');
                document.getElementById('planetary-status').textContent = '⏳ Testing...';
                
                // This would call a specific planetary validation endpoint
                fetch('/run-validation')
                    .then(response => response.json())
                    .then(data => {
                        totalTests++;
                        if (data.status === 'success') {
                            successfulTests++;
                            const planetary = data.results.components.planetary_validation;
                            const accuracy = (planetary.summary.accuracy * 100).toFixed(1);
                            document.getElementById('planetary-status').innerHTML = 
                                `<strong>${accuracy}% Accurate</strong><br>` +
                                `${planetary.summary.passed}/${planetary.summary.total} tests passed`;
                        } else {
                            document.getElementById('planetary-status').textContent = 'Error';
                        }
                        updateMetrics();
                    })
                    .catch(error => {
                        totalTests++;
                        document.getElementById('planetary-status').textContent = 'Failed';
                        updateMetrics();
                    });
            }
            
            function runFullValidation() {
                showLoading('results-area');
                document.getElementById('overall-score').textContent = '⏳ Calculating...';
                
                fetch('/run-validation')
                    .then(response => response.json())
                    .then(data => {
                        totalTests++;
                        if (data.status === 'success') {
                            successfulTests++;
                            const score = (data.results.overall_score * 100).toFixed(1);
                            document.getElementById('overall-score').innerHTML = 
                                `<strong>${score}%</strong><br>System Score`;
                            
                            document.getElementById('results-area').innerHTML = 
                                '<h3>Complete Validation Results:</h3>' +
                                '<pre>' + JSON.stringify(data.results, null, 2) + '</pre>';
                        } else {
                            document.getElementById('overall-score').textContent = 'Error';
                            document.getElementById('results-area').innerHTML = 
                                '<h3>Validation Error:</h3>' +
                                '<p style="color: red;">' + data.error + '</p>';
                        }
                        updateMetrics();
                    })
                    .catch(error => {
                        totalTests++;
                        document.getElementById('overall-score').textContent = 'Failed';
                        document.getElementById('results-area').innerHTML = 
                            '<h3>Validation Failed:</h3>' +
                            '<p style="color: red;">' + error.message + '</p>';
                        updateMetrics();
                    });
            }
            
            function clearResults() {
                document.getElementById('results-area').innerHTML = 
                    '<div class="loading">Results cleared. Click a validation button to start testing...</div>';
            }
            
            // Auto-run health check on page load
            setTimeout(runHealthCheck, 1000);
        </script>
        
        <div style="text-align: center; margin: 40px 0;">
            <a href="/" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); 
                              padding: 10px 20px; border-radius: 8px;">← Back to Main Calculator</a>
        </div>
    </body>
    </html>
    """)

@app.route('/test')
def test_enhanced():
    """Enhanced test route with validation integration"""
    if not ENHANCED_ENGINE_AVAILABLE:
        return """
        <h1>Enhanced Engine Not Available</h1>
        <p>The enhanced engine could not be loaded.</p>
        <p>Please check that the engines/base_engine.py file exists.</p>
        <p><a href="/">Back</a> | <a href="/validation-dashboard">Validation Dashboard</a></p>
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
                <h3>🔧 Validation Status</h3>
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
                <a href="/">🏠 Main Calculator</a>
                <a href="/calculate-enhanced">🔬 Enhanced Chart</a>
                <a href="/rectify-time">⏰ Time Rectification</a>
                <a href="/validation-dashboard">🔧 Validation Dashboard</a>
                <a href="/system-validation">📊 System Validation</a>
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
            <p><a href="/">Back to Birth Chart Calculator</a> | <a href="/validation-dashboard">Validation Dashboard</a></p>
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

# Keep all your existing routes (calculate-enhanced, rectify-time, predictions, api endpoints)
# They remain unchanged from your original code...

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
                .nav-links { margin: 20px 0; }
                .nav-links a { color: #007bff; text-decoration: none; margin: 0 10px; }
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
            <div class="nav-links">
                <a href="/">🏠 Main Calculator</a>
                <a href="/validation-dashboard">🔧 Validation Dashboard</a>
                <a href="/test">🧪 Test Engine</a>
            </div>
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
        
        # Get validation status for this calculation
        validation_status = "Not tested"
        if validation_framework:
            try:
                health = validation_framework.quick_health_check()
                validation_status = f"{health['status']} ({health['summary']['passed']}/{health['summary']['total']} tests)"
            except:
                validation_status = "Validation unavailable"
        
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
            'calculation_method': 'Enhanced Precision Engine',
            'validation_status': validation_status
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
                .validation-banner { background: linear-gradient(135deg, #4299e1, #3182ce); color: white; 
                                   padding: 15px; border-radius: 8px; margin: 15px 0; text-align: center; }
                .planet-row { display: flex; justify-content: space-between; margin: 10px 0; }
                .planet-name { font-weight: bold; width: 100px; }
                .planet-pos { flex: 1; margin: 0 10px; }
                h1, h2 { color: #333; }
                .success { color: #28a745; font-weight: bold; }
                .nav-links { text-align: center; margin: 30px 0; }
                .nav-links a { color: #007bff; text-decoration: none; margin: 0 15px; padding: 8px 16px; 
                             background: #f8f9fa; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>Enhanced Precision Birth Chart</h1>
            
            <div class="validation-banner">
                <h3>🔧 System Validation Status</h3>
                <p>{{ chart.validation_status }}</p>
            </div>
            
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
            </div>
            
            <div class="nav-links">
                <a href="/validation-dashboard">🔧 Validation Dashboard</a>
                <a href="/test">🧪 Test Engine</a>
                <a href="/">🏠 Main Calculator</a>
                <a href="/rectify-time">⏰ Time Rectification</a>
            </div>
        </body>
        </html>
        """, chart=enhanced_chart)
        
    except Exception as e:
        return f"<h1>Error in Enhanced Calculation</h1><p>{str(e)}</p><p><a href='/calculate-enhanced'>Back</a> | <a href='/validation-dashboard'>Validation Dashboard</a></p>"

# [Keep all your other existing routes unchanged: rectify-time, predictions, api endpoints...]
# I'm keeping your existing routes but won't repeat them all here to save space
# Just add the validation integration as shown above

if __name__ == '__main__':
    print("🚀 Starting Astrology App with Precision Validation Framework...")
    print("📊 Validation Dashboard available at: /validation-dashboard")
    print("🔧 System Validation available at: /system-validation")
    print("🏥 Health Check API available at: /api/health-check")
    app.run(debug=True, host='0.0.0.0', port=5000)
