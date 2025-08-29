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
        
        # Get base chart data using your existing methods
        if self.precision_mode == 'ENHANCED':
            chart_data = self._enhanced_precision_calculation(birth_datetime, latitude, longitude, house_system)
        else:
            chart_data = self._standard_calculation(birth_datetime, latitude, longitude, house_system)
        
        # Add comprehensive interpretations
        chart_data['comprehensive_interpretations'] = self.generate_comprehensive_interpretation(chart_data)
        
        return chart_data
    
    # ========== COMPREHENSIVE INTERPRETATION SYSTEM ==========
    
    def generate_comprehensive_interpretation(self, chart_data):
        """Generate detailed interpretations across all major life aspects"""
        
        interpretations = {
            'personality_core': self.interpret_personality_core(chart_data),
            'career_profession': self.interpret_career_profession(chart_data),
            'relationships_love': self.interpret_relationships_love(chart_data),
            'health_vitality': self.interpret_health_vitality(chart_data),
            'finances_wealth': self.interpret_finances_wealth(chart_data),
            'family_children': self.interpret_family_children(chart_data),
            'spiritual_growth': self.interpret_spiritual_growth(chart_data),
            'communication_learning': self.interpret_communication_learning(chart_data),
            'travel_adventure': self.interpret_travel_adventure(chart_data),
            'challenges_lessons': self.interpret_challenges_lessons(chart_data)
        }
        
        return interpretations
    
    def interpret_personality_core(self, chart_data):
        """Comprehensive personality analysis"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        moon_sign = chart_data.get('moon_sign', 'Cancer')
        rising_sign = chart_data.get('ascendant', 'Leo')
        
        sun_descriptions = {
            'Aries': "You possess a pioneering spirit that naturally drives you to lead and initiate new ventures. Your confidence and courage inspire others to follow your vision, though practicing patience when others don't match your energetic pace enhances your leadership effectiveness.",
            'Taurus': "You bring remarkable stability and practical wisdom to every situation. Your persistence and reliability make you someone others truly depend on, though developing flexibility helps you adapt gracefully when circumstances require change.",
            'Gemini': "Your quick wit and insatiable curiosity make you an excellent communicator and natural networker. You thrive on mental stimulation and variety, though focusing on depth rather than breadth can deepen your impact.",
            'Cancer': "Your intuitive nature and emotional intelligence help you nurture others with remarkable sensitivity. You create safe spaces where people can heal and grow, though healthy boundaries protect your energy.",
            'Leo': "Your natural charisma and creative spirit light up any room. You inspire through authentic self-expression and generous leadership, though sharing the spotlight enhances your own radiance.",
            'Virgo': "Your attention to detail and desire to serve creates meaningful improvements everywhere you go. Your analytical mind solves complex problems, though self-compassion balances perfectionism.",
            'Libra': "Your diplomatic nature brings harmony to relationships and beauty to environments. You excel at seeing multiple perspectives, though trusting your own judgment strengthens decision-making.",
            'Scorpio': "Your emotional depth and transformative power help others heal profoundly. You see beneath surfaces to essential truths, though vulnerability deepens your connections.",
            'Sagittarius': "Your philosophical nature and love of adventure expands minds and opens possibilities. You inspire others to think bigger, though grounding visions makes them reality.",
            'Capricorn': "Your discipline and long-term vision create lasting achievements. You build things that endure through challenge, though celebrating progress sustains motivation.",
            'Aquarius': "Your innovative thinking and humanitarian spirit advance society toward a better future. You see possibilities others miss, though emotional connection strengthens impact.",
            'Pisces': "Your compassion and imagination heal and inspire everyone you encounter. You understand life's deeper meanings, though healthy boundaries preserve your sensitive energy."
        }
        
        return {
            'title': 'Your Core Personality & Life Purpose',
            'sections': {
                'essential_self': {
                    'heading': f'Your Sun in {sun_sign} - Your Essential Nature',
                    'content': sun_descriptions.get(sun_sign, f"Your {sun_sign} nature brings unique gifts to the world.")
                },
                'emotional_world': {
                    'heading': f'Your Moon in {moon_sign} - Your Emotional Nature',
                    'content': f"Your {moon_sign} Moon reveals your deepest emotional needs and instinctive responses. This placement shows how you process feelings and what makes you feel truly secure and nurtured."
                },
                'outer_expression': {
                    'heading': f'Your {rising_sign} Rising - How Others See You',
                    'content': f"Your {rising_sign} Ascendant shapes the first impression you make and your approach to new situations. This is your natural style of engaging with the world."
                }
            }
        }
    
    def interpret_career_profession(self, chart_data):
        """Comprehensive career guidance"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        
        career_paths = {
            'Aries': "Your natural leadership and pioneering spirit excel in entrepreneurship, emergency services, competitive sports, or any field where you can be first to market. You thrive when taking charge of challenging projects and inspiring teams through decisive action.",
            'Taurus': "Your patience and eye for quality suit careers in finance, real estate, agriculture, luxury goods, or artisanal crafts. You excel at building lasting value and creating systems others depend on for security.",
            'Gemini': "Your communication skills and versatility shine in media, education, sales, technology, or journalism. You excel at connecting people and ideas, making complex information accessible.",
            'Cancer': "Your nurturing abilities make you exceptional in healthcare, hospitality, real estate, counseling, or childcare. You create environments where others feel safe and supported.",
            'Leo': "Your creativity and natural charisma suit entertainment, education, luxury retail, management, or any role where you can inspire and showcase talent.",
            'Virgo': "Your analytical skills excel in healthcare, research, quality control, editing, or technical fields. You improve systems and solve problems with methodical precision.",
            'Libra': "Your diplomatic skills suit law, counseling, design, mediation, or partnership-based businesses. You create harmony and find solutions that benefit everyone.",
            'Scorpio': "Your investigative nature suits psychology, research, finance, healing arts, or transformation-focused careers. You help others navigate profound changes.",
            'Sagittarius': "Your love of learning suits education, travel, publishing, law, or international business. You expand others' horizons through teaching and cultural exchange.",
            'Capricorn': "Your discipline and ambition suit business leadership, government, engineering, or traditional professional fields. You build lasting institutions.",
            'Aquarius': "Your innovative thinking suits technology, humanitarian work, research, or progressive causes. You advance society through breakthrough ideas.",
            'Pisces': "Your creativity and compassion suit arts, healing professions, spirituality, or charitable work. You bring inspiration and emotional healing to your work."
        }
        
        return {
            'title': 'Career & Professional Success',
            'sections': {
                'career_path': {
                    'heading': f'Professional Direction for {sun_sign}',
                    'content': career_paths.get(sun_sign, f"Your {sun_sign} nature offers unique professional opportunities.")
                }
            }
        }
    
    def interpret_relationships_love(self, chart_data):
        """Comprehensive relationship insights"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        moon_sign = chart_data.get('moon_sign', 'Cancer')
        
        love_styles = {
            'Aries': "In love, you bring passion, excitement, and unwavering loyalty. You love with your whole heart and appreciate partners who can match your enthusiasm for life while respecting your need for independence.",
            'Taurus': "You offer steady, devoted love and create beautiful, comfortable shared spaces. You show love through practical actions and prefer stable, long-term commitments over casual dating.",
            'Gemini': "You bring playfulness and intellectual stimulation to relationships. You need mental connection as much as emotional intimacy and appreciate partners who engage with your ideas.",
            'Cancer': "You nurture your loved ones with deep emotional care and intuitive understanding. You create a sense of home and family wherever you are, offering emotional security.",
            'Leo': "You bring warmth, generosity, and romantic flair to relationships. You love to celebrate your partner and create memorable experiences together.",
            'Virgo': "You show love through thoughtful actions and genuine care for your partner's wellbeing. You pay attention to details that matter and work to improve relationships.",
            'Libra': "You bring harmony, romance, and diplomatic grace to partnerships. You naturally seek balance and work to create relationships where both feel valued.",
            'Scorpio': "You offer intense, transformative love that goes beyond surface attraction. You seek deep emotional connection and are fiercely loyal once committed.",
            'Sagittarius': "You bring adventure, optimism, and philosophical depth to relationships. You need freedom to explore within partnership and inspire growth.",
            'Capricorn': "You build relationships with care and long-term vision. You show love through commitment and working toward shared goals.",
            'Aquarius': "You bring unique perspectives and humanitarian values to relationships. You need intellectual connection and appreciate partners who share your ideals.",
            'Pisces': "You love with boundless compassion and intuitive understanding. You bring creativity, spirituality, and emotional healing to relationships."
        }
        
        return {
            'title': 'Love & Relationships',
            'sections': {
                'love_nature': {
                    'heading': f'Your {sun_sign} Love Style',
                    'content': love_styles.get(sun_sign, f"Your {sun_sign} nature brings unique gifts to relationships.")
                },
                'emotional_needs': {
                    'heading': f'Emotional Needs ({moon_sign} Moon)',
                    'content': f"With your Moon in {moon_sign}, you feel most loved when your deep emotional needs for security, understanding, and connection are honored in relationships."
                }
            }
        }
    
    def interpret_health_vitality(self, chart_data):
        """Health and wellness guidance"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        
        health_approaches = {
            'Aries': "Your dynamic energy needs regular physical outlets. High-intensity exercise, competitive sports, or martial arts help you release stress. Pay attention to head-related issues and manage stress levels.",
            'Taurus': "Your steady constitution benefits from consistent, moderate exercise and attention to nutrition. Walking, yoga, or gardening suit your nature. Watch throat and weight-related concerns.",
            'Gemini': "Your active mind needs variety in fitness routines. Team sports, dance, or activities combining learning with movement work well. Pay attention to nervous system and respiratory health.",
            'Cancer': "Your sensitive system benefits from gentle, nurturing approaches. Swimming, walking, or home-based routines suit you. Watch digestive and emotional eating patterns.",
            'Leo': "Your vital energy shines when you enjoy your fitness routine. Dance, performance-based fitness, or heart-healthy activities align with your nature.",
            'Virgo': "Your methodical approach serves you well with detailed wellness routines. Precise programs and nutrition tracking suit your systematic nature.",
            'Libra': "Your love of beauty draws you to aesthetically pleasing fitness activities. Partner workouts or activities in beautiful settings motivate you.",
            'Scorpio': "Your intense nature benefits from transformative, challenging routines. Intense training or healing arts suit your depth.",
            'Sagittarius': "Your adventurous spirit thrives with outdoor activities and varied fitness experiences. Hiking or adventure sports motivate you.",
            'Capricorn': "Your disciplined approach creates lasting wellness habits through consistent, goal-oriented routines. Structured programs suit your determination.",
            'Aquarius': "Your innovative nature enjoys unique, technology-enhanced, or group fitness activities. Progressive approaches appeal to you.",
            'Pisces': "Your sensitive system responds well to gentle, flowing movement and water-based activities. Swimming, yoga, or tai chi suit your nature."
        }
        
        return {
            'title': 'Health & Vitality',
            'sections': {
                'wellness_approach': {
                    'heading': f'Health Approach for {sun_sign}',
                    'content': health_approaches.get(sun_sign, f"Your {sun_sign} nature benefits from wellness approaches that align with your natural energy.")
                }
            }
        }
    
    def interpret_finances_wealth(self, chart_data):
        """Financial guidance and wealth building"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        
        financial_styles = {
            'Aries': "Your entrepreneurial spirit and calculated risk-taking can lead to significant gains. You spot opportunities quickly, though patience with long-term investments balances impulsive tendencies.",
            'Taurus': "Your natural financial instincts and patience make you excellent at building substantial wealth over time. You appreciate quality investments and tangible assets.",
            'Gemini': "Your versatility creates opportunities for diverse income sources. You excel at finding profitable information, though focusing on fewer investments may yield better returns.",
            'Cancer': "Your intuitive approach and focus on security lead to emotionally satisfying financial choices. You excel at saving for family needs and long-term security.",
            'Leo': "Your confidence can attract wealth through creative ventures and high-visibility opportunities. Balance generous spending with consistent saving.",
            'Virgo': "Your analytical skills make you excellent at budgeting and finding undervalued opportunities. You prefer conservative, well-researched investments.",
            'Libra': "Your diplomatic skills can create wealth through partnerships or beauty-related businesses. You appreciate balanced investment portfolios.",
            'Scorpio': "Your strategic thinking can uncover hidden opportunities and lead to wealth transformation. You excel at long-term financial planning.",
            'Sagittarius': "Your optimistic nature can create wealth through international or education-related ventures. Ground expansive visions with practical planning.",
            'Capricorn': "Your disciplined approach naturally builds substantial wealth through consistent saving and strategic investments.",
            'Aquarius': "Your innovative thinking can create wealth through technology or progressive investments aligned with your values.",
            'Pisces': "Your intuitive nature influences financial choices toward personally meaningful investments. Balance generosity with practical money management."
        }
        
        return {
            'title': 'Finances & Wealth Building',
            'sections': {
                'money_approach': {
                    'heading': f'Financial Style for {sun_sign}',
                    'content': financial_styles.get(sun_sign, f"Your {sun_sign} approach reflects your natural values and decision-making style.")
                }
            }
        }
    
    def interpret_family_children(self, chart_data):
        """Family and parenting insights"""
        moon_sign = chart_data.get('moon_sign', 'Cancer')
        sun_sign = chart_data.get('sun_sign', 'Aries')
        
        parenting_styles = {
            'Aries': "You encourage independence and courage in children, teaching them to be strong and pursue goals fearlessly.",
            'Taurus': "You provide stability and security, teaching children patience and appreciation for life's simple pleasures.",
            'Gemini': "You stimulate curiosity and communication, creating environments rich in learning and exploration.",
            'Cancer': "You nurture emotional development and create deep family bonds through caring attention.",
            'Leo': "You encourage self-expression and creativity, helping children develop confidence in their talents.",
            'Virgo': "You teach practical skills and attention to detail, helping children develop good habits.",
            'Libra': "You teach fairness and diplomacy, helping children appreciate beauty and harmony.",
            'Scorpio': "You encourage emotional honesty and depth, helping children understand life's complexities.",
            'Sagittarius': "You inspire adventure and learning, encouraging children to explore and question.",
            'Capricorn': "You teach responsibility and goal-setting, helping children build character through achievement.",
            'Aquarius': "You encourage individuality and social awareness, helping children think independently.",
            'Pisces': "You nurture creativity and compassion, helping children develop emotional intelligence."
        }
        
        return {
            'title': 'Family & Children',
            'sections': {
                'family_role': {
                    'heading': f'Your Family Role ({moon_sign} Moon)',
                    'content': f"Your {moon_sign} Moon influences how you nurture family members and create emotional bonds."
                },
                'parenting_style': {
                    'heading': 'Your Natural Parenting Approach',
                    'content': parenting_styles.get(sun_sign, f"Your {sun_sign} nature shapes how you guide children.")
                }
            }
        }
    
    def interpret_spiritual_growth(self, chart_data):
        """Spiritual development insights"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        
        spiritual_paths = {
            'Aries': "Your spiritual path involves balancing pioneering spirit with patience. You grow through leadership in spiritual communities and courageous service.",
            'Taurus': "Your spiritual development comes through connecting with nature and finding sacred meaning in life's simple pleasures.",
            'Gemini': "Your spiritual journey involves synthesizing diverse wisdom traditions and sharing insights through teaching or writing.",
            'Cancer': "Your spiritual path centers on developing healing abilities and creating nurturing communities where others can grow.",
            'Leo': "Your spiritual development involves expressing authentic self while serving something greater than personal recognition.",
            'Virgo': "Your spiritual path involves finding perfection through humble service and attention to life's sacred details.",
            'Libra': "Your spiritual journey involves creating harmony and justice through diplomatic service and mediation.",
            'Scorpio': "Your spiritual path involves deep transformation and helping others heal from life's wounds.",
            'Sagittarius': "Your spiritual development comes through exploring wisdom traditions and sharing philosophical insights.",
            'Capricorn': "Your spiritual path involves building lasting structures for spiritual purposes through disciplined practice.",
            'Aquarius': "Your spiritual journey involves humanitarian causes that advance consciousness for all humanity.",
            'Pisces': "Your spiritual path is naturally mystical, involving direct divine connection and selfless service."
        }
        
        return {
            'title': 'Spiritual Growth & Higher Purpose',
            'sections': {
                'spiritual_journey': {
                    'heading': f'Your {sun_sign} Spiritual Path',
                    'content': spiritual_paths.get(sun_sign, f"Your {sun_sign} nature suggests a unique approach to spiritual development.")
                }
            }
        }
    
    def interpret_communication_learning(self, chart_data):
        """Communication and learning insights"""
        mercury_sign = chart_data['planets'].get('mercury', {}).get('sign', chart_data.get('sun_sign', 'Aries'))
        
        communication_styles = {
            'Aries': "You communicate with directness and enthusiasm, preferring quick conversations. You learn best through hands-on experience and express ideas with motivating energy.",
            'Taurus': "You communicate thoughtfully and deliberately, preferring substantial conversations. You learn through practical application and express ideas emphasizing real-world value.",
            'Gemini': "You're a natural communicator who enjoys exploring ideas through conversation. You learn quickly through varied experiences and explain complex concepts accessibly.",
            'Cancer': "You communicate with emotional intelligence and intuitive understanding. You learn best in supportive environments and express ideas creating connection.",
            'Leo': "You communicate with warmth and engaging flair. You learn through creative expression and naturally explain ideas in inspiring ways.",
            'Virgo': "You communicate with precision and helpful detail. You learn through systematic study and organize complex information usefully.",
            'Libra': "You communicate diplomatically, always considering others' perspectives. You learn through discussion and present ideas in balanced ways.",
            'Scorpio': "You communicate with intensity and depth, preferring meaningful conversations. You learn through investigation and express ideas revealing hidden truths.",
            'Sagittarius': "You communicate enthusiasm for big ideas and philosophical concepts. You learn through exploration and explain concepts broadening perspectives.",
            'Capricorn': "You communicate with authority and practical wisdom. You learn through structured study and present ideas emphasizing long-term benefits.",
            'Aquarius': "You communicate innovative ideas challenging conventional thinking. You learn through experimentation and inspire others to consider new possibilities.",
            'Pisces': "You communicate with empathy and intuitive understanding. You learn through immersion and explain ideas helping others feel emotional truth."
        }
        
        return {
            'title': 'Communication & Learning',
            'sections': {
                'communication_style': {
                    'heading': f'Your {mercury_sign} Communication Style',
                    'content': communication_styles.get(mercury_sign, f"Your {mercury_sign} Mercury influences how you think and share ideas.")
                }
            }
        }
    
    def interpret_travel_adventure(self, chart_data):
        """Travel and adventure preferences"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        
        travel_styles = {
            'Aries': "You love adventure travel that challenges you physically and mentally. You prefer independent travel where you can make spontaneous decisions.",
            'Taurus': "You enjoy comfortable, scenic travel to beautiful destinations with good food and luxury accommodations.",
            'Gemini': "You love variety in travel, preferring trips offering multiple experiences and learning opportunities.",
            'Cancer': "You prefer travel that feels emotionally meaningful and connects you with family heritage or nurturing experiences.",
            'Leo': "You enjoy glamorous travel to exciting destinations where you can experience luxury and entertainment.",
            'Virgo': "You prefer well-organized travel with detailed itineraries and practical benefits like health retreats or educational tours.",
            'Libra': "You love romantic or aesthetically beautiful destinations offering cultural refinement and harmonious experiences.",
            'Scorpio': "You're drawn to transformative travel experiences offering depth and mystery like spiritual retreats or archaeological sites.",
            'Sagittarius': "You're the natural traveler, loving international adventures that expand your philosophical understanding of different cultures.",
            'Capricorn': "You prefer travel offering educational value and contributing to long-term goals like business or historical sites.",
            'Aquarius': "You enjoy unique, unconventional travel experiences most people wouldn't consider, including humanitarian travel.",
            'Pisces': "You prefer spiritual or artistic travel nourishing your soul, drawn to mystical destinations or places near water."
        }
        
        return {
            'title': 'Travel & Adventure',
            'sections': {
                'travel_preferences': {
                    'heading': f'Your {sun_sign} Travel Style',
                    'content': travel_styles.get(sun_sign, f"Your {sun_sign} nature influences what types of travel experiences inspire you most.")
                }
            }
        }
    
    def interpret_challenges_lessons(self, chart_data):
        """Life challenges and growth opportunities"""
        sun_sign = chart_data.get('sun_sign', 'Aries')
        
        growth_areas = {
            'Aries': "Your challenge is learning patience while maintaining natural leadership. Growth comes through developing diplomatic skills and understanding that true leadership serves others' highest good.",
            'Taurus': "Your challenge is developing flexibility while maintaining stability. Growth comes through learning when to adapt and finding balance between security and necessary evolution.",
            'Gemini': "Your challenge is developing depth while maintaining curiosity. Growth comes through choosing meaningful commitments and learning to complete projects before moving to new interests.",
            'Cancer': "Your challenge is setting boundaries while maintaining nurturing nature. Growth comes through learning to care for yourself and recognizing when helping becomes enabling.",
            'Leo': "Your challenge is sharing attention while maintaining confidence. Growth comes through learning that true leadership elevates others and your light shines brighter helping others discover their brilliance.",
            'Virgo': "Your challenge is accepting imperfection while maintaining excellence. Growth comes through learning 'good enough' is often sufficient and perfectionism can prevent completing important work.",
            'Libra': "Your challenge is making independent decisions while maintaining diplomacy. Growth comes through trusting your judgment and understanding some conflict is necessary for authentic relationships.",
            'Scorpio': "Your challenge is learning to trust while maintaining strength. Growth comes through understanding true power includes courage to be open and healing requires both strength and gentleness.",
            'Sagittarius': "Your challenge is developing commitment while maintaining freedom. Growth comes through learning depth enhances adventures and understanding that promises matter.",
            'Capricorn': "Your challenge is balancing achievement with enjoyment while maintaining discipline. Growth comes through celebrating progress and understanding success includes happiness, not just accomplishment.",
            'Aquarius': "Your challenge is connecting emotionally while maintaining objectivity. Growth comes through learning personal relationships enhance your ability to serve humanity's evolution.",
            'Pisces': "Your challenge is developing boundaries while maintaining compassion. Growth comes through learning self-care enables you to serve others more effectively."
        }
        
        return {
            'title': 'Life Challenges & Growth Opportunities',
            'sections': {
                'growth_edge': {
                    'heading': f'Your {sun_sign} Growth Challenge',
                    'content': growth_areas.get(sun_sign, f"Your {sun_sign} nature brings both gifts and growth opportunities.")
                }
            }
        }
    
    # ========== YOUR EXISTING TECHNICAL METHODS (UNCHANGED) ==========
    
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
            'conjunction': (0, 6),      
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
                
                predictions.extend([
                    {
                        'type': 'solar',
                        'description': f"Solar Energy in {sun_sign}",
                        'interpretation': f"The Sun in {sun_sign} brings opportunities for growth in {sun_sign.lower()} themes. This is an excellent time to focus on developing your {sun_sign.lower()} qualities and pursuing related goals.",
                        'strength': 'strong',
                        'precision': 'enhanced'
                    },
                    {
                        'type': 'lunar', 
                        'description': f"Lunar Energy in {moon_sign}",
                        'interpretation': f"The Moon in {moon_sign} influences your emotional responses and intuitive insights. Pay attention to {moon_sign.lower()} qualities in your feelings and reactions.",
                        'strength': 'moderate',
                        'precision': 'enhanced'
                    }
                ])
                
            else:
                # Fallback to standard calculations
                from astro_calc import AstrologyCalculator
                calc = AstrologyCalculator()
                
                current_sun_sign = calc.get_sun_sign(prediction_date)
                current_moon_sign = calc.get_moon_sign(prediction_date)
                
                predictions.extend([
                    {
                        'type': 'solar',
                        'description': f"Current solar energy in {current_sun_sign}",
                        'interpretation': f"The Sun's position in {current_sun_sign} emphasizes themes of {current_sun_sign.lower()} expression and growth opportunities in related areas.",
                        'strength': 'moderate',
                        'precision': 'standard'
                    },
                    {
                        'type': 'lunar',
                        'description': f"Current lunar energy in {current_moon_sign}",
                        'interpretation': f"The Moon in {current_moon_sign} brings {current_moon_sign.lower()} emotional influences and intuitive guidance to your daily experiences.",
                        'strength': 'moderate',
                        'precision': 'standard'
                    }
                ])
            
        except Exception as e:
            predictions.append({
                'type': 'error',
                'description': 'Current cosmic energies are being calculated',
                'interpretation': 'The universe is aligning to provide you with meaningful guidance. Please try again in a moment.',
                'precision': 'calculating'
            })
        
        return predictions
