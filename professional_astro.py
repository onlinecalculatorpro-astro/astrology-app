from datetime import datetime, timezone
import math

# Import our enhanced engine
try:
    from engines.base_engine import EnhancedBaseEngine
    ENHANCED_ENGINE_AVAILABLE = True
except ImportError:
    ENHANCED_ENGINE_AVAILABLE = False

class ProfessionalAstrologyEngine:
    """Professional-grade astrology calculations with enhanced precision"""
    
    PLANETS = {
        'sun': 'Sun',
        'moon': 'Moon', 
        'mercury': 'Mercury',
        'venus': 'Venus',
        'mars': 'Mars',
        'jupiter': 'Jupiter',
        'saturn': 'Saturn',
        'uranus': 'Uranus',
        'neptune': 'Neptune',
        'pluto': 'Pluto'
    }
    
    ZODIAC_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    HOUSE_SYSTEMS = {
        'placidus': 'Placidus',
        'koch': 'Koch',
        'equal': 'Equal House',
        'whole': 'Whole Sign'
    }
    
    def __init__(self, ayanamsa_system='LAHIRI'):
        """Initialize with enhanced precision engine"""
        self.ayanamsa_system = ayanamsa_system
        
        # Initialize enhanced engine if available
        if ENHANCED_ENGINE_AVAILABLE:
            self.enhanced_engine = EnhancedBaseEngine({
                'precision': 'HIGH',
                'enable_logging': False,  # Disable logging for production
                'ayanamsa_system': ayanamsa_system
            })
            self.precision_mode = 'ENHANCED'
        else:
            self.enhanced_engine = None
            self.precision_mode = 'STANDARD'
        
        # Keep existing ephemeris initialization for fallback
        self.eph = None
        self.ts = None
        self.ephemeris_available = False
        
        try:
            from skyfield.api import load
            self.ts = load.timescale()
            self.eph = load('de421_excerpt.bsp')
            self.ephemeris_available = True
        except Exception:
            self.ephemeris_available = False
    
    def get_coordinates_for_city(self, city_name):
        """Get coordinates for any city worldwide using Nominatim"""
        import requests
        
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': city_name,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'AstroApp-Professional/2.0 (astrology software)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    result = data[0]
                    lat = float(result['lat'])
                    lon = float(result['lon'])
                    
                    display_name = result.get('display_name', city_name)
                    location_parts = display_name.split(', ')[:3]
                    clean_name = ', '.join(location_parts)
                    
                    return (lat, lon, clean_name)
            
            return self._fallback_city_lookup(city_name)
            
        except Exception:
            return self._fallback_city_lookup(city_name)
    
    def _fallback_city_lookup(self, city_name):
        """Fallback to local city database"""
        city_coords = {
            'new york': (40.7128, -74.0060, 'New York, NY, USA'),
            'london': (51.5074, -0.1278, 'London, UK'),
            'paris': (48.8566, 2.3522, 'Paris, France'),
            'tokyo': (35.6762, 139.6503, 'Tokyo, Japan'),
            'mumbai': (19.0760, 72.8777, 'Mumbai, India'),
            'delhi': (28.7041, 77.1025, 'New Delhi, India'),
            'sydney': (-33.8688, 151.2093, 'Sydney, Australia'),
            'patna': (25.5941, 85.1376, 'Patna, Bihar, India'),
            'kolkata': (22.5726, 88.3639, 'Kolkata, West Bengal, India'),
        }
        
        city_key = city_name.lower().strip()
        return city_coords.get(city_key, (0.0, 0.0, f'{city_name} (coordinates needed)'))
    
    def calculate_professional_chart(self, birth_datetime, latitude, longitude, house_system='placidus'):
        """Calculate comprehensive birth chart with enhanced precision"""
        
        if self.precision_mode == 'ENHANCED':
            return self._enhanced_precision_calculation(birth_datetime, latitude, longitude, house_system)
        else:
            return self._standard_calculation(birth_datetime, latitude, longitude, house_system)
    
    def _enhanced_precision_calculation(self, birth_datetime, latitude, longitude, house_system):
        """Enhanced calculations using precision engine"""
        
        # Ensure datetime has timezone info
        if birth_datetime.tzinfo is None:
            birth_datetime = birth_datetime.replace(tzinfo=timezone.utc)
        
        # Calculate precise Julian Day
        jd = self.enhanced_engine.precise_julian_day(birth_datetime)
        
        # Get enhanced planetary positions (tropical)
        sun_tropical = self.enhanced_engine.enhanced_sun_longitude(jd)
        moon_tropical = self.enhanced_engine.enhanced_moon_longitude(jd)
        planets_tropical = self.enhanced_engine.enhanced_planetary_positions(jd)
        planets_tropical['sun'] = sun_tropical
        planets_tropical['moon'] = moon_tropical
        
        # Add outer planets with basic calculations for completeness
        planets_tropical.update({
            'uranus': self._calculate_planet_longitude(jd, 'uranus'),
            'neptune': self._calculate_planet_longitude(jd, 'neptune'),
            'pluto': self._calculate_planet_longitude(jd, 'pluto')
        })
        
        # Calculate ayanamsa and convert to sidereal
        ayanamsa_value = self.enhanced_engine.calculate_ayanamsa(jd, self.ayanamsa_system)
        
        # Convert tropical to sidereal positions
        enhanced_planets = {}
        for planet_key, tropical_lon in planets_tropical.items():
            sidereal_lon = self.enhanced_engine.tropical_to_sidereal(tropical_lon, jd, self.ayanamsa_system)
            
            sign_index = int(sidereal_lon // 30)
            sign_degrees = sidereal_lon % 30
            
            enhanced_planets[planet_key] = {
                'name': self.PLANETS.get(planet_key, planet_key.title()),
                'longitude': sidereal_lon,
                'tropical_longitude': tropical_lon,
                'sign': self.ZODIAC_SIGNS[sign_index],
                'degrees': sign_degrees,
                'formatted': f"{sign_degrees:.1f}° {self.ZODIAC_SIGNS[sign_index]}",
                'precision': 'enhanced'
            }
        
        # Calculate enhanced house cusps
        houses = self._calculate_enhanced_houses(birth_datetime, latitude, longitude, house_system, jd, ayanamsa_value)
        
        # Calculate aspects with higher precision
        aspects = self._calculate_precise_aspects(enhanced_planets)
        
        # Traditional compatibility fields
        sun_sign = enhanced_planets['sun']['sign']
        moon_sign = enhanced_planets['moon']['sign']
        ascendant_sign = houses[0]['sign'] if houses else 'Calculating...'
        
        return {
            'planets': enhanced_planets,
            'houses': houses,
            'aspects': aspects,
            'calculation_method': f'Enhanced Precision Engine (Sidereal/{self.ayanamsa_system})',
            'ayanamsa_system': self.ayanamsa_system,
            'ayanamsa_value': f"{ayanamsa_value:.6f}°",
            'house_system': self.HOUSE_SYSTEMS.get(house_system, 'Placidus'),
            'sun_sign': sun_sign,
            'moon_sign': moon_sign,
            'ascendant': ascendant_sign,
            'precision_mode': 'ENHANCED',
            'julian_day': jd
        }
    
    def _standard_calculation(self, birth_datetime, latitude, longitude, house_system):
        """Standard calculation fallback"""
        # Your existing enhanced fallback calculation
        from astro_calc import AstrologyCalculator
        calc = AstrologyCalculator()
        
        sun_sign = calc.get_sun_sign(birth_datetime)
        moon_sign = calc.get_moon_sign(birth_datetime)
        ascendant = calc.get_ascendant(birth_datetime, latitude, longitude)
        basic_planets = calc.get_planetary_positions(birth_datetime)
        
        # Enhanced planetary positions with degrees
        enhanced_planets = {}
        jd = calc.julian_day(birth_datetime)
        
        # Sun
        sun_lon = calc.sun_longitude(jd)
        sun_sign_index = int(sun_lon // 30)
        sun_degrees = sun_lon % 30
        enhanced_planets['sun'] = {
            'name': 'Sun',
            'longitude': sun_lon,
            'sign': self.ZODIAC_SIGNS[sun_sign_index],
            'degrees': sun_degrees,
            'formatted': f"{sun_degrees:.1f}° {self.ZODIAC_SIGNS[sun_sign_index]}",
            'precision': 'standard'
        }
        
        # Moon
        moon_lon = calc.moon_longitude(jd)
        moon_sign_index = int(moon_lon // 30)
        moon_degrees = moon_lon % 30
        enhanced_planets['moon'] = {
            'name': 'Moon',
            'longitude': moon_lon,
            'sign': self.ZODIAC_SIGNS[moon_sign_index],
            'degrees': moon_degrees,
            'formatted': f"{moon_degrees:.1f}° {self.ZODIAC_SIGNS[moon_sign_index]}",
            'precision': 'standard'
        }
        
        # Other planets
        for planet_name, sign in basic_planets.items():
            if planet_name.lower() not in ['sun', 'moon']:
                planet_lon = self._calculate_planet_longitude(jd, planet_name.lower())
                planet_sign_index = int(planet_lon // 30)
                planet_degrees = planet_lon % 30
                
                enhanced_planets[planet_name.lower()] = {
                    'name': planet_name,
                    'longitude': planet_lon,
                    'sign': self.ZODIAC_SIGNS[planet_sign_index],
                    'degrees': planet_degrees,
                    'formatted': f"{planet_degrees:.1f}° {self.ZODIAC_SIGNS[planet_sign_index]}",
                    'precision': 'standard'
                }
        
        houses = self._calculate_enhanced_houses(birth_datetime, latitude, longitude, house_system)
        aspects = self._calculate_aspects(enhanced_planets)
        
        return {
            'planets': enhanced_planets,
            'houses': houses,
            'aspects': aspects,
            'calculation_method': 'Standard Professional Engine',
            'house_system': self.HOUSE_SYSTEMS.get(house_system, 'Placidus'),
            'sun_sign': sun_sign,
            'moon_sign': moon_sign,
            'ascendant': ascendant,
            'precision_mode': 'STANDARD'
        }
    
    def _calculate_planet_longitude(self, jd, planet):
        """Calculate approximate planetary longitudes"""
        n = jd - 2451545.0
        
        planet_formulas = {
            'mercury': (252.25, 4.092317),
            'venus': (181.98, 1.602129),
            'mars': (355.43, 0.524071),
            'jupiter': (34.35, 0.083091),
            'saturn': (50.08, 0.033494),
            'uranus': (313.23, 0.011773),
            'neptune': (304.35, 0.006027),
            'pluto': (238.92, 0.003968)
        }
        
        if planet in planet_formulas:
            base, rate = planet_formulas[planet]
            return (base + rate * n) % 360
        return 0.0
    
    def _calculate_enhanced_houses(self, birth_datetime, latitude, longitude, system, jd=None, ayanamsa_value=None):
        """Calculate house cusps with enhanced precision"""
        houses = []
        
        # Use enhanced Julian Day if available, otherwise calculate
        if jd is None:
            from astro_calc import AstrologyCalculator
            calc = AstrologyCalculator()
            jd = calc.julian_day(birth_datetime)
        
        # Calculate Local Sidereal Time with higher precision
        T = (jd - 2451545.0) / 36525.0
        theta0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T**2 - T**3 / 38710000.0
        lst_degrees = (theta0 + longitude) % 360
        
        # Enhanced house calculation
        for i in range(12):
            if system == 'equal':
                house_longitude = (lst_degrees + i * 30) % 360
            elif system == 'whole':
                ascendant_sign = int(lst_degrees // 30)
                house_longitude = ((ascendant_sign + i) % 12) * 30
            else:  # Placidus approximation with latitude correction
                base_longitude = (i * 30 + lst_degrees) % 360
                lat_correction = math.sin(math.radians(latitude)) * 3 * math.cos(math.radians(base_longitude))
                house_longitude = (base_longitude + lat_correction) % 360
            
            # Apply ayanamsa correction if available (for sidereal houses)
            if ayanamsa_value is not None:
                house_longitude = (house_longitude - ayanamsa_value) % 360
            
            sign_index = int(house_longitude // 30)
            sign_degrees = house_longitude % 30
            
            houses.append({
                'house': i + 1,
                'longitude': house_longitude,
                'sign': self.ZODIAC_SIGNS[sign_index],
                'degrees': sign_degrees,
                'formatted': f"House {i + 1}: {sign_degrees:.1f}° {self.ZODIAC_SIGNS[sign_index]}"
            })
        
        return houses
    
    def _calculate_precise_aspects(self, planetary_data):
        """Calculate aspects with enhanced precision"""
        aspects = []
        major_aspects = {
            'conjunction': (0, 6),      # Tighter orbs for precision
            'opposition': (180, 6),     
            'trine': (120, 5),          
            'square': (90, 5),          
            'sextile': (60, 3),         
        }
        
        planet_list = list(planetary_data.keys())
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                if 'longitude' not in planetary_data[planet1] or 'longitude' not in planetary_data[planet2]:
                    continue
                
                p1_lon = planetary_data[planet1]['longitude']
                p2_lon = planetary_data[planet2]['longitude']
                
                # Calculate angular separation with higher precision
                separation = abs(p1_lon - p2_lon)
                if separation > 180:
                    separation = 360 - separation
                
                # Check for major aspects with tighter orbs
                for aspect_name, (exact_angle, orb) in major_aspects.items():
                    orb_difference = abs(separation - exact_angle)
                    if orb_difference <= orb:
                        strength = 'exact' if orb_difference < 1 else 'close' if orb_difference < 3 else 'wide'
                        
                        aspects.append({
                            'planet1': planetary_data[planet1]['name'],
                            'planet2': planetary_data[planet2]['name'],
                            'aspect': aspect_name,
                            'orb': orb_difference,
                            'strength': strength,
                            'description': f"{planetary_data[planet1]['name']} {aspect_name} {planetary_data[planet2]['name']}",
                            'precision': 'enhanced' if self.precision_mode == 'ENHANCED' else 'standard'
                        })
        
        return aspects
    
    def _calculate_aspects(self, planetary_data):
        """Standard aspect calculation for fallback"""
        aspects = []
        major_aspects = {
            'conjunction': (0, 8),      
            'opposition': (180, 8),     
            'trine': (120, 6),          
            'square': (90, 6),          
            'sextile': (60, 4),         
        }
        
        planet_list = list(planetary_data.keys())
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                if 'longitude' not in planetary_data[planet1] or 'longitude' not in planetary_data[planet2]:
                    continue
                
                p1_lon = planetary_data[planet1]['longitude']
                p2_lon = planetary_data[planet2]['longitude']
                
                separation = abs(p1_lon - p2_lon)
                if separation > 180:
                    separation = 360 - separation
                
                for aspect_name, (exact_angle, orb) in major_aspects.items():
                    if abs(separation - exact_angle) <= orb:
                        aspects.append({
                            'planet1': planetary_data[planet1]['name'],
                            'planet2': planetary_data[planet2]['name'],
                            'aspect': aspect_name,
                            'orb': abs(separation - exact_angle),
                            'description': f"{planetary_data[planet1]['name']} {aspect_name} {planetary_data[planet2]['name']}",
                            'precision': 'standard'
                        })
        
        return aspects
    
    def get_transit_predictions(self, birth_chart, prediction_date):
        """Generate enhanced transit predictions"""
        predictions = []
        
        try:
            if self.precision_mode == 'ENHANCED' and birth_chart.get('julian_day'):
                # Use enhanced engine for precise transits
                current_jd = self.enhanced_engine.precise_julian_day(prediction_date.replace(tzinfo=timezone.utc))
                
                # Calculate current planetary positions
                current_sun = self.enhanced_engine.enhanced_sun_longitude(current_jd)
                current_moon = self.enhanced_engine.enhanced_moon_longitude(current_jd)
                
                # Convert to sidereal
                current_sun_sidereal = self.enhanced_engine.tropical_to_sidereal(current_sun, current_jd, self.ayanamsa_system)
                current_moon_sidereal = self.enhanced_engine.tropical_to_sidereal(current_moon, current_jd, self.ayanamsa_system)
                
                sun_sign = self.ZODIAC_SIGNS[int(current_sun_sidereal // 30)]
                moon_sign = self.ZODIAC_SIGNS[int(current_moon_sidereal // 30)]
                
                predictions.append({
                    'type': 'solar',
                    'description': f"Enhanced Solar Transit in {sun_sign}",
                    'interpretation': f"The Sun's precise sidereal position in {sun_sign} brings focused energy to {sun_sign.lower()} themes.",
                    'strength': 'strong',
                    'precision': 'enhanced'
                })
                
                predictions.append({
                    'type': 'lunar', 
                    'description': f"Enhanced Lunar Transit in {moon_sign}",
                    'interpretation': f"The Moon's sidereal position in {moon_sign} influences emotional currents and intuitive insights.",
                    'strength': 'moderate',
                    'precision': 'enhanced'
                })
                
            else:
                # Fallback to standard calculations
                from astro_calc import AstrologyCalculator
                calc = AstrologyCalculator()
                
                current_sun_sign = calc.get_sun_sign(prediction_date)
                current_moon_sign = calc.get_moon_sign(prediction_date)
                
                predictions.append({
                    'type': 'solar',
                    'description': f"Current solar energy in {current_sun_sign}",
                    'interpretation': f"The Sun's current position in {current_sun_sign} emphasizes themes related to this sign.",
                    'strength': 'moderate',
                    'precision': 'standard'
                })
                
                predictions.append({
                    'type': 'lunar',
                    'description': f"Current lunar energy in {current_moon_sign}",
                    'interpretation': f"The Moon in {current_moon_sign} influences emotional currents and intuitive insights.",
                    'strength': 'moderate',
                    'precision': 'standard'
                })
            
        except Exception as e:
            predictions.append({
                'type': 'error',
                'description': f'Unable to calculate current predictions: {str(e)}',
                'precision': 'error'
            })
        
        return predictionsfrom datetime import datetime, timezone
import math

# Import our enhanced engine
try:
    from engines.base_engine import EnhancedBaseEngine
    ENHANCED_ENGINE_AVAILABLE = True
except ImportError:
    ENHANCED_ENGINE_AVAILABLE = False

class ProfessionalAstrologyEngine:
    """Professional-grade astrology calculations with enhanced precision"""
    
    PLANETS = {
        'sun': 'Sun',
        'moon': 'Moon', 
        'mercury': 'Mercury',
        'venus': 'Venus',
        'mars': 'Mars',
        'jupiter': 'Jupiter',
        'saturn': 'Saturn',
        'uranus': 'Uranus',
        'neptune': 'Neptune',
        'pluto': 'Pluto'
    }
    
    ZODIAC_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    HOUSE_SYSTEMS = {
        'placidus': 'Placidus',
        'koch': 'Koch',
        'equal': 'Equal House',
        'whole': 'Whole Sign'
    }
    
    def __init__(self, ayanamsa_system='LAHIRI'):
        """Initialize with enhanced precision engine"""
        self.ayanamsa_system = ayanamsa_system
        
        # Initialize enhanced engine if available
        if ENHANCED_ENGINE_AVAILABLE:
            self.enhanced_engine = EnhancedBaseEngine({
                'precision': 'HIGH',
                'enable_logging': False,  # Disable logging for production
                'ayanamsa_system': ayanamsa_system
            })
            self.precision_mode = 'ENHANCED'
        else:
            self.enhanced_engine = None
            self.precision_mode = 'STANDARD'
        
        # Keep existing ephemeris initialization for fallback
        self.eph = None
        self.ts = None
        self.ephemeris_available = False
        
        try:
            from skyfield.api import load
            self.ts = load.timescale()
            self.eph = load('de421_excerpt.bsp')
            self.ephemeris_available = True
        except Exception:
            self.ephemeris_available = False
    
    def get_coordinates_for_city(self, city_name):
        """Get coordinates for any city worldwide using Nominatim"""
        import requests
        
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': city_name,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'AstroApp-Professional/2.0 (astrology software)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    result = data[0]
                    lat = float(result['lat'])
                    lon = float(result['lon'])
                    
                    display_name = result.get('display_name', city_name)
                    location_parts = display_name.split(', ')[:3]
                    clean_name = ', '.join(location_parts)
                    
                    return (lat, lon, clean_name)
            
            return self._fallback_city_lookup(city_name)
            
        except Exception:
            return self._fallback_city_lookup(city_name)
    
    def _fallback_city_lookup(self, city_name):
        """Fallback to local city database"""
        city_coords = {
            'new york': (40.7128, -74.0060, 'New York, NY, USA'),
            'london': (51.5074, -0.1278, 'London, UK'),
            'paris': (48.8566, 2.3522, 'Paris, France'),
            'tokyo': (35.6762, 139.6503, 'Tokyo, Japan'),
            'mumbai': (19.0760, 72.8777, 'Mumbai, India'),
            'delhi': (28.7041, 77.1025, 'New Delhi, India'),
            'sydney': (-33.8688, 151.2093, 'Sydney, Australia'),
            'patna': (25.5941, 85.1376, 'Patna, Bihar, India'),
            'kolkata': (22.5726, 88.3639, 'Kolkata, West Bengal, India'),
        }
        
        city_key = city_name.lower().strip()
        return city_coords.get(city_key, (0.0, 0.0, f'{city_name} (coordinates needed)'))
    
    def calculate_professional_chart(self, birth_datetime, latitude, longitude, house_system='placidus'):
        """Calculate comprehensive birth chart with enhanced precision"""
        
        if self.precision_mode == 'ENHANCED':
            return self._enhanced_precision_calculation(birth_datetime, latitude, longitude, house_system)
        else:
            return self._standard_calculation(birth_datetime, latitude, longitude, house_system)
    
    def _enhanced_precision_calculation(self, birth_datetime, latitude, longitude, house_system):
        """Enhanced calculations using precision engine"""
        
        # Ensure datetime has timezone info
        if birth_datetime.tzinfo is None:
            birth_datetime = birth_datetime.replace(tzinfo=timezone.utc)
        
        # Calculate precise Julian Day
        jd = self.enhanced_engine.precise_julian_day(birth_datetime)
        
        # Get enhanced planetary positions (tropical)
        sun_tropical = self.enhanced_engine.enhanced_sun_longitude(jd)
        moon_tropical = self.enhanced_engine.enhanced_moon_longitude(jd)
        planets_tropical = self.enhanced_engine.enhanced_planetary_positions(jd)
        planets_tropical['sun'] = sun_tropical
        planets_tropical['moon'] = moon_tropical
        
        # Add outer planets with basic calculations for completeness
        planets_tropical.update({
            'uranus': self._calculate_planet_longitude(jd, 'uranus'),
            'neptune': self._calculate_planet_longitude(jd, 'neptune'),
            'pluto': self._calculate_planet_longitude(jd, 'pluto')
        })
        
        # Calculate ayanamsa and convert to sidereal
        ayanamsa_value = self.enhanced_engine.calculate_ayanamsa(jd, self.ayanamsa_system)
        
        # Convert tropical to sidereal positions
        enhanced_planets = {}
        for planet_key, tropical_lon in planets_tropical.items():
            sidereal_lon = self.enhanced_engine.tropical_to_sidereal(tropical_lon, jd, self.ayanamsa_system)
            
            sign_index = int(sidereal_lon // 30)
            sign_degrees = sidereal_lon % 30
            
            enhanced_planets[planet_key] = {
                'name': self.PLANETS.get(planet_key, planet_key.title()),
                'longitude': sidereal_lon,
                'tropical_longitude': tropical_lon,
                'sign': self.ZODIAC_SIGNS[sign_index],
                'degrees': sign_degrees,
                'formatted': f"{sign_degrees:.1f}° {self.ZODIAC_SIGNS[sign_index]}",
                'precision': 'enhanced'
            }
        
        # Calculate enhanced house cusps
        houses = self._calculate_enhanced_houses(birth_datetime, latitude, longitude, house_system, jd, ayanamsa_value)
        
        # Calculate aspects with higher precision
        aspects = self._calculate_precise_aspects(enhanced_planets)
        
        # Traditional compatibility fields
        sun_sign = enhanced_planets['sun']['sign']
        moon_sign = enhanced_planets['moon']['sign']
        ascendant_sign = houses[0]['sign'] if houses else 'Calculating...'
        
        return {
            'planets': enhanced_planets,
            'houses': houses,
            'aspects': aspects,
            'calculation_method': f'Enhanced Precision Engine (Sidereal/{self.ayanamsa_system})',
            'ayanamsa_system': self.ayanamsa_system,
            'ayanamsa_value': f"{ayanamsa_value:.6f}°",
            'house_system': self.HOUSE_SYSTEMS.get(house_system, 'Placidus'),
            'sun_sign': sun_sign,
            'moon_sign': moon_sign,
            'ascendant': ascendant_sign,
            'precision_mode': 'ENHANCED',
            'julian_day': jd
        }
    
    def _standard_calculation(self, birth_datetime, latitude, longitude, house_system):
        """Standard calculation fallback"""
        # Your existing enhanced fallback calculation
        from astro_calc import AstrologyCalculator
        calc = AstrologyCalculator()
        
        sun_sign = calc.get_sun_sign(birth_datetime)
        moon_sign = calc.get_moon_sign(birth_datetime)
        ascendant = calc.get_ascendant(birth_datetime, latitude, longitude)
        basic_planets = calc.get_planetary_positions(birth_datetime)
        
        # Enhanced planetary positions with degrees
        enhanced_planets = {}
        jd = calc.julian_day(birth_datetime)
        
        # Sun
        sun_lon = calc.sun_longitude(jd)
        sun_sign_index = int(sun_lon // 30)
        sun_degrees = sun_lon % 30
        enhanced_planets['sun'] = {
            'name': 'Sun',
            'longitude': sun_lon,
            'sign': self.ZODIAC_SIGNS[sun_sign_index],
            'degrees': sun_degrees,
            'formatted': f"{sun_degrees:.1f}° {self.ZODIAC_SIGNS[sun_sign_index]}",
            'precision': 'standard'
        }
        
        # Moon
        moon_lon = calc.moon_longitude(jd)
        moon_sign_index = int(moon_lon // 30)
        moon_degrees = moon_lon % 30
        enhanced_planets['moon'] = {
            'name': 'Moon',
            'longitude': moon_lon,
            'sign': self.ZODIAC_SIGNS[moon_sign_index],
            'degrees': moon_degrees,
            'formatted': f"{moon_degrees:.1f}° {self.ZODIAC_SIGNS[moon_sign_index]}",
            'precision': 'standard'
        }
        
        # Other planets
        for planet_name, sign in basic_planets.items():
            if planet_name.lower() not in ['sun', 'moon']:
                planet_lon = self._calculate_planet_longitude(jd, planet_name.lower())
                planet_sign_index = int(planet_lon // 30)
                planet_degrees = planet_lon % 30
                
                enhanced_planets[planet_name.lower()] = {
                    'name': planet_name,
                    'longitude': planet_lon,
                    'sign': self.ZODIAC_SIGNS[planet_sign_index],
                    'degrees': planet_degrees,
                    'formatted': f"{planet_degrees:.1f}° {self.ZODIAC_SIGNS[planet_sign_index]}",
                    'precision': 'standard'
                }
        
        houses = self._calculate_enhanced_houses(birth_datetime, latitude, longitude, house_system)
        aspects = self._calculate_aspects(enhanced_planets)
        
        return {
            'planets': enhanced_planets,
            'houses': houses,
            'aspects': aspects,
            'calculation_method': 'Standard Professional Engine',
            'house_system': self.HOUSE_SYSTEMS.get(house_system, 'Placidus'),
            'sun_sign': sun_sign,
            'moon_sign': moon_sign,
            'ascendant': ascendant,
            'precision_mode': 'STANDARD'
        }
    
    def _calculate_planet_longitude(self, jd, planet):
        """Calculate approximate planetary longitudes"""
        n = jd - 2451545.0
        
        planet_formulas = {
            'mercury': (252.25, 4.092317),
            'venus': (181.98, 1.602129),
            'mars': (355.43, 0.524071),
            'jupiter': (34.35, 0.083091),
            'saturn': (50.08, 0.033494),
            'uranus': (313.23, 0.011773),
            'neptune': (304.35, 0.006027),
            'pluto': (238.92, 0.003968)
        }
        
        if planet in planet_formulas:
            base, rate = planet_formulas[planet]
            return (base + rate * n) % 360
        return 0.0
    
    def _calculate_enhanced_houses(self, birth_datetime, latitude, longitude, system, jd=None, ayanamsa_value=None):
        """Calculate house cusps with enhanced precision"""
        houses = []
        
        # Use enhanced Julian Day if available, otherwise calculate
        if jd is None:
            from astro_calc import AstrologyCalculator
            calc = AstrologyCalculator()
            jd = calc.julian_day(birth_datetime)
        
        # Calculate Local Sidereal Time with higher precision
        T = (jd - 2451545.0) / 36525.0
        theta0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T**2 - T**3 / 38710000.0
        lst_degrees = (theta0 + longitude) % 360
        
        # Enhanced house calculation
        for i in range(12):
            if system == 'equal':
                house_longitude = (lst_degrees + i * 30) % 360
            elif system == 'whole':
                ascendant_sign = int(lst_degrees // 30)
                house_longitude = ((ascendant_sign + i) % 12) * 30
            else:  # Placidus approximation with latitude correction
                base_longitude = (i * 30 + lst_degrees) % 360
                lat_correction = math.sin(math.radians(latitude)) * 3 * math.cos(math.radians(base_longitude))
                house_longitude = (base_longitude + lat_correction) % 360
            
            # Apply ayanamsa correction if available (for sidereal houses)
            if ayanamsa_value is not None:
                house_longitude = (house_longitude - ayanamsa_value) % 360
            
            sign_index = int(house_longitude // 30)
            sign_degrees = house_longitude % 30
            
            houses.append({
                'house': i + 1,
                'longitude': house_longitude,
                'sign': self.ZODIAC_SIGNS[sign_index],
                'degrees': sign_degrees,
                'formatted': f"House {i + 1}: {sign_degrees:.1f}° {self.ZODIAC_SIGNS[sign_index]}"
            })
        
        return houses
    
    def _calculate_precise_aspects(self, planetary_data):
        """Calculate aspects with enhanced precision"""
        aspects = []
        major_aspects = {
            'conjunction': (0, 6),      # Tighter orbs for precision
            'opposition': (180, 6),     
            'trine': (120, 5),          
            'square': (90, 5),          
            'sextile': (60, 3),         
        }
        
        planet_list = list(planetary_data.keys())
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                if 'longitude' not in planetary_data[planet1] or 'longitude' not in planetary_data[planet2]:
                    continue
                
                p1_lon = planetary_data[planet1]['longitude']
                p2_lon = planetary_data[planet2]['longitude']
                
                # Calculate angular separation with higher precision
                separation = abs(p1_lon - p2_lon)
                if separation > 180:
                    separation = 360 - separation
                
                # Check for major aspects with tighter orbs
                for aspect_name, (exact_angle, orb) in major_aspects.items():
                    orb_difference = abs(separation - exact_angle)
                    if orb_difference <= orb:
                        strength = 'exact' if orb_difference < 1 else 'close' if orb_difference < 3 else 'wide'
                        
                        aspects.append({
                            'planet1': planetary_data[planet1]['name'],
                            'planet2': planetary_data[planet2]['name'],
                            'aspect': aspect_name,
                            'orb': orb_difference,
                            'strength': strength,
                            'description': f"{planetary_data[planet1]['name']} {aspect_name} {planetary_data[planet2]['name']}",
                            'precision': 'enhanced' if self.precision_mode == 'ENHANCED' else 'standard'
                        })
        
        return aspects
    
    def _calculate_aspects(self, planetary_data):
        """Standard aspect calculation for fallback"""
        aspects = []
        major_aspects = {
            'conjunction': (0, 8),      
            'opposition': (180, 8),     
            'trine': (120, 6),          
            'square': (90, 6),          
            'sextile': (60, 4),         
        }
        
        planet_list = list(planetary_data.keys())
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                if 'longitude' not in planetary_data[planet1] or 'longitude' not in planetary_data[planet2]:
                    continue
                
                p1_lon = planetary_data[planet1]['longitude']
                p2_lon = planetary_data[planet2]['longitude']
                
                separation = abs(p1_lon - p2_lon)
                if separation > 180:
                    separation = 360 - separation
                
                for aspect_name, (exact_angle, orb) in major_aspects.items():
                    if abs(separation - exact_angle) <= orb:
                        aspects.append({
                            'planet1': planetary_data[planet1]['name'],
                            'planet2': planetary_data[planet2]['name'],
                            'aspect': aspect_name,
                            'orb': abs(separation - exact_angle),
                            'description': f"{planetary_data[planet1]['name']} {aspect_name} {planetary_data[planet2]['name']}",
                            'precision': 'standard'
                        })
        
        return aspects
    
    def get_transit_predictions(self, birth_chart, prediction_date):
        """Generate enhanced transit predictions"""
        predictions = []
        
        try:
            if self.precision_mode == 'ENHANCED' and birth_chart.get('julian_day'):
                # Use enhanced engine for precise transits
                current_jd = self.enhanced_engine.precise_julian_day(prediction_date.replace(tzinfo=timezone.utc))
                
                # Calculate current planetary positions
                current_sun = self.enhanced_engine.enhanced_sun_longitude(current_jd)
                current_moon = self.enhanced_engine.enhanced_moon_longitude(current_jd)
                
                # Convert to sidereal
                current_sun_sidereal = self.enhanced_engine.tropical_to_sidereal(current_sun, current_jd, self.ayanamsa_system)
                current_moon_sidereal = self.enhanced_engine.tropical_to_sidereal(current_moon, current_jd, self.ayanamsa_system)
                
                sun_sign = self.ZODIAC_SIGNS[int(current_sun_sidereal // 30)]
                moon_sign = self.ZODIAC_SIGNS[int(current_moon_sidereal // 30)]
                
                predictions.append({
                    'type': 'solar',
                    'description': f"Enhanced Solar Transit in {sun_sign}",
                    'interpretation': f"The Sun's precise sidereal position in {sun_sign} brings focused energy to {sun_sign.lower()} themes.",
                    'strength': 'strong',
                    'precision': 'enhanced'
                })
                
                predictions.append({
                    'type': 'lunar', 
                    'description': f"Enhanced Lunar Transit in {moon_sign}",
                    'interpretation': f"The Moon's sidereal position in {moon_sign} influences emotional currents and intuitive insights.",
                    'strength': 'moderate',
                    'precision': 'enhanced'
                })
                
            else:
                # Fallback to standard calculations
                from astro_calc import AstrologyCalculator
                calc = AstrologyCalculator()
                
                current_sun_sign = calc.get_sun_sign(prediction_date)
                current_moon_sign = calc.get_moon_sign(prediction_date)
                
                predictions.append({
                    'type': 'solar',
                    'description': f"Current solar energy in {current_sun_sign}",
                    'interpretation': f"The Sun's current position in {current_sun_sign} emphasizes themes related to this sign.",
                    'strength': 'moderate',
                    'precision': 'standard'
                })
                
                predictions.append({
                    'type': 'lunar',
                    'description': f"Current lunar energy in {current_moon_sign}",
                    'interpretation': f"The Moon in {current_moon_sign} influences emotional currents and intuitive insights.",
                    'strength': 'moderate',
                    'precision': 'standard'
                })
            
        except Exception as e:
            predictions.append({
                'type': 'error',
                'description': f'Unable to calculate current predictions: {str(e)}',
                'precision': 'error'
            })
        
        return predictions
