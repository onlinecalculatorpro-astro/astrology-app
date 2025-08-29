"""
Enhanced Base Engine for Professional Astrology Calculations
This will enhance your existing AstrologyCalculator and ProfessionalAstrologyEngine
"""

import time
import math
from datetime import datetime, timezone
from typing import Dict, Any, Optional

class EnhancedBaseEngine:
    """Enhanced base class that your existing classes can inherit from"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = {
            'precision': 'HIGH',
            'enable_logging': True,
            'cache_enabled': True,
            'ayanamsa_system': 'LAHIRI',
            **(config or {})
        }
        
        # Initialize systems
        self.cache = {}
        self.performance_log = []
        self.start_time = time.time()
        
        self.log(f"Enhanced engine initialized - Precision: {self.config['precision']}")
    
    def log(self, message: str, level: str = 'INFO'):
        """Simple logging system"""
        if self.config['enable_logging']:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] [Enhanced] {message}")
    
    # Julian Day utilities with higher precision
    def precise_julian_day(self, dt):
        """More precise Julian Day calculation"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        elif dt.tzinfo != timezone.utc:
            dt = dt.astimezone(timezone.utc)
        
        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3
        
        jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        
        # More precise time fraction
        time_fraction = (dt.hour + dt.minute / 60.0 + dt.second / 3600.0 + dt.microsecond / 3600000000.0) / 24.0
        
        return jdn + time_fraction - 0.5
    
    # Enhanced Sun calculation with corrections
    def enhanced_sun_longitude(self, jd):
        """Enhanced sun longitude with higher accuracy"""
        T = (jd - 2451545.0) / 36525.0  # Centuries since J2000
        
        # Mean longitude of Sun
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T**2
        
        # Mean anomaly
        M = 357.52911 + 35999.05029 * T - 0.0001537 * T**2
        M_rad = math.radians(M)
        
        # Equation of center
        C = (1.914602 - 0.004817 * T - 0.000014 * T**2) * math.sin(M_rad) + \
            (0.019993 - 0.000101 * T) * math.sin(2 * M_rad) + \
            0.000289 * math.sin(3 * M_rad)
        
        # True longitude
        true_longitude = (L0 + C) % 360
        
        return true_longitude
    
    # Enhanced Moon calculation
    def enhanced_moon_longitude(self, jd):
        """Enhanced moon longitude calculation"""
        T = (jd - 2451545.0) / 36525.0
        
        # Moon's mean longitude
        L = 218.3164477 + 481267.88123421 * T - 0.0015786 * T**2
        
        # Moon's mean anomaly
        M = 134.9633964 + 477198.8675055 * T + 0.0087414 * T**2
        
        # Sun's mean anomaly
        M_sun = 357.5291092 + 35999.0502909 * T - 0.0001536 * T**2
        
        # Moon's argument of latitude
        F = 93.2720950 + 483202.0175233 * T - 0.0036539 * T**2
        
        # Convert to radians
        M_rad = math.radians(M)
        M_sun_rad = math.radians(M_sun)
        F_rad = math.radians(F)
        
        # Main corrections
        longitude = L + 6.288774 * math.sin(M_rad)
        longitude += 1.274027 * math.sin(2 * math.radians(L - M_sun) - M_rad)
        longitude += 0.658314 * math.sin(2 * math.radians(L - M_sun))
        longitude += 0.213618 * math.sin(2 * M_rad)
        
        return longitude % 360
    
    # Ayanamsa calculation (for Vedic astrology)
    def calculate_ayanamsa(self, jd, system='LAHIRI'):
        """Calculate ayanamsa for sidereal astrology"""
        # Years since J2000
        years_since_2000 = (jd - 2451545.0) / 365.25
        
        ayanamsa_values = {
            'LAHIRI': 23.85208333 + (50.290966 / 3600) * years_since_2000,
            'RAMAN': 21.94613889 + (50.290966 / 3600) * years_since_2000,
            'KP': 23.85208333 + (50.290966 / 3600) * years_since_2000,
        }
        
        return ayanamsa_values.get(system, ayanamsa_values['LAHIRI'])
    
    # Convert tropical to sidereal
    def tropical_to_sidereal(self, tropical_longitude, jd, ayanamsa_system='LAHIRI'):
        """Convert tropical longitude to sidereal"""
        ayanamsa = self.calculate_ayanamsa(jd, ayanamsa_system)
        sidereal = tropical_longitude - ayanamsa
        return sidereal % 360
    
    # Enhanced planetary positions
    def enhanced_planetary_positions(self, jd):
        """Calculate enhanced planetary positions"""
        T = (jd - 2451545.0) / 36525.0  # Centuries since J2000
        
        planets = {}
        
        # Mercury - enhanced calculation
        mercury_L = 252.250906 + 149474.0722491 * T + 0.00030397 * T**2
        mercury_a = 0.38709830
        mercury_e = 0.20563175 + 0.000020406 * T - 0.0000000284 * T**2
        mercury_M = 174.7948 + 149472.51529 * T + 0.00008444 * T**2
        mercury_longitude = self._calculate_planet_longitude(mercury_L, mercury_M, mercury_e)
        planets['mercury'] = mercury_longitude % 360
        
        # Venus - enhanced calculation  
        venus_L = 181.979801 + 58519.2130302 * T + 0.00031014 * T**2
        venus_M = 50.4161 + 58517.81539 * T + 0.00008567 * T**2
        venus_e = 0.00677188 - 0.000047766 * T + 0.0000000975 * T**2
        venus_longitude = self._calculate_planet_longitude(venus_L, venus_M, venus_e)
        planets['venus'] = venus_longitude % 360
        
        # Mars - enhanced calculation
        mars_L = 355.433275 + 19141.6964746 * T + 0.00031097 * T**2
        mars_M = 19.3730 + 19139.85475 * T + 0.00000181 * T**2  
        mars_e = 0.09340062 + 0.000090483 * T - 0.0000000806 * T**2
        mars_longitude = self._calculate_planet_longitude(mars_L, mars_M, mars_e)
        planets['mars'] = mars_longitude % 360
        
        # Jupiter - enhanced calculation
        jupiter_L = 34.351484 + 3036.3027748 * T + 0.00022330 * T**2
        jupiter_M = 20.0202 + 3034.90567 * T - 0.00000023 * T**2
        jupiter_e = 0.04849485 + 0.000163244 * T - 0.0000004719 * T**2
        jupiter_longitude = self._calculate_planet_longitude(jupiter_L, jupiter_M, jupiter_e)
        planets['jupiter'] = jupiter_longitude % 360
        
        # Saturn - enhanced calculation
        saturn_L = 50.077471 + 1223.5110686 * T + 0.00051952 * T**2
        saturn_M = 317.0207 + 1222.11494 * T + 0.00000611 * T**2
        saturn_e = 0.05554814 - 0.000346641 * T - 0.0000006436 * T**2
        saturn_longitude = self._calculate_planet_longitude(saturn_L, saturn_M, saturn_e)
        planets['saturn'] = saturn_longitude % 360
        
        return planets
    
    def _calculate_planet_longitude(self, mean_longitude, mean_anomaly, eccentricity):
        """Calculate planet longitude using mean anomaly and eccentricity"""
        M_rad = math.radians(mean_anomaly % 360)
        
        # Equation of center (simplified)
        C = (2 * eccentricity * math.sin(M_rad) + 
             1.25 * eccentricity**2 * math.sin(2 * M_rad))
        
        true_longitude = mean_longitude + math.degrees(C)
        return true_longitude
    
    # Performance monitoring
    def measure_performance(self, operation_name):
        """Simple performance measurement"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                
                self.performance_log.append({
                    'operation': operation_name,
                    'duration_ms': duration * 1000,
                    'timestamp': datetime.now().isoformat()
                })
                
                if duration > 0.1:  # Log slow operations
                    self.log(f"{operation_name} took {duration*1000:.1f}ms")
                
                return result
            return wrapper
        return decorator
    
    # Cache system
    def get_cached(self, key: str):
        """Get cached calculation result"""
        if not self.config['cache_enabled']:
            return None
            
        if key in self.cache:
            entry = self.cache[key]
            # Simple 5-minute cache TTL
            if time.time() - entry['timestamp'] < 300:
                return entry['value']
            else:
                del self.cache[key]
        return None
    
    def set_cached(self, key: str, value):
        """Store calculation result in cache"""
        if self.config['cache_enabled']:
            self.cache[key] = {
                'value': value,
                'timestamp': time.time()
            }
    
    # Statistics
    def get_performance_stats(self):
        """Get performance statistics"""
        if not self.performance_log:
            return "No performance data yet"
            
        avg_duration = sum(op['duration_ms'] for op in self.performance_log) / len(self.performance_log)
        total_operations = len(self.performance_log)
        
        return {
            'total_operations': total_operations,
            'average_duration_ms': round(avg_duration, 2),
            'cache_size': len(self.cache),
            'uptime_seconds': round(time.time() - self.start_time, 1)
        }
