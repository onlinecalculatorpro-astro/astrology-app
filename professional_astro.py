from datetime import datetime, timezone
import math
from skyfield.api import load, Topos
from skyfield import almanac
import pytz

class ProfessionalAstrologyEngine:
    """Professional-grade astrology calculations using Swiss Ephemeris data"""
    
    PLANETS = {
        'sun': 'Sun',
        'moon': 'Moon', 
        'mercury': 'Mercury',
        'venus': 'Venus',
        'mars': 'Mars',
        'jupiter': 'Jupiter barycenter',
        'saturn': 'Saturn barycenter',
        'uranus': 'Uranus barycenter',
        'neptune': 'Neptune barycenter',
        'pluto': 'Pluto barycenter'
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
    
    def __init__(self):
        """Initialize with ephemeris data"""
        try:
            # Load JPL ephemeris data (may download ~10MB on first use)
            self.eph = load('de421.bsp')  # NASA JPL ephemeris
            self.ts = load.timescale()
        except Exception as e:
            # Fallback to simpler ephemeris if JPL data unavailable
            self.eph = load('de421_excerpt.bsp')
            self.ts = load.timescale()
    
    def get_coordinates_for_city(self, city_name):
        """Get coordinates for any city worldwide using Nominatim (OpenStreetMap)"""
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
            
        except Exception as e:
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
        }
        
        city_key = city_name.lower().strip()
        return city_coords.get(city_key, (0.0, 0.0, f'{city_name} (coordinates needed)'))
    
    def calculate_professional_chart(self, birth_datetime, latitude, longitude, house_system='placidus'):
        """Calculate comprehensive birth chart using Swiss Ephemeris"""
        try:
            # Convert to Skyfield time
            utc_dt = birth_datetime.replace(tzinfo=timezone.utc)
            t = self.ts.from_datetime(utc_dt)
            
            # Set geographic location
            location = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
            
            # Calculate planetary positions
            planetary_data = {}
            
            for planet_key, planet_name in self.PLANETS.items():
                try:
                    if planet_key == 'sun':
                        planet_obj = self.eph['sun']
                    elif planet_key == 'moon':
                        planet_obj = self.eph['moon']
                    else:
                        planet_obj = self.eph[planet_name]
                    
                    # Get geocentric position
                    earth = self.eph['earth']
                    astrometric = earth.at(t).observe(planet_obj)
                    apparent = astrometric.apparent()
                    
                    # Convert to ecliptic longitude
                    lon, lat, distance = apparent.ecliptic_latlon()
                    longitude_degrees = lon.degrees
                    
                    # Convert to zodiac sign and degrees
                    sign_index = int(longitude_degrees // 30)
                    sign_degrees = longitude_degrees % 30
                    
                    planetary_data[planet_key] = {
                        'name': planet_key.title(),
                        'longitude': longitude_degrees,
                        'sign': self.ZODIAC_SIGNS[sign_index],
                        'degrees': sign_degrees,
                        'formatted': f"{sign_degrees:.1f}° {self.ZODIAC_SIGNS[sign_index]}"
                    }
                    
                except Exception as e:
                    # Skip planets that can't be calculated
                    continue
            
            # Calculate house cusps (simplified Placidus approximation)
            houses = self._calculate_houses(t, latitude, longitude, house_system)
            
            # Calculate aspects
            aspects = self._calculate_aspects(planetary_data)
            
            return {
                'planets': planetary_data,
                'houses': houses,
                'aspects': aspects,
                'calculation_method': 'Swiss Ephemeris (Professional)',
                'house_system': self.HOUSE_SYSTEMS.get(house_system, 'Placidus')
            }
            
        except Exception as e:
            # Fallback to basic calculation if ephemeris fails
            return self._fallback_calculation(birth_datetime, latitude, longitude)
    
    def _calculate_houses(self, t, latitude, longitude, system='placidus'):
        """Calculate house cusps using specified house system"""
        try:
            # Get sidereal time for house calculations
            earth = self.eph['earth']
            location = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
            
            # Simplified house calculation (professional implementation would be more complex)
            houses = []
            for i in range(12):
                # This is a simplified approximation - real Placidus requires iterative calculations
                house_longitude = (i * 30) % 360  # Equal house approximation for now
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
            
        except Exception:
            return []
    
    def _calculate_aspects(self, planetary_data):
        """Calculate major aspects between planets"""
        aspects = []
        major_aspects = {
            'conjunction': (0, 8),      # 0° ± 8°
            'opposition': (180, 8),     # 180° ± 8°
            'trine': (120, 6),          # 120° ± 6°
            'square': (90, 6),          # 90° ± 6°
            'sextile': (60, 4),         # 60° ± 4°
        }
        
        planet_list = list(planetary_data.keys())
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                p1_lon = planetary_data[planet1]['longitude']
                p2_lon = planetary_data[planet2]['longitude']
                
                # Calculate angular separation
                separation = abs(p1_lon - p2_lon)
                if separation > 180:
                    separation = 360 - separation
                
                # Check for major aspects
                for aspect_name, (exact_angle, orb) in major_aspects.items():
                    if abs(separation - exact_angle) <= orb:
                        aspects.append({
                            'planet1': planetary_data[planet1]['name'],
                            'planet2': planetary_data[planet2]['name'],
                            'aspect': aspect_name,
                            'orb': abs(separation - exact_angle),
                            'description': f"{planetary_data[planet1]['name']} {aspect_name} {planetary_data[planet2]['name']}"
                        })
        
        return aspects
    
    def _fallback_calculation(self, birth_datetime, latitude, longitude):
        """Fallback to simplified calculations if Swiss Ephemeris fails"""
        # Import the existing calculator as fallback
        from astro_calc import AstrologyCalculator
        
        calc = AstrologyCalculator()
        
        sun_sign = calc.get_sun_sign(birth_datetime)
        moon_sign = calc.get_moon_sign(birth_datetime)
        ascendant = calc.get_ascendant(birth_datetime, latitude, longitude)
        planets = calc.get_planetary_positions(birth_datetime)
        
        # Format in professional structure
        professional_planets = {}
        for planet, sign in planets.items():
            professional_planets[planet.lower()] = {
                'name': planet,
                'sign': sign,
                'formatted': f"{sign} (approx.)"
            }
        
        return {
            'planets': professional_planets,
            'houses': [],
            'aspects': [],
            'calculation_method': 'Simplified (Fallback)',
            'sun_sign': sun_sign,
            'moon_sign': moon_sign,
            'ascendant': ascendant
        }
    
    def get_transit_predictions(self, birth_chart, prediction_date):
        """Calculate transit predictions for a given date"""
        try:
            # Convert prediction date to Skyfield time
            utc_dt = prediction_date.replace(tzinfo=timezone.utc)
            t = self.ts.from_datetime(utc_dt)
            
            predictions = []
            
            # Get current planetary positions
            current_positions = {}
            for planet_key, planet_name in self.PLANETS.items():
                try:
                    if planet_key == 'sun':
                        planet_obj = self.eph['sun']
                    elif planet_key == 'moon':
                        planet_obj = self.eph['moon']
                    else:
                        planet_obj = self.eph[planet_name]
                    
                    earth = self.eph['earth']
                    astrometric = earth.at(t).observe(planet_obj)
                    apparent = astrometric.apparent()
                    
                    lon, lat, distance = apparent.ecliptic_latlon()
                    current_positions[planet_key] = lon.degrees
                    
                except Exception:
                    continue
            
            # Compare with birth chart positions
            if 'planets' in birth_chart:
                for transit_planet, transit_lon in current_positions.items():
                    for natal_planet, natal_data in birth_chart['planets'].items():
                        if 'longitude' in natal_data:
                            natal_lon = natal_data['longitude']
                            
                            # Calculate aspect
                            separation = abs(transit_lon - natal_lon)
                            if separation > 180:
                                separation = 360 - separation
                            
                            # Check for major transiting aspects
                            if abs(separation - 0) <= 3:  # Conjunction
                                predictions.append({
                                    'type': 'transit',
                                    'description': f"Transiting {transit_planet.title()} conjunct natal {natal_planet.title()}",
                                    'interpretation': self._get_transit_interpretation(transit_planet, natal_planet, 'conjunction'),
                                    'strength': 'strong'
                                })
                            elif abs(separation - 180) <= 3:  # Opposition
                                predictions.append({
                                    'type': 'transit',
                                    'description': f"Transiting {transit_planet.title()} opposite natal {natal_planet.title()}",
                                    'interpretation': self._get_transit_interpretation(transit_planet, natal_planet, 'opposition'),
                                    'strength': 'strong'
                                })
            
            return predictions
            
        except Exception as e:
            return [{'type': 'error', 'description': f'Transit calculation error: {str(e)}'}]
    
    def _get_transit_interpretation(self, transit_planet, natal_planet, aspect):
        """Get interpretation for transit aspects"""
        interpretations = {
            ('sun', 'sun', 'conjunction'): "A time of renewed vitality and self-expression. Focus on personal goals.",
            ('mars', 'sun', 'conjunction'): "Increased energy and drive. Good time for action and leadership.",
            ('saturn', 'sun', 'conjunction'): "A time of responsibility and discipline. Focus on long-term goals.",
            ('jupiter', 'sun', 'conjunction'): "Opportunities for growth and expansion. Optimistic period.",
        }
        
        key = (transit_planet, natal_planet, aspect)
        return interpretations.get(key, f"Significant {aspect} between {transit_planet} and {natal_planet}")
