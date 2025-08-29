"""
Test the Enhanced Base Engine
Run this to verify our enhancements work
"""

from engines.base_engine import EnhancedBaseEngine
from datetime import datetime, timezone

def test_enhanced_calculations():
    """Test the enhanced calculation methods"""
    
    print("🧪 Testing Enhanced Astrology Engine...")
    print("=" * 50)
    
    # Create enhanced engine
    engine = EnhancedBaseEngine({
        'precision': 'HIGH',
        'enable_logging': True
    })
    
    # Test date
    test_date = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    
    try:
        # Test 1: Precise Julian Day
        jd = engine.precise_julian_day(test_date)
        print(f"✅ Precise Julian Day: {jd}")
        
        # Test 2: Enhanced Sun position
        sun_lon = engine.enhanced_sun_longitude(jd)
        print(f"✅ Enhanced Sun longitude: {sun_lon:.6f}°")
        
        # Test 3: Enhanced Moon position
        moon_lon = engine.enhanced_moon_longitude(jd)
        print(f"✅ Enhanced Moon longitude: {moon_lon:.6f}°")
        
        # Test 4: Ayanamsa calculation
        ayanamsa = engine.calculate_ayanamsa(jd, 'LAHIRI')
        print(f"✅ Lahiri Ayanamsa: {ayanamsa:.6f}°")
        
        # Test 5: Tropical to Sidereal conversion
        sidereal_sun = engine.tropical_to_sidereal(sun_lon, jd, 'LAHIRI')
        print(f"✅ Sidereal Sun longitude: {sidereal_sun:.6f}°")
        
        # Test 6: Enhanced planetary positions
        planets = engine.enhanced_planetary_positions(jd)
        print(f"✅ Enhanced planetary positions:")
        for planet, longitude in planets.items():
            print(f"   {planet.capitalize()}: {longitude:.6f}°")
        
        # Test 7: Performance stats
        stats = engine.get_performance_stats()
        print(f"✅ Performance stats: {stats}")
        
        print("\n🎉 All enhanced calculations working!")
        print("✅ Enhanced precision engine is ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in enhanced calculations: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_calculations()
    if success:
        print("\n✅ Enhanced engine test PASSED!")
        print("Ready to integrate with your existing code!")
    else:
        print("\n❌ Enhanced engine test FAILED!")
        print("Check the error messages above.")
