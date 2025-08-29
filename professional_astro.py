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
                'enable_logging': False,
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
        """Calculate comprehensive birth chart with enhanced precision and interpretations"""
        
        # Get base chart data
        if self.precision_mode == 'ENHANCED':
            chart_data = self._enhanced_precision_calculation(birth_datetime, latitude, longitude, house_system)
        else:
            chart_data = self._standard_calculation(birth_datetime, latitude, longitude, house_system)
        
        # Add comprehensive interpretations
        chart_data['comprehensive_interpretations'] = self.generate_comprehensive_interpretation(chart_data)
        
        return chart_data
    
    def generate_comprehensive_interpretation(self, chart_data):
        """Generate detailed interpretations across all life aspects"""
        
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
        """Deep personality analysis with practical insights"""
        sun_sign = chart_data['planets']['sun']['sign']
        moon_sign = chart_data['planets']['moon']['sign']
        rising_sign = chart_data['houses'][0]['sign'] if chart_data.get('houses') else 'Unknown'
        
        sun_descriptions = {
            'Aries': "You possess a pioneering spirit that drives you to lead and initiate new ventures. Your natural confidence inspires others to follow your vision, though practicing patience when others don't match your energetic pace will enhance your leadership effectiveness. You thrive when you can be first to explore new territories, whether in ideas, projects, or experiences.",
            'Taurus': "You bring remarkable stability and practical wisdom to every situation you encounter. Your persistence and reliability make you someone others can truly depend on, though developing flexibility helps you adapt gracefully when circumstances require change. You have an innate ability to create beauty and comfort in your environment.",
            'Gemini': "Your quick wit and insatiable curiosity make you an excellent communicator and natural networker. You thrive on variety and mental stimulation, easily connecting diverse ideas and people, though focusing on developing depth rather than just breadth can significantly deepen your impact and expertise in chosen areas.",
            'Cancer': "Your intuitive nature and emotional intelligence help you nurture and support others with remarkable sensitivity. You naturally create safe, welcoming spaces where people can grow and heal, though learning to set healthy boundaries protects your sensitive energy while still allowing you to care for others.",
            'Leo': "Your natural charisma and creative spirit have the power to light up any room you enter. You inspire others through authentic self-expression and generous leadership, though sharing the spotlight and celebrating others' achievements enhances your own radiance and builds lasting loyalty from those around you.",
            'Virgo': "Your keen attention to detail and genuine desire to serve creates meaningful improvements in everything you touch. Your analytical mind excels at solving complex problems and streamlining processes, though practicing self-compassion balances your perfectionist tendencies and allows you to appreciate your significant contributions.",
            'Libra': "Your diplomatic nature and refined aesthetic sense bring harmony to relationships and beauty to environments. You excel at seeing multiple perspectives and finding fair solutions to conflicts, though learning to trust your own judgment strengthens your decision-making and reduces the stress of over-deliberation.",
            'Scorpio': "Your emotional depth and transformative power help others heal and evolve in profound ways. You see beneath surfaces to essential truths that others miss, though embracing vulnerability in your connections allows others to truly know and appreciate your remarkable inner strength and wisdom.",
            'Sagittarius': "Your philosophical nature and love of adventure naturally expands minds and opens new possibilities for growth. You inspire others to think bigger and explore beyond their comfort zones, though grounding your expansive visions with practical steps makes your dreams achievable realities.",
            'Capricorn': "Your discipline and long-term vision create lasting structures and achievements that benefit everyone around you. You excel at building things that endure through time and challenge, though remembering to celebrate small wins along the way sustains your motivation for the lengthy journey to your ambitious goals.",
            'Aquarius': "Your innovative thinking and humanitarian spirit advance society toward a better future for all. You naturally see possibilities and solutions that others haven't considered, though connecting with others' emotional needs and experiences strengthens your ability to implement your visionary ideas.",
            'Pisces': "Your compassionate nature and vivid imagination heal and inspire everyone you encounter. You understand life's deeper spiritual meanings and can translate abstract concepts into accessible wisdom, though maintaining healthy emotional boundaries preserves your sensitive energy for the important work you do."
        }
        
        moon_descriptions = {
            'Aries': "emotionally direct and need independence and excitement to feel truly secure and alive",
            'Taurus': "emotionally steady and need comfort, routine, and material security to feel safe and grounded",
            'Gemini': "emotionally curious and need mental stimulation and variety to feel engaged and fulfilled",
            'Cancer': "deeply emotional and need family connections and nurturing environments to feel complete",
            'Leo': "emotionally expressive and need appreciation and creative outlets to feel valued and vibrant",
            'Virgo': "emotionally practical and need order, purpose, and useful activity to feel calm and centered",
            'Libra': "emotionally harmonious and need balanced relationships and beautiful surroundings to feel peaceful",
            'Scorpio': "emotionally intense and need deep, authentic connections to feel truly understood and accepted",
            'Sagittarius': "emotionally adventurous and need freedom and philosophical meaning to feel truly alive",
            'Capricorn': "emotionally reserved and need achievement and respect to feel worthy and accomplished",
            'Aquarius': "emotionally detached and need intellectual connection and social causes to feel fulfilled",
            'Pisces': "emotionally sensitive and need spiritual connection and creative expression to feel whole"
        }
        
        return {
            'title': 'Your Core Personality & Life Path',
            'sections': {
                'essential_self': {
                    'heading': f'Your Sun in {sun_sign} - Your Life Purpose & Core Identity',
                    'content': sun_descriptions.get(sun_sign, f"Your {sun_sign} nature brings unique gifts and perspectives to the world around you.")
                },
                'emotional_nature': {
                    'heading': f'Your Moon in {moon_sign} - Your Inner Emotional World',
                    'content': f"At your emotional core, you are {moon_descriptions.get(moon_sign, 'emotionally complex and multifaceted')}. Understanding and honoring these deep emotional needs is fundamental to your happiness, relationships, and overall life satisfaction."
                },
                'public_persona': {
                    'heading': f'Your {rising_sign} Rising - How the World Sees You',
                    'content': f"Your {rising_sign} Ascendant shapes how others initially perceive you and influences your approach to new situations and challenges." if rising_sign != 'Unknown' else "Your rising sign creates the first impression you make and influences how you instinctively respond to life's opportunities and challenges."
                }
            }
        }
    
    def interpret_career_profession(self, chart_data):
        """Career and professional life analysis with practical guidance"""
        sun_sign = chart_data['planets']['sun']['sign']
        
        career_insights = {
            'Aries': "You excel in careers that allow you to pioneer new initiatives and lead dynamic teams. Consider entrepreneurship, emergency services, competitive sports, or any field where you can be first to market. Your natural leadership shines when you can take charge of challenging projects and inspire others through decisive action.",
            'Taurus': "You thrive in careers that build lasting value and provide financial security. Banking, real estate, agriculture, luxury goods, or artisanal crafts align with your nature. Your patience and reliability make you exceptional at long-term projects and creating systems that others can depend upon for years to come.",
            'Gemini': "Your communication skills and versatility suit careers in media, education, sales, writing, or technology. You excel at connecting people and ideas, making you valuable in networking roles, journalism, or any field requiring quick thinking and adaptability to changing information.",
            'Cancer': "Your nurturing abilities and emotional intelligence make you exceptional in healthcare, hospitality, childcare, or real estate. You create environments where others feel safe and supported, making you naturally suited for counseling, teaching, or any role focused on caring for others' wellbeing.",
            'Leo': "Your creative flair and natural charisma suit entertainment, education, luxury retail, or management roles. You inspire others through your enthusiasm and vision, making you effective in leadership positions where you can showcase talent and motivate teams toward ambitious goals.",
            'Virgo': "Your analytical skills and attention to detail excel in healthcare, quality control, editing, research, or technical fields. You improve systems and processes wherever you go, making you invaluable in roles requiring precision, organization, and methodical problem-solving approaches.",
            'Libra': "Your diplomatic skills and aesthetic sense suit law, diplomacy, design, counseling, or partnership-based businesses. You excel at creating harmony and finding win-win solutions, making you effective in mediation, client relations, or any role requiring interpersonal finesse.",
            'Scorpio': "Your investigative nature and transformative abilities suit psychology, research, finance, healing arts, or crisis management. You see what others miss and help people navigate profound changes, making you powerful in roles requiring depth and emotional courage.",
            'Sagittarius': "Your love of learning and cultural exploration suit education, travel, publishing, law, or international business. You expand others' horizons through teaching, writing, or creating experiences that broaden perspectives and inspire philosophical growth.",
            'Capricorn': "Your discipline and long-term vision suit business leadership, government, engineering, or traditional professional fields. You build lasting institutions and climb career ladders through persistent effort, eventually achieving positions of significant authority and respect.",
            'Aquarius': "Your innovative thinking suits technology, humanitarian work, scientific research, or progressive social causes. You see future trends before others and work effectively in teams focused on advancing society through breakthrough ideas and systematic change.",
            'Pisces': "Your creativity and compassion suit arts, healing professions, spirituality, or charitable work. You bring inspiration and emotional healing to your work, making you effective in roles where you can use imagination and empathy to serve others' deepest needs."
        }
        
        return {
            'title': 'Career & Professional Success',
            'sections': {
                'career_direction': {
                    'heading': f'Professional Path for {sun_sign}',
                    'content': career_insights.get(sun_sign, f"Your {sun_sign} nature offers unique professional advantages and opportunities for meaningful career development.")
                },
                'success_strategies': {
                    'heading': 'Keys to Professional Success',
                    'content': f"Your {sun_sign} strengths position you for success when you align your career with your natural talents and values. Focus on roles that energize rather than drain you, and seek environments where your unique contributions are recognized and valued."
                }
            }
        }
    
    def interpret_relationships_love(self, chart_data):
        """Love and relationship insights with practical guidance"""
        sun_sign = chart_data['planets']['sun']['sign']
        moon_sign = chart_data['planets']['moon']['sign']
        venus_sign = chart_data['planets'].get('venus', {}).get('sign', 'Unknown')
        
        love_insights = {
            'Aries': "In love, you bring passion, excitement, and unwavering loyalty to your relationships. You love with your whole heart and appreciate partners who can match your enthusiasm for life's adventures. You need independence within partnership and thrive with someone who encourages your goals while maintaining their own identity.",
            'Taurus': "You offer steady, devoted love and create beautiful, comfortable shared spaces. You show love through practical actions and physical affection, preferring stable, long-term commitments over casual dating. You need security and consistency in love, and you provide the same reliable foundation for your partner.",
            'Gemini': "You bring playfulness, intellectual stimulation, and great conversation to relationships. You need mental connection as much as emotional intimacy and appreciate partners who can engage with your ideas and adapt to your changing interests. Variety and communication keep your relationships fresh and engaging.",
            'Cancer': "You nurture your loved ones with deep emotional care and intuitive understanding. You create a sense of home and family wherever you are, offering emotional security and comfort. You need to feel emotionally safe and appreciated for your caring nature, and you give the same protective love in return.",
            'Leo': "You bring warmth, generosity, and romantic flair to your relationships. You love to celebrate your partner and create memorable experiences together. You need appreciation and admiration in love, and you naturally give the same generous recognition to your partner's unique qualities and achievements.",
            'Virgo': "You show love through thoughtful actions and genuine care for your partner's wellbeing. You pay attention to the small details that matter and work steadily to improve your relationships. You need to feel useful and appreciated in love, offering practical support and expecting the same consideration in return.",
            'Libra': "You bring harmony, romance, and diplomatic grace to your partnerships. You naturally seek balance and fairness in relationships and excel at seeing your partner's perspective. You need beauty and peace in love, working to create relationships where both partners feel heard and valued.",
            'Scorpio': "You offer intense, transformative love that goes beyond surface attraction. You seek deep emotional and spiritual connection with your partner and are fiercely loyal once you commit. You need complete honesty and emotional courage in love, offering the same authentic vulnerability in return.",
            'Sagittarius': "You bring adventure, optimism, and philosophical depth to your relationships. You need freedom to explore and grow within partnership and appreciate partners who share your love of learning and adventure. You inspire your loved ones to expand their horizons and embrace life's possibilities.",
            'Capricorn': "You build relationships with the same care and long-term vision you bring to everything else. You show love through commitment, reliability, and working toward shared goals. You need respect and stability in love, offering the same steady foundation for building a lasting partnership.",
            'Aquarius': "You bring unique perspectives and humanitarian values to your relationships. You need intellectual connection and personal freedom within partnership, appreciating partners who respect your individuality while sharing your vision for a better world. Friendship forms the foundation of your romantic connections.",
            'Pisces': "You love with boundless compassion and intuitive understanding of your partner's deepest needs. You bring creativity, spirituality, and emotional healing to relationships. You need kindness and emotional safety in love, offering the same gentle acceptance and support to your partner."
        }
        
        return {
            'title': 'Love & Relationships',
            'sections': {
                'love_nature': {
                    'heading': f'Your {sun_sign} Love Style',
                    'content': love_insights.get(sun_sign, f"Your {sun_sign} nature brings unique gifts to your romantic relationships and partnerships.")
                },
                'relationship_needs': {
                    'heading': f'Emotional Needs in Relationships ({moon_sign} Moon)',
                    'content': f"With your Moon in {moon_sign}, you feel most loved and secure when your emotional needs for connection, understanding, and support are met in ways that honor your sensitive inner nature."
                }
            }
        }
    
    def interpret_health_vitality(self, chart_data):
        """Health and wellness guidance based on astrological indicators"""
        sun_sign = chart_data['planets']['sun']['sign']
        
        health_insights = {
            'Aries': "Your dynamic energy needs regular physical outlets to maintain optimal health. High-intensity exercise, competitive sports, or martial arts help you release stress and stay strong. Pay attention to head, eyes, and stress-related issues. Your quick healing and natural vitality serve you well when you maintain active lifestyle.",
            'Taurus': "Your steady constitution benefits from consistent, moderate exercise and attention to nutrition. Walking, yoga, strength training, or gardening suit your nature. Watch throat, neck, and weight-related concerns. Your body responds well to natural remedies, massage, and maintaining regular sleep and eating schedules.",
            'Gemini': "Your active mind needs variety in physical activities to stay engaged with fitness routines. Team sports, dance classes, or activities that combine learning with movement work well. Pay attention to hands, arms, lungs, and nervous system. Mental stimulation and social exercise keep you motivated and healthy.",
            'Cancer': "Your sensitive system benefits from gentle, nurturing approaches to health and wellness. Swimming, walking, or home-based exercise routines suit you well. Watch digestive system, chest, and emotional eating patterns. Your intuitive connection to your body helps you recognize what you need for optimal health.",
            'Leo': "Your vital energy shines when you enjoy your fitness routine and can express yourself through movement. Dance, performance-based fitness, or heart-healthy activities align with your nature. Pay attention to heart, back, and circulation. You thrive when exercise feels like creative expression rather than obligation.",
            'Virgo': "Your methodical approach to health serves you well when you create detailed wellness routines. Precise exercise programs, nutrition tracking, or health-focused activities suit your systematic nature. Watch digestive system, nervous system, and perfectionist stress. Your attention to detail helps optimize your health protocols.",
            'Libra': "Your love of beauty and balance draws you to aesthetically pleasing and harmonious fitness activities. Partner workouts, ballet, or activities in beautiful settings motivate you. Watch kidneys, lower back, and stress from indecision. Social exercise and balanced approaches to wellness work best for you.",
            'Scorpio': "Your intense nature benefits from transformative, challenging fitness routines that push your limits. Intense strength training, transformative practices, or healing arts suit your depth. Watch reproductive system, elimination, and stress-related issues. You heal powerfully when you address root causes.",
            'Sagittarius': "Your adventurous spirit thrives with outdoor activities and varied fitness experiences. Hiking, adventure sports, or fitness challenges that feel like exploration motivate you. Watch hips, thighs, and overextension injuries. Your optimistic nature supports healing when you maintain variety in your wellness approach.",
            'Capricorn': "Your disciplined approach to health creates lasting wellness habits through consistent, goal-oriented routines. Structured fitness programs, mountain climbing, or endurance activities suit your determination. Watch bones, joints, and stress from overwork. Your persistence pays off in long-term health achievements.",
            'Aquarius': "Your innovative nature enjoys unique, technology-enhanced, or group fitness activities. Unusual sports, fitness gadgets, or community wellness programs appeal to you. Watch circulation, ankles, and stress from overstimulation. Your progressive approach to health often leads you to beneficial new wellness trends.",
            'Pisces': "Your sensitive system responds well to gentle, flowing movement and water-based activities. Swimming, yoga, tai chi, or dance suit your fluid nature. Watch feet, immune system, and emotional stress affecting physical health. Your intuitive connection to healing helps you find what your body truly needs."
        }
        
        return {
            'title': 'Health & Vitality',
            'sections': {
                'health_approach': {
                    'heading': f'Wellness Approach for {sun_sign}',
                    'content': health_insights.get(sun_sign, f"Your {sun_sign} constitution benefits from approaches to health and fitness that align with your natural energy and preferences.")
                },
                'vitality_tips': {
                    'heading': 'Maintaining Optimal Health',
                    'content': f"Your {sun_sign} nature thrives when you honor your body's natural rhythms and choose wellness activities that energize rather than deplete you. Listen to your body's signals and adjust your health routines accordingly."
                }
            }
        }
    
    def interpret_finances_wealth(self, chart_data):
        """Financial patterns and wealth-building guidance"""
        sun_sign = chart_data['planets']['sun']['sign']
        
        financial_insights = {
            'Aries': "Your entrepreneurial spirit and willingness to take calculated risks can lead to significant financial gains. You excel at spotting new opportunities and acting quickly, though developing patience for long-term investments balances your impulsive tendencies. Your leadership abilities can create multiple income streams.",
            'Taurus': "Your natural financial instincts and patience with long-term growth make you excellent at building substantial wealth over time. You appreciate quality investments and tangible assets like real estate or collectibles. Your steady approach and resistance to get-rich-quick schemes serve your financial security well.",
            'Gemini': "Your versatility and communication skills create opportunities for diverse income sources and financial innovation. You excel at finding information that leads to profitable opportunities, though focusing on fewer, higher-quality investments may yield better returns than scattered financial activities.",
            'Cancer': "Your intuitive approach to money and focus on security lead you to make emotionally satisfying financial choices. You excel at saving for family needs and long-term security, though balancing emotional spending with practical financial planning helps you achieve both security and growth.",
            'Leo': "Your confidence and leadership abilities can attract wealth through creative ventures and high-visibility opportunities. You may enjoy investing in luxury items or experiences, though balancing your generous nature with consistent saving ensures your financial stability matches your lifestyle preferences.",
            'Virgo': "Your analytical skills and attention to detail make you excellent at budgeting, cost analysis, and finding undervalued opportunities. You prefer conservative, well-researched investments and excel at maximizing efficiency in your financial planning and spending decisions.",
            'Libra': "Your diplomatic skills and aesthetic sense can create wealth through partnerships, beauty-related businesses, or luxury markets. You appreciate balanced investment portfolios and may benefit from financial partnerships, though making decisions independently strengthens your financial confidence.",
            'Scorpio': "Your investigative abilities and strategic thinking can uncover hidden financial opportunities and lead to substantial wealth transformation. You excel at long-term financial planning and may profit from investments others overlook, particularly in transformation or healing industries.",
            'Sagittarius': "Your optimistic nature and global perspective can create wealth through international investments, education, or travel-related ventures. You may benefit from diverse, growth-oriented investments, though grounding your expansive financial visions with practical planning ensures success.",
            'Capricorn': "Your disciplined approach and long-term vision naturally build substantial wealth through consistent saving and strategic investments. You excel at traditional wealth-building methods and may achieve significant financial status through patient, methodical financial planning.",
            'Aquarius': "Your innovative thinking and humanitarian values can create wealth through technology, social causes, or progressive investments. You may pioneer new financial approaches or benefit from investing in future-focused industries that align with your values.",
            'Pisces': "Your intuitive nature and compassionate values influence your financial choices, often leading to investments that feel personally meaningful. You may benefit from creative or spiritually-aligned financial opportunities, though practical money management balances your generous instincts."
        }
        
        return {
            'title': 'Finances & Wealth Building',
            'sections': {
                'money_approach': {
                    'heading': f'Financial Style for {sun_sign}',
                    'content': financial_insights.get(sun_sign, f"Your {sun_sign} approach to money and wealth building reflects your natural values and decision-making style.")
                },
                'wealth_strategy': {
                    'heading': 'Building Financial Security',
                    'content': f"Your {sun_sign} nature suggests specific strategies for building wealth that align with your values and natural abilities. Focus on approaches that feel authentic to you while maintaining practical financial discipline."
                }
            }
        }
    
    def interpret_family_children(self, chart_data):
        """Family relationships and parenting insights"""
        moon_sign = chart_data['planets']['moon']['sign']
        
        family_insights = {
            'Aries': "You bring energy and leadership to family dynamics, encouraging independence and courage in loved ones. As a parent, you inspire children to be brave and pursue their dreams, though balancing your high expectations with patience helps children develop at their own pace.",
            'Taurus': "You create stable, nurturing family environments where everyone feels secure and loved. Your consistent presence and practical care provide the foundation family members need to thrive, and you excel at creating beautiful, comfortable homes filled with warmth and tradition.",
            'Cancer': "Your natural nurturing instincts make family your top priority, and you intuitively understand what each family member needs. You create emotional safety and belonging, though maintaining some boundaries helps you care for others without depleting your own emotional resources.",
            'Leo': "You bring warmth, celebration, and creative joy to family life, making every gathering feel special. You encourage family members to express their unique talents and feel proud of their achievements, creating an atmosphere of mutual appreciation and support.",
            'Virgo': "You show family love through practical care and attention to everyone's daily needs and wellbeing. Your organized approach to family life creates smooth routines, though accepting imperfection allows for more spontaneous family joy and connection."
        }
        
        parenting_styles = {
            'Aries': "You encourage independence and courage in children, teaching them to be strong and pursue their goals fearlessly.",
            'Taurus': "You provide stability and security, teaching children the value of consistency, patience, and appreciation for life's simple pleasures.",
            'Gemini': "You stimulate children's curiosity and communication skills, creating an environment rich in learning and intellectual exploration.",
            'Cancer': "You nurture children's emotional development and create deep family bonds through caring attention and intuitive understanding.",
            'Leo': "You encourage children's self-expression and creativity, helping them develop confidence and pride in their unique talents.",
            'Virgo': "You teach children practical skills and attention to detail, helping them develop good habits and problem-solving abilities."
        }
        
        return {
            'title': 'Family & Children',
            'sections': {
                'family_role': {
                    'heading': f'Your Role in Family ({moon_sign} Moon)',
                    'content': family_insights.get(moon_sign, f"Your {moon_sign} Moon influences how you nurture and connect with family members, creating your unique contribution to family harmony and growth.")
                },
                'parenting_style': {
                    'heading': 'Your Natural Parenting Approach',
                    'content': parenting_styles.get(chart_data['planets']['sun']['sign'], f"Your {chart_data['planets']['sun']['sign']} nature shapes how you guide and support the children in your life.")
                }
            }
        }
    
    def interpret_spiritual_growth(self, chart_data):
        """Spiritual path and personal development insights"""
        sun_sign = chart_data['planets']['sun']['sign']
        
        spiritual_paths = {
            'Aries': "Your spiritual path involves learning to balance your pioneering spirit with patience and consideration for others. You grow through taking on leadership roles in spiritual communities and finding ways to serve that utilize your natural courage and initiative.",
            'Taurus': "Your spiritual development comes through connecting with the divine in nature and finding sacred meaning in life's simple pleasures. You grow by creating beautiful, peaceful spaces for reflection and by serving others through practical acts of kindness.",
            'Gemini': "Your spiritual journey involves synthesizing diverse wisdom traditions and sharing spiritual insights through teaching or writing. You grow by exploring different perspectives on truth and finding ways to communicate spiritual concepts clearly to others.",
            'Cancer': "Your spiritual path centers on developing your natural healing abilities and creating nurturing communities where others can grow. You find the divine through family connections, emotional healing work, and caring for those who need support.",
            'Leo': "Your spiritual development involves learning to express your authentic self while serving something greater than personal recognition. You grow by using your creative gifts and natural leadership to inspire others and spread joy and encouragement.",
            'Virgo': "Your spiritual path involves finding perfection through humble service and attention to life's sacred details. You grow by developing practical spiritual disciplines and by serving others through healing work or by improving systems that help people.",
            'Libra': "Your spiritual journey involves learning to create harmony and justice in the world through diplomatic service. You grow by mediating conflicts, creating beauty that inspires others, and building bridges between different groups or ideas.",
            'Scorpio': "Your spiritual path involves deep transformation and helping others heal from life's wounds. You grow by facing your own shadows honestly and by serving as a guide for others through their own processes of death and rebirth.",
            'Sagittarius': "Your spiritual development comes through exploring different wisdom traditions and sharing philosophical insights that expand others' horizons. You grow by teaching, traveling, or engaging with diverse cultures and belief systems.",
            'Capricorn': "Your spiritual path involves building lasting structures that serve spiritual purposes and developing wisdom through disciplined practice. You grow by taking responsibility for spiritual leadership and by creating institutions that support others' growth.",
            'Aquarius': "Your spiritual journey involves working for humanitarian causes that advance consciousness for all humanity. You grow by participating in groups focused on social progress and by developing innovative approaches to spiritual practice.",
            'Pisces': "Your spiritual path is naturally mystical and compassionate, involving direct connection with the divine and service to those who suffer. You grow through meditation, creative expression, and acts of selfless service that transcend personal boundaries."
        }
        
        return {
            'title': 'Spiritual Growth & Higher Purpose',
            'sections': {
                'spiritual_path': {
                    'heading': f'Your {sun_sign} Spiritual Journey',
                    'content': spiritual_paths.get(sun_sign, f"Your {sun_sign} nature suggests a unique approach to spiritual development and service to others.")
                },
                'higher_purpose': {
                    'heading': 'Your Soul\'s Mission',
                    'content': f"Your {sun_sign} soul came here to develop specific qualities and contribute to the world\'s healing and evolution. Your spiritual growth serves not only your own development but also helps others find their own path to wisdom and service."
                }
            }
        }
    
    def interpret_communication_learning(self, chart_data):
        """Communication style and learning preferences"""
        mercury_sign = chart_data['planets'].get('mercury', {}).get('sign', chart_data['planets']['sun']['sign'])
        
        communication_styles = {
            'Aries': "You communicate with directness and enthusiasm, preferring quick, to-the-point conversations. You learn best through hands-on experience and interactive discussions, and you express ideas with confidence and energy that motivates others to take action.",
            'Taurus': "You communicate thoughtfully and deliberately, preferring substantial conversations over small talk. You learn through practical application and repetition, and you express ideas in ways that emphasize stability, value, and real-world applications.",
            'Gemini': "You're a natural communicator who enjoys exploring ideas through conversation and debate. You learn quickly through reading, discussion, and varied experiences, and you excel at explaining complex concepts in accessible ways that engage others' curiosity.",
            'Cancer': "You communicate with emotional intelligence and intuitive understanding of others' feelings. You learn best in supportive environments and remember information that has emotional significance, expressing ideas in ways that create connection and understanding.",
            'Leo': "You communicate with warmth and dramatic flair that captures others' attention. You learn through creative expression and presentation, and you naturally explain ideas in engaging, entertaining ways that inspire others and build their confidence.",
            'Virgo': "You communicate with precision and attention to helpful detail. You learn through systematic study and practical application, and you excel at organizing complex information into useful formats that others can understand and implement.",
            'Libra': "You communicate diplomatically, always considering others' perspectives and seeking harmonious dialogue. You learn through discussion and comparison of different viewpoints, and you present ideas in balanced ways that help others see multiple sides of issues.",
            'Scorpio': "You communicate with intensity and depth, preferring meaningful conversations to superficial chat. You learn through investigation and experience, and you express ideas in ways that reveal hidden truths and encourage others to think more deeply.",
            'Sagittarius': "You communicate with enthusiasm for big ideas and philosophical concepts. You learn through exploration and cultural exchange, and you naturally explain concepts in ways that broaden others' perspectives and inspire them to think beyond current limitations.",
            'Capricorn': "You communicate with authority and practical wisdom gained through experience. You learn through structured study and real-world application, and you present ideas in ways that emphasize their practical value and long-term benefits.",
            'Aquarius': "You communicate innovative ideas and progressive concepts that challenge conventional thinking. You learn through experimentation and group discussion, and you express ideas in ways that inspire others to consider new possibilities and social improvements.",
            'Pisces': "You communicate with empathy and intuitive understanding that reaches others' hearts. You learn through immersion and creative expression, and you explain ideas in ways that help others feel the emotional truth and spiritual significance behind concepts."
        }
        
        return {
            'title': 'Communication & Learning',
            'sections': {
                'communication_style': {
                    'heading': f'Your {mercury_sign} Communication Style',
                    'content': communication_styles.get(mercury_sign, f"Your {mercury_sign} Mercury influences how you think, learn, and share ideas with others.")
                },
                'learning_approach': {
                    'heading': 'How You Learn Best',
                    'content': f"Understanding your {mercury_sign} learning style helps you choose educational approaches and communication methods that work with rather than against your natural mental processes and preferences."
                }
            }
        }
    
    def interpret_travel_adventure(self, chart_data):
        """Travel and adventure preferences"""
        sun_sign = chart_data['planets']['sun']['sign']
        
        travel_styles = {
            'Aries': "You love adventure travel that challenges you physically and mentally. Extreme sports destinations, pioneering new routes, or competitive travel experiences energize you. You prefer independent travel where you can make spontaneous decisions and explore at your own energetic pace.",
            'Taurus': "You enjoy comfortable, scenic travel to beautiful destinations with good food and luxury accommodations. You prefer well-planned trips to stable destinations where you can relax and enjoy sensory pleasures without rushing through packed itineraries.",
            'Gemini': "You love variety in travel, preferring trips that offer multiple experiences and learning opportunities. City breaks, cultural tours, or educational travel satisfy your curiosity, and you enjoy trips where you can meet locals and engage in interesting conversations.",
            'Cancer': "You prefer travel that feels emotionally meaningful and connects you with family heritage or nurturing experiences. You enjoy destinations with historical significance, coastal locations, or places where you can create lasting memories with loved ones.",
            'Leo': "You enjoy glamorous travel to exciting destinations where you can experience luxury and entertainment. You prefer trips that offer opportunities for creative expression, cultural performances, or experiences that make you feel special and celebrated.",
            'Virgo': "You prefer well-organized travel with detailed itineraries and practical benefits. Health retreats, educational tours, or eco-travel appeal to you, and you enjoy trips where you can learn new skills or contribute to meaningful causes.",
            'Libra': "You love romantic or aesthetically beautiful destinations that offer cultural refinement and harmonious experiences. Art-focused travel, wine country, or destinations known for their beauty and grace appeal to your refined sensibilities.",
            'Scorpio': "You're drawn to transformative travel experiences that offer depth and mystery. Spiritual retreats, archaeological sites, or destinations with rich psychological or mystical significance provide the profound experiences you seek.",
            'Sagittarius': "You're the natural traveler of the zodiac, loving international adventures that expand your philosophical understanding. You prefer independent travel to diverse cultures where you can learn about different ways of life and belief systems.",
            'Capricorn': "You prefer travel that offers educational value and contributes to your long-term goals. Business travel, historical sites, or destinations that enhance your professional development appeal to your practical approach to experiences.",
            'Aquarius': "You enjoy unique, unconventional travel experiences that most people wouldn't consider. You're drawn to progressive destinations, technology-focused travel, or humanitarian travel that allows you to contribute to social causes.",
            'Pisces': "You prefer spiritual or artistic travel that nourishes your soul and creativity. You're drawn to mystical destinations, artistic retreats, or places near water where you can connect with your intuitive and imaginative nature."
        }
        
        return {
            'title': 'Travel & Adventure',
            'sections': {
                'travel_style': {
                    'heading': f'Your {sun_sign} Travel Preferences',
                    'content': travel_styles.get(sun_sign, f"Your {sun_sign} nature influences what types of travel experiences energize and inspire you most.")
                },
                'adventure_growth': {
                    'heading': 'Growth Through Exploration',
                    'content': f"Travel and new experiences help you develop your {sun_sign} qualities while challenging you to grow beyond your comfort zone. Choose adventures that align with your natural interests while gently pushing your boundaries."
                }
            }
        }
    
    def interpret_challenges_lessons(self, chart_data):
        """Life challenges and growth opportunities"""
        sun_sign = chart_data['planets']['sun']['sign']
        saturn_sign = chart_data['planets'].get('saturn', {}).get('sign', 'Unknown')
        
        growth_challenges = {
            'Aries': "Your challenge is learning patience and considering others' needs while maintaining your natural leadership and initiative. Growth comes through developing diplomatic skills and learning that true leadership serves others' highest good as well as your own ambitions.",
            'Taurus': "Your challenge is developing flexibility and openness to change while maintaining your natural stability and values. Growth comes through learning when to adapt and when to stand firm, finding the balance between security and necessary evolution.",
            'Gemini': "Your challenge is developing depth and follow-through while maintaining your natural curiosity and versatility. Growth comes through choosing commitments that truly matter to you and learning to complete projects before moving to new interests.",
            'Cancer': "Your challenge is setting healthy boundaries while maintaining your natural nurturing and emotional sensitivity. Growth comes through learning to care for yourself as well as others and recognizing when your helping becomes enabling.",
            'Leo': "Your challenge is sharing attention and credit while maintaining your natural confidence and creative expression. Growth comes through learning that true leadership elevates others and that your light shines brighter when you help others discover their own brilliance.",
            'Virgo': "Your challenge is accepting imperfection while maintaining your natural desire for excellence and service. Growth comes through learning that 'good enough' is often sufficient and that perfectionism can prevent you from completing important work.",
            'Libra': "Your challenge is making decisions independently while maintaining your natural diplomacy and desire for harmony. Growth comes through learning to trust your own judgment and understanding that some conflict is necessary for authentic relationships.",
            'Scorpio': "Your challenge is learning to trust and be vulnerable while maintaining your natural strength and emotional depth. Growth comes through understanding that true power includes the courage to be open and that healing requires both strength and gentleness.",
            'Sagittarius': "Your challenge is developing commitment and attention to detail while maintaining your natural optimism and love of freedom. Growth comes through learning that depth enhances rather than limits your adventures and that promises matter.",
            'Capricorn': "Your challenge is balancing achievement with enjoyment while maintaining your natural discipline and ambition. Growth comes through learning to celebrate progress and understanding that success includes happiness, not just accomplishment.",
            'Aquarius': "Your challenge is connecting emotionally while maintaining your natural objectivity and progressive ideals. Growth comes through learning that personal relationships enhance rather than limit your ability to serve humanity's evolution.",
            'Pisces': "Your challenge is developing boundaries and practical skills while maintaining your natural compassion and spiritual sensitivity. Growth comes through learning that taking care of yourself enables you to serve others more effectively."
        }
        
        return {
            'title': 'Life Challenges & Growth Opportunities',
            'sections': {
                'primary_challenge': {
                    'heading': f'Your {sun_sign} Growth Edge',
                    'content': growth_challenges.get(sun_sign, f"Your {sun_sign} nature brings both gifts and growth opportunities as you develop your highest potential.")
                },
                'integration_wisdom': {
                    'heading': 'Path to Wholeness',
                    'content': f"Your spiritual evolution involves integrating your {sun_sign} strengths with the lessons that challenge you to grow. Each difficulty you master becomes a source of wisdom you can share with others facing similar challenges."
                }
            }
        }
    
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
                        
                        # Enhanced aspect interpretations
                        aspect_meaning = self._get_aspect_meaning(planet1, planet2, aspect_name, planetary_data)
                        
                        aspects.append({
                            'planet1': planetary_data[planet1]['name'],
                            'planet2': planetary_data[planet2]['name'],
                            'aspect': aspect_name,
                            'orb': orb_difference,
                            'strength': strength,
                            'description': aspect_meaning,
                            'precision': 'enhanced' if self.precision_mode == 'ENHANCED' else 'standard'
                        })
        
        return aspects
    
    def _get_aspect_meaning(self, planet1, planet2, aspect, planetary_data):
        """Generate meaningful aspect interpretations"""
        p1_name = planetary_data[planet1]['name']
        p2_name = planetary_data[planet2]['name']
        
        aspect_meanings = {
            'conjunction': f"{p1_name} and {p2_name} work together harmoniously, blending their energies for unified expression",
            'opposition': f"{p1_name} and {p2_name} create dynamic tension that requires balance and integration", 
            'trine': f"{p1_name} and {p2_name} flow together naturally, creating easy expression and natural talent",
            'square': f"{p1_name} and {p2_name} create productive tension that motivates growth and achievement",
            'sextile': f"{p1_name} and {p2_name} support each other, creating opportunities for positive development"
        }
        
        return aspect_meanings.get(aspect, f"{p1_name} {aspect} {p2_name} creates meaningful interaction between these planetary energies")
    
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
                        aspect_meaning = self._get_aspect_meaning(planet1, planet2, aspect_name, planetary_data)
                        
                        aspects.append({
                            'planet1': planetary_data[planet1]['name'],
                            'planet2': planetary_data[planet2]['name'],
                            'aspect': aspect_name,
                            'orb': abs(separation - exact_angle),
                            'description': aspect_meaning,
                            'precision': 'standard'
                        })
        
        return aspects
    
    def get_transit_predictions(self, birth_chart, prediction_date):
        """Generate enhanced transit predictions with detailed insights"""
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
                
                # Enhanced predictions with practical guidance
                predictions.extend([
                    {
                        'type': 'solar',
                        'description': f"Solar Energy in {sun_sign}",
                        'interpretation': self._get_solar_transit_meaning(sun_sign),
                        'strength': 'strong',
                        'precision': 'enhanced'
                    },
                    {
                        'type': 'lunar', 
                        'description': f"Lunar Energy in {moon_sign}",
                        'interpretation': self._get_lunar_transit_meaning(moon_sign),
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
                        'description': f"Solar Energy in {current_sun_sign}",
                        'interpretation': self._get_solar_transit_meaning(current_sun_sign),
                        'strength': 'moderate',
                        'precision': 'standard'
                    },
                    {
                        'type': 'lunar',
                        'description': f"Lunar Energy in {current_moon_sign}",
                        'interpretation': self._get_lunar_transit_meaning(current_moon_sign),
                        'strength': 'moderate',
                        'precision': 'standard'
                    }
                ])
            
        except Exception as e:
            predictions.append({
                'type': 'error',
                'description': 'Current cosmic energies are being calculated',
                'interpretation': 'The universe\'s current influences are being processed. Please try again in a moment.',
                'precision': 'calculating'
            })
        
        return predictions
    
    def _get_solar_transit_meaning(self, sign):
        """Get meaningful solar transit interpretations"""
        solar_meanings = {
            'Aries': "This is an excellent time for new beginnings and bold initiatives. Your energy is high and you're inspired to lead and pioneer new projects. Take action on ideas you've been considering.",
            'Taurus': "Focus on building stability and enjoying life's pleasures. This is a time for steady progress, financial planning, and appreciating beauty. Slow and steady wins the race now.",
            'Gemini': "Communication and learning are highlighted. This is perfect for networking, writing, teaching, or exploring new ideas. Your curiosity leads to valuable connections and insights.",
            'Cancer': "Family, home, and emotional connections take priority. This is an ideal time for nurturing relationships, creating comfortable spaces, and honoring your feelings and intuition.",
            'Leo': "Creativity and self-expression are emphasized. This is your time to shine, showcase talents, and lead with confidence. Romance and entertainment bring joy and fulfillment.",
            'Virgo': "Organization and improvement are key themes. Focus on health, work efficiency, and attention to detail. This is perfect for decluttering both physical and mental spaces.",
            'Libra': "Relationships and harmony are highlighted. This is ideal for partnership decisions, aesthetic projects, and creating balance in all areas of life. Diplomacy serves you well.",
            'Scorpio': "Transformation and deep insights are emphasized. This is a powerful time for psychological work, research, and releasing what no longer serves you. Trust your intuition.",
            'Sagittarius': "Adventure and expansion call to you. This is perfect for travel, higher learning, and exploring new philosophies. Your optimism attracts exciting opportunities.",
            'Capricorn': "Career and long-term goals are highlighted. This is excellent for professional advancement, building authority, and taking on greater responsibilities with confidence.",
            'Aquarius': "Innovation and social causes are emphasized. This is ideal for group projects, humanitarian work, and implementing progressive ideas that benefit everyone.",
            'Pisces': "Spirituality and creativity flow strongly. This is perfect for artistic projects, meditation, and compassionate service. Trust your dreams and intuitive guidance."
        }
        
        return solar_meanings.get(sign, f"The Sun in {sign} brings opportunities for growth and self-expression aligned with {sign} themes.")
    
    def _get_lunar_transit_meaning(self, sign):
        """Get meaningful lunar transit interpretations"""
        lunar_meanings = {
            'Aries': "Your emotions are direct and energized. This is a good time to act on feelings and express yourself honestly. Quick emotional responses serve you well now.",
            'Taurus': "Emotional stability and comfort are important. Focus on activities that ground you and bring peace. Trust your practical instincts and enjoy simple pleasures.",
            'Gemini': "Your mind is emotionally engaged and curious. This is perfect for meaningful conversations and learning about topics that interest you emotionally.",
            'Cancer': "Your intuition and emotional sensitivity are heightened. This is ideal for family time, home activities, and trusting your feelings about people and situations.",
            'Leo': "Your heart is open and generous. This is perfect for creative expression, romance, and activities that make you feel appreciated and valued.",
            'Virgo': "Your emotional focus is on practical matters and service. This is good for organizing your feelings and taking care of health and daily routines.",
            'Libra': "Emotional harmony and beauty are important to you now. Focus on relationships and creating peaceful, aesthetically pleasing environments.",
            'Scorpio': "Your emotions run deep and transformative. This is powerful for emotional healing, research, and connecting with your psychological depths.",
            'Sagittarius': "Your emotions seek adventure and meaning. This is perfect for exploring new perspectives and activities that expand your emotional understanding of the world.",
            'Capricorn': "Your emotions are practical and goal-oriented. This is good for making realistic plans and taking responsibility for your emotional wellbeing.",
            'Aquarius': "Your emotions are progressive and detached. This is ideal for group activities and considering how your feelings connect to larger social issues.",
            'Pisces': "Your emotions are sensitive and compassionate. This is perfect for creative activities, spiritual practices, and helping others with their emotional needs."
        }
        
        return lunar_meanings.get(sign, f"The Moon in {sign} influences your emotional responses and intuitive insights in ways aligned with {sign} qualities.")
            'Sagittarius': "Your emotions seek adventure and meaning. This is perfect for exploring new perspectives
