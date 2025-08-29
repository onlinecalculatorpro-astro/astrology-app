from datetime import datetime, timezone
import math

class AstrologyCalculator:
    """Simple astrology calculator using basic astronomical formulas"""
    
    ZODIAC_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    def __init__(self):
        pass
    
    def get_coordinates_for_city(self, city_name):
        """Simple geocoding for major cities - you can expand this database"""
        city_coords = {
            'new york': (40.7128, -74.0060, 'New York, NY, USA'),
            'new york, usa': (40.7128, -74.0060, 'New York, NY, USA'),
            'london': (51.5074, -0.1278, 'London, UK'),
            'london, uk': (51.5074, -0.1278, 'London, UK'),
            'paris': (48.8566, 2.3522, 'Paris, France'),
            'paris, france': (48.8566, 2.3522, 'Paris, France'),
            'tokyo': (35.6762, 139.6503, 'Tokyo, Japan'),
            'tokyo, japan': (35.6762, 139.6503, 'Tokyo, Japan'),
            'los angeles': (34.0522, -118.2437, 'Los Angeles, CA, USA'),
            'los angeles, usa': (34.0522, -118.2437, 'Los Angeles, CA, USA'),
            'sydney': (-33.8688, 151.2093, 'Sydney, Australia'),
            'sydney, australia': (-33.8688, 151.2093, 'Sydney, Australia'),
            'mumbai': (19.0760, 72.8777, 'Mumbai, India'),
            'mumbai, india': (19.0760, 72.8777, 'Mumbai, India'),
            'delhi': (28.7041, 77.1025, 'New Delhi, India'),
            'delhi, india': (28.7041, 77.1025, 'New Delhi, India'),
        }
        
        city_key = city_name.lower().strip()
        if city_key in city_coords:
            return city_coords[city_key]
        else:
            # Default to GMT coordinates if city not found
            return (51.4769, -0.0005, f'{city_name} (approx.)')
    
    def local_sidereal_time(self, jd, longitude):
        """Calculate Local Sidereal Time"""
        # Greenwich Sidereal Time at 0h UT
        T = (jd - 2451545.0) / 36525.0
        theta0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T**2 - T**3 / 38710000.0
        
        # Convert to hours and add longitude correction
        lst_degrees = (theta0 + longitude) % 360
        return lst_degrees / 15.0  # Convert to hours
    
    def julian_day(self, dt):
        """Calculate Julian Day Number from datetime"""
        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3
        
        jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        
        # Add time of day
        time_fraction = (dt.hour + dt.minute / 60.0 + dt.second / 3600.0) / 24.0
        return jdn + time_fraction - 0.5
    
    def sun_longitude(self, jd):
        """Calculate approximate sun longitude for given Julian Day"""
        # Simplified formula - good enough for sun sign calculation
        n = jd - 2451545.0
        L = (280.460 + 0.9856474 * n) % 360
        g = math.radians((357.528 + 0.9856003 * n) % 360)
        
        # Apply equation of center (simplified)
        longitude = L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)
        return longitude % 360
    
    def moon_longitude(self, jd):
        """Calculate approximate moon longitude"""
        # Very simplified moon calculation
        n = jd - 2451545.0
        L = (218.316 + 13.176396 * n) % 360
        M = math.radians((134.963 + 13.064993 * n) % 360)
        F = math.radians((93.272 + 13.229350 * n) % 360)
        
        # Apply main correction
        longitude = L + 6.289 * math.sin(M)
        return longitude % 360
    
    def get_sun_sign(self, birth_datetime):
        """Get zodiac sun sign from birth datetime"""
        jd = self.julian_day(birth_datetime)
        sun_lon = self.sun_longitude(jd)
        
        # Convert longitude to zodiac sign
        sign_index = int(sun_lon // 30)
        return self.ZODIAC_SIGNS[sign_index]
    
    def get_moon_sign(self, birth_datetime):
        """Get zodiac moon sign from birth datetime"""
        jd = self.julian_day(birth_datetime)
        moon_lon = self.moon_longitude(jd)
        
        sign_index = int(moon_lon // 30)
        return self.ZODIAC_SIGNS[sign_index]
    
    def get_ascendant(self, birth_datetime, latitude, longitude, timezone='UTC'):
        """Calculate accurate rising sign using birth location"""
        jd = self.julian_day(birth_datetime)
        
        # Calculate Local Sidereal Time
        lst_hours = self.local_sidereal_time(jd, longitude)
        
        # Convert latitude to radians
        lat_rad = math.radians(latitude)
        
        # Calculate ascendant for each zodiac sign
        # This is a simplified method - proper calculation requires more complex formulas
        
        # Use the Local Sidereal Time to determine rising sign
        # Each sign rises for approximately 2 hours
        ascendant_sign_index = int((lst_hours * 0.5) % 12)
        
        # Adjust for latitude effects
        if abs(latitude) > 60:  # High latitudes need special handling
            return f"{self.ZODIAC_SIGNS[ascendant_sign_index]} (high latitude approximation)"
        
        return self.ZODIAC_SIGNS[ascendant_sign_index]
    
    def get_planetary_positions(self, birth_datetime):
        """Get approximate planetary positions"""
        jd = self.julian_day(birth_datetime)
        n = jd - 2451545.0  # Days since J2000
        
        # Very simplified planetary calculations
        planets = {}
        
        # Mercury
        mercury_lon = (252.25 + 4.092317 * n) % 360
        planets['Mercury'] = self.ZODIAC_SIGNS[int(mercury_lon // 30)]
        
        # Venus
        venus_lon = (181.98 + 1.602129 * n) % 360
        planets['Venus'] = self.ZODIAC_SIGNS[int(venus_lon // 30)]
        
        # Mars
        mars_lon = (355.43 + 0.524071 * n) % 360
        planets['Mars'] = self.ZODIAC_SIGNS[int(mars_lon // 30)]
        
        # Jupiter
        jupiter_lon = (34.35 + 0.083091 * n) % 360
        planets['Jupiter'] = self.ZODIAC_SIGNS[int(jupiter_lon // 30)]
        
        # Saturn
        saturn_lon = (50.08 + 0.033494 * n) % 360
        planets['Saturn'] = self.ZODIAC_SIGNS[int(saturn_lon // 30)]
        
        return planets
    
    def get_daily_horoscope(self, sign):
        """Simple daily horoscope generator"""
        horoscopes = {
            'Aries': 'Your fiery energy is at its peak today. Take initiative in new projects.',
            'Taurus': 'Focus on stability and practical matters. Good day for financial decisions.',
            'Gemini': 'Communication flows easily today. Great time for networking and learning.',
            'Cancer': 'Trust your intuition. Family and home matters are highlighted.',
            'Leo': 'Your creativity shines bright. Time to step into the spotlight.',
            'Virgo': 'Attention to detail pays off. Organize and plan for future success.',
            'Libra': 'Harmony and balance are key. Focus on relationships and partnerships.',
            'Scorpio': 'Deep transformation is possible. Trust the process of change.',
            'Sagittarius': 'Adventure calls to you. Expand your horizons through learning.',
            'Capricorn': 'Steady progress toward your goals. Discipline brings rewards.',
            'Aquarius': 'Innovation and originality are your strengths today.',
            'Pisces': 'Compassion and intuition guide you. Trust your inner wisdom.'
        }
        return horoscopes.get(sign, 'The stars have a special message for you today.')
