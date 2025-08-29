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
    
    def get_ascendant(self, birth_datetime):
        """Calculate rising sign (simplified - assumes birth at equator)"""
        # This is a very simplified calculation
        # Real ascendant calculation requires birth location (lat/lon)
        hour = birth_datetime.hour + birth_datetime.minute / 60.0
        
        # Approximate rising sign based on birth time
        # Each sign rises for about 2 hours
        rising_index = int((hour * 30) // 60) % 12
        return f"{self.ZODIAC_SIGNS[rising_index]} (approximate)"
    
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
