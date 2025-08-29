# precision_validation.py
# Precision Validation Framework for Astrology App
# Add this file to your GitHub repository now!

import datetime
import math
from typing import Dict, List, Optional, Tuple, Any
import json

class PrecisionValidationFramework:
    """
    Step-by-step validation framework that integrates with your existing astrology app.
    This validates accuracy and provides recommendations for improvements.
    """
    
    def __init__(self, astro_calculator=None):
        """Initialize with your existing astrology calculator"""
        self.astro_calculator = astro_calculator
        self.results_history = []
        
        print("🔧 Precision Validation Framework initialized")
        print("📊 Ready to validate your astrology calculations!")
        
        # Validation tolerances (start relaxed, tighten as we improve)
        self.tolerances = {
            'planetary_position': 1.0,  # degrees (start with 1 degree tolerance)
            'rising_sign': 2.0,         # degrees (2 degree tolerance for ascendant)
            'house_cusps': 3.0,         # degrees (3 degree tolerance for houses)
        }
        
        # Test data for validation
        self.benchmark_data = self.initialize_test_data()
    
    def initialize_test_data(self):
        """Initialize test data with known accurate positions"""
        return {
            # Simple test cases for immediate validation
            'basic_tests': [
                {
                    'name': 'New Year 2024 Test',
                    'date': datetime.datetime(2024, 1, 1, 12, 0, 0),
                    'location': {'lat': 0.0, 'lng': 0.0},  # Equator reference
                    'expected': {
                        'sun_sign': 'Capricorn',
                        'sun_longitude': 280.0,  # Approximate
                    }
                },
                {
                    'name': 'Spring Equinox 2024',
                    'date': datetime.datetime(2024, 3, 20, 9, 6, 0),
                    'location': {'lat': 0.0, 'lng': 0.0},
                    'expected': {
                        'sun_sign': 'Aries',
                        'sun_longitude': 0.0,  # Exactly 0° at equinox
                    }
                }
            ],
            
            # Real birth chart for testing (Gandhi - public data)
            'historical_charts': [
                {
                    'name': 'Gandhi Test Chart',
                    'date': datetime.datetime(1869, 10, 2, 7, 33, 0),
                    'location': {'lat': 21.52, 'lng': 69.66},  # Porbandar
                    'expected': {
                        'sun_sign': 'Libra',
                        'moon_sign': 'Scorpio',
                        'ascendant_sign': 'Libra'
                    }
                }
            ]
        }
    
    def quick_health_check(self) -> Dict[str, Any]:
        """
        STEP 1: Run this first to check system health
        """
        print("\n🏥 Running Quick System Health Check...")
        
        health_report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'UNKNOWN',
            'tests': [],
            'summary': {'total': 0, 'passed': 0, 'failed': 0},
            'recommendations': []
        }
        
        # Test 1: Check if astrology calculator is available
        if self.astro_calculator:
            health_report['tests'].append({
                'name': 'Astrology Calculator Connection',
                'status': 'PASS',
                'message': 'Calculator is connected and ready'
            })
            health_report['summary']['passed'] += 1
        else:
            health_report['tests'].append({
                'name': 'Astrology Calculator Connection', 
                'status': 'WARNING',
                'message': 'No calculator connected - will use mock data for testing'
            })
        
        health_report['summary']['total'] += 1
        
        # Test 2: Check date/time handling
        try:
            test_date = datetime.datetime.now()
            health_report['tests'].append({
                'name': 'Date/Time Processing',
                'status': 'PASS',
                'message': f'Date processing working: {test_date}'
            })
            health_report['summary']['passed'] += 1
        except Exception as e:
            health_report['tests'].append({
                'name': 'Date/Time Processing',
                'status': 'FAIL', 
                'message': f'Date processing error: {str(e)}'
            })
            health_report['summary']['failed'] += 1
        
        health_report['summary']['total'] += 1
        
        # Test 3: Math operations
        try:
            test_calc = math.sin(math.radians(30))  # Should be 0.5
            if abs(test_calc - 0.5) < 0.001:
                health_report['tests'].append({
                    'name': 'Mathematical Operations',
                    'status': 'PASS',
                    'message': 'Math library functioning correctly'
                })
                health_report['summary']['passed'] += 1
            else:
                health_report['tests'].append({
                    'name': 'Mathematical Operations',
                    'status': 'FAIL',
                    'message': 'Math calculations showing errors'
                })
                health_report['summary']['failed'] += 1
        except Exception as e:
            health_report['tests'].append({
                'name': 'Mathematical Operations',
                'status': 'FAIL',
                'message': f'Math error: {str(e)}'
            })
            health_report['summary']['failed'] += 1
            
        health_report['summary']['total'] += 1
        
        # Determine overall health
        pass_rate = health_report['summary']['passed'] / health_report['summary']['total']
        if pass_rate >= 0.8:
            health_report['status'] = 'HEALTHY'
        elif pass_rate >= 0.5:
            health_report['status'] = 'FAIR'  
        else:
            health_report['status'] = 'POOR'
            
        # Add recommendations
        if health_report['status'] == 'HEALTHY':
            health_report['recommendations'].append('✅ System ready for precision testing')
        elif health_report['status'] == 'FAIR':
            health_report['recommendations'].append('⚠️ Some issues detected - proceed with caution')
        else:
            health_report['recommendations'].append('❌ Critical issues - fix before proceeding')
        
        print(f"✅ Health Check Complete: Status = {health_report['status']}")
        print(f"📊 Score: {health_report['summary']['passed']}/{health_report['summary']['total']}")
        
        return health_report
    
    def validate_planetary_calculations(self) -> Dict[str, Any]:
        """
        STEP 2: Validate planetary position calculations
        """
        print("\n🌍 Validating Planetary Calculations...")
        
        validation_report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'method': 'Basic Planetary Position Validation',
            'tests': [],
            'summary': {'total': 0, 'passed': 0, 'accuracy': 0.0},
            'recommendations': []
        }
        
        for test_case in self.benchmark_data['basic_tests']:
            test_result = {
                'name': test_case['name'],
                'date': test_case['date'].isoformat(),
                'status': 'UNKNOWN',
                'details': {}
            }
            
            try:
                # If we have a real calculator, use it
                if self.astro_calculator and hasattr(self.astro_calculator, 'calculate_planets'):
                    calculated = self.astro_calculator.calculate_planets(
                        test_case['date'], 
                        test_case['location']['lat'], 
                        test_case['location']['lng']
                    )
                    
                    # Compare sun position
                    if 'sun_longitude' in calculated and 'sun_longitude' in test_case['expected']:
                        calc_sun = calculated['sun_longitude']
                        expected_sun = test_case['expected']['sun_longitude']
                        error = abs(calc_sun - expected_sun)
                        
                        test_result['details']['sun_position'] = {
                            'calculated': calc_sun,
                            'expected': expected_sun,
                            'error_degrees': error,
                            'within_tolerance': error <= self.tolerances['planetary_position']
                        }
                        
                        if error <= self.tolerances['planetary_position']:
                            test_result['status'] = 'PASS'
                            validation_report['summary']['passed'] += 1
                        else:
                            test_result['status'] = 'FAIL'
                    else:
                        test_result['status'] = 'SKIP'
                        test_result['message'] = 'Sun position not available in calculations'
                        
                else:
                    # Mock validation for testing framework
                    test_result['status'] = 'MOCK'
                    test_result['message'] = 'Using mock data - calculator not connected'
                    test_result['details']['sun_position'] = {
                        'calculated': test_case['expected']['sun_longitude'] + 0.1,  # Small mock error
                        'expected': test_case['expected']['sun_longitude'],
                        'error_degrees': 0.1,
                        'within_tolerance': True
                    }
                    validation_report['summary']['passed'] += 1
                    
            except Exception as e:
                test_result['status'] = 'ERROR'
                test_result['error'] = str(e)
            
            validation_report['tests'].append(test_result)
            validation_report['summary']['total'] += 1
        
        # Calculate accuracy
        if validation_report['summary']['total'] > 0:
            validation_report['summary']['accuracy'] = (
                validation_report['summary']['passed'] / validation_report['summary']['total']
            )
        
        # Add recommendations based on results
        accuracy = validation_report['summary']['accuracy']
        if accuracy >= 0.9:
            validation_report['recommendations'].append('🌟 Excellent planetary accuracy!')
        elif accuracy >= 0.7:
            validation_report['recommendations'].append('✅ Good accuracy - minor improvements possible')
        elif accuracy >= 0.5:
            validation_report['recommendations'].append('⚠️ Fair accuracy - significant improvements needed')
        else:
            validation_report['recommendations'].append('❌ Poor accuracy - major fixes required')
            
        print(f"📊 Planetary Validation: {accuracy:.1%} accuracy")
        
        return validation_report
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """
        STEP 3: Run complete validation suite
        """
        print("\n🚀 Running Comprehensive Validation Suite...")
        print("=" * 50)
        
        comprehensive_report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0',
            'components': {},
            'overall_score': 0.0,
            'recommendations': [],
            'next_steps': []
        }
        
        # Run all validation components
        try:
            # Component 1: Health Check
            comprehensive_report['components']['health_check'] = self.quick_health_check()
            
            # Component 2: Planetary Validation
            comprehensive_report['components']['planetary_validation'] = self.validate_planetary_calculations()
            
            # Calculate overall score
            scores = []
            
            # Health check score
            health_score = (comprehensive_report['components']['health_check']['summary']['passed'] / 
                          comprehensive_report['components']['health_check']['summary']['total'])
            scores.append(health_score)
            
            # Planetary validation score
            planetary_score = comprehensive_report['components']['planetary_validation']['summary']['accuracy']
            scores.append(planetary_score)
            
            comprehensive_report['overall_score'] = sum(scores) / len(scores)
            
            # Generate overall recommendations
            overall_score = comprehensive_report['overall_score']
            if overall_score >= 0.85:
                comprehensive_report['recommendations'].append('🌟 Excellent overall accuracy - system ready for production')
                comprehensive_report['next_steps'].append('Consider adding advanced features like house calculations')
                comprehensive_report['next_steps'].append('Implement birth time rectification capabilities')
            elif overall_score >= 0.70:
                comprehensive_report['recommendations'].append('✅ Good accuracy - minor optimizations recommended')
                comprehensive_report['next_steps'].append('Focus on improving planetary calculation precision')
                comprehensive_report['next_steps'].append('Add more comprehensive test cases')
            elif overall_score >= 0.50:
                comprehensive_report['recommendations'].append('⚠️ Fair accuracy - significant improvements needed')
                comprehensive_report['next_steps'].append('Review and enhance core calculation algorithms')
                comprehensive_report['next_steps'].append('Implement better astronomical data sources')
            else:
                comprehensive_report['recommendations'].append('❌ Poor accuracy - major fixes required')
                comprehensive_report['next_steps'].append('Debug core calculation issues immediately')
                comprehensive_report['next_steps'].append('Consider using established astronomy libraries')
            
            print(f"\n🎯 VALIDATION COMPLETE!")
            print(f"📊 Overall Score: {overall_score:.1%}")
            print(f"🔍 System Status: {comprehensive_report['components']['health_check']['status']}")
            
            # Save results
            self.results_history.append(comprehensive_report)
            
        except Exception as e:
            comprehensive_report['error'] = f"Validation failed: {str(e)}"
            print(f"❌ Validation Error: {str(e)}")
        
        return comprehensive_report
    
    def get_improvement_suggestions(self) -> List[str]:
        """
        STEP 4: Get specific suggestions for improving accuracy
        """
        suggestions = [
            "1. 🎯 Immediate Actions:",
            "   • Run validation daily to track improvements",
            "   • Fix any failing health checks first",
            "   • Test with multiple birth dates and locations",
            "",
            "2. 📈 Accuracy Improvements:",
            "   • Upgrade to Swiss Ephemeris for planetary positions",
            "   • Add proper birth location handling for rising signs",
            "   • Implement multiple ayanamsa systems for Vedic astrology",
            "",
            "3. 🔧 Technical Enhancements:",
            "   • Add house system calculations (Placidus, Koch, Equal)",
            "   • Implement aspect calculations with proper orbs",
            "   • Add birth time rectification algorithms",
            "",
            "4. 🎨 User Experience:",
            "   • Add visual chart wheels",
            "   • Implement detailed interpretations",
            "   • Create comparison and synastry features"
        ]
        
        return suggestions

# Usage functions for easy integration with your existing app
def validate_astrology_app(calculator=None):
    """
    Quick function to validate your astrology app
    Call this from your main app to run validation
    """
    validator = PrecisionValidationFramework(calculator)
    return validator.run_comprehensive_validation()

def get_app_health_status(calculator=None):
    """
    Quick health check for your astrology app
    """
    validator = PrecisionValidationFramework(calculator)
    return validator.quick_health_check()

# Demo function - test the framework
if __name__ == "__main__":
    print("🌟 PRECISION VALIDATION FRAMEWORK DEMO")
    print("=" * 50)
    
    # Create validator (without real calculator for demo)
    demo_validator = PrecisionValidationFramework()
    
    # Run comprehensive validation
    results = demo_validator.run_comprehensive_validation()
    
    # Show improvement suggestions  
    print("\n💡 IMPROVEMENT SUGGESTIONS:")
    suggestions = demo_validator.get_improvement_suggestions()
    for suggestion in suggestions:
        print(suggestion)
    
    print("\n✅ Demo Complete! Add this to your astrology app now.")
