"""
Birth Time Rectification Engine
Advanced algorithms for determining accurate birth times using life events
"""

import math
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Tuple

class BirthTimeRectifier:
    """Professional birth time rectification using multiple methods"""
    
    def __init__(self, enhanced_engine):
        self.enhanced_engine = enhanced_engine
        self.confidence_thresholds = {
            'HIGH': 0.85,
            'MEDIUM': 0.65,
            'LOW': 0.45
        }
        
        # Event-planet correlations for validation
        self.event_correlations = {
            'marriage': ['venus', 'jupiter', 'moon'],
            'career': ['sun', 'jupiter', 'saturn', 'mercury'],
            'education': ['jupiter', 'mercury', 'sun'],
            'health': ['sun', 'moon', 'mars'],
            'travel': ['jupiter', 'mercury', 'moon'],
            'property': ['mars', 'saturn', 'moon'],
            'children': ['jupiter', 'sun'],
            'death_family': ['saturn', 'mars'],
            'accident': ['mars', 'saturn'],
            'spiritual': ['jupiter', 'moon']
        }
        
        # Dasha system periods (Vimshottari)
        self.dasha_periods = {
            'sun': 6, 'moon': 10, 'mars': 7, 'rahu': 18,
            'jupiter': 16, 'saturn': 19, 'mercury': 17,
            'ketu': 7, 'venus': 20
        }
        
        # Nakshatra to dasha lord mapping
        self.nakshatra_lords = [
            'ketu', 'venus', 'sun', 'moon', 'mars', 'rahu', 'jupiter',
            'saturn', 'mercury', 'ketu', 'venus', 'sun', 'moon', 'mars',
            'rahu', 'jupiter', 'saturn', 'mercury', 'ketu', 'venus',
            'sun', 'moon', 'mars', 'rahu', 'jupiter', 'saturn', 'mercury'
        ]
    
    def rectify_birth_time(self, birth_data: Dict, life_events: List[Dict], 
                          time_window_hours: int = 4) -> Dict:
        """
        Main rectification method using multiple validation techniques
        
        Args:
            birth_data: Basic birth information (date, approximate time, location)
            life_events: List of significant life events with dates and types
            time_window_hours: Search window in hours around approximate time
            
        Returns:
            Rectification results with confidence scores and recommendations
        """
        
        if not life_events:
            return {
                'success': False,
                'error': 'Life events required for rectification',
                'recommendation': 'Please provide at least 3 significant life events'
            }
        
        # Parse birth data
        birth_date = datetime.strptime(birth_data['date'], '%Y-%m-%d')
        approx_time = birth_data.get('approximate_time', '12:00')
        approx_datetime = datetime.strptime(f"{birth_data['date']} {approx_time}", '%Y-%m-%d %H:%M')
        
        latitude = float(birth_data['latitude'])
        longitude = float(birth_data['longitude'])
        
        # Generate time candidates
        candidates = self._generate_time_candidates(approx_datetime, time_window_hours)
        
        # Score each candidate using multiple methods
        scored_candidates = []
        
        for candidate_time in candidates:
            candidate_jd = self.enhanced_engine.precise_julian_day(candidate_time.replace(tzinfo=timezone.utc))
            
            # Calculate chart for this candidate
            chart = self._calculate_candidate_chart(candidate_jd, latitude, longitude)
            
            # Score using different methods
            scores = {
                'dasha_events': self._score_dasha_events(chart, life_events),
                'transit_timing': self._score_transit_timing(chart, life_events),
                'ascendant_traits': self._score_ascendant_traits(chart, birth_data.get('personality', {})),
                'house_events': self._score_house_events(chart, life_events)
            }
            
            # Calculate composite score
            composite_score = (
                scores['dasha_events'] * 0.35 +
                scores['transit_timing'] * 0.25 +
                scores['ascendant_traits'] * 0.20 +
                scores['house_events'] * 0.20
            )
            
            scored_candidates.append({
                'time': candidate_time,
                'julian_day': candidate_jd,
                'chart': chart,
                'scores': scores,
                'composite_score': composite_score,
                'confidence': self._calculate_confidence(composite_score, scores)
            })
        
        # Sort by composite score
        scored_candidates.sort(key=lambda x: x['composite_score'], reverse=True)
        
        # Get best candidate
        best_candidate = scored_candidates[0]
        
        return {
            'success': True,
            'rectified_time': best_candidate['time'],
            'confidence': best_candidate['confidence'],
            'confidence_score': best_candidate['composite_score'],
            'method_scores': best_candidate['scores'],
            'chart': best_candidate['chart'],
            'alternatives': scored_candidates[1:4],  # Top 3 alternatives
            'total_candidates_tested': len(candidates),
            'recommendations': self._generate_recommendations(best_candidate, scored_candidates)
        }
    
    def _generate_time_candidates(self, approx_time: datetime, window_hours: int) -> List[datetime]:
        """Generate time candidates within the specified window"""
        candidates = []
        
        # High precision: every 2 minutes
        start_time = approx_time - timedelta(hours=window_hours/2)
        end_time = approx_time + timedelta(hours=window_hours/2)
        
        current_time = start_time
        while current_time <= end_time:
            candidates.append(current_time)
            current_time += timedelta(minutes=2)
        
        return candidates
    
    def _calculate_candidate_chart(self, jd: float, latitude: float, longitude: float) -> Dict:
        """Calculate basic chart data for a candidate time"""
        
        # Get enhanced planetary positions
        sun_tropical = self.enhanced_engine.enhanced_sun_longitude(jd)
        moon_tropical = self.enhanced_engine.enhanced_moon_longitude(jd)
        planets_tropical = self.enhanced_engine.enhanced_planetary_positions(jd)
        planets_tropical['sun'] = sun_tropical
        planets_tropical['moon'] = moon_tropical
        
        # Convert to sidereal
        ayanamsa_value = self.enhanced_engine.calculate_ayanamsa(jd, 'LAHIRI')
        
        chart = {
            'julian_day': jd,
            'ayanamsa': ayanamsa_value,
            'planets_sidereal': {},
            'moon_longitude': 0,
            'ascendant': 0
        }
        
        for planet, tropical_lon in planets_tropical.items():
            sidereal_lon = self.enhanced_engine.tropical_to_sidereal(tropical_lon, jd, 'LAHIRI')
            chart['planets_sidereal'][planet] = sidereal_lon
            
            if planet == 'moon':
                chart['moon_longitude'] = sidereal_lon
        
        # Calculate approximate ascendant
        lst = self._calculate_local_sidereal_time(jd, longitude)
        chart['ascendant'] = (lst + latitude/4) % 360  # Simplified ascendant
        
        return chart
    
    def _calculate_local_sidereal_time(self, jd: float, longitude: float) -> float:
        """Calculate Local Sidereal Time"""
        T = (jd - 2451545.0) / 36525.0
        theta0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T**2
        return (theta0 + longitude) % 360
    
    def _score_dasha_events(self, chart: Dict, life_events: List[Dict]) -> float:
        """Score based on dasha period correlations with life events"""
        if not life_events:
            return 0.5
        
        total_score = 0
        event_count = 0
        
        for event in life_events:
            if 'date' not in event or 'type' not in event:
                continue
                
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            event_jd = self.enhanced_engine.precise_julian_day(event_date.replace(tzinfo=timezone.utc))
            
            # Calculate running dasha at event time
            birth_jd = chart['julian_day']
            years_since_birth = (event_jd - birth_jd) / 365.25
            
            running_dasha = self._calculate_running_dasha(chart['moon_longitude'], years_since_birth)
            
            # Score correlation between dasha lord and event type
            event_type = event['type'].lower()
            if event_type in self.event_correlations:
                expected_planets = self.event_correlations[event_type]
                if running_dasha in expected_planets:
                    importance = event.get('importance', 0.7)
                    total_score += 0.8 + importance * 0.2
                else:
                    total_score += 0.3
            else:
                total_score += 0.5
                
            event_count += 1
        
        return total_score / event_count if event_count > 0 else 0.5
    
    def _calculate_running_dasha(self, moon_longitude: float, years_since_birth: float) -> str:
        """Calculate which dasha is running at a given time"""
        
        # Determine birth nakshatra
        nakshatra_number = int(moon_longitude // (360/27))
        nakshatra_position = (moon_longitude % (360/27)) / (360/27)
        
        # Get starting dasha lord
        birth_dasha_lord = self.nakshatra_lords[nakshatra_number]
        birth_dasha_period = self.dasha_periods[birth_dasha_lord]
        
        # Calculate remaining time in birth dasha
        remaining_birth_dasha = birth_dasha_period * (1 - nakshatra_position)
        
        if years_since_birth <= remaining_birth_dasha:
            return birth_dasha_lord
        
        # Calculate which dasha is running
        elapsed_years = years_since_birth - remaining_birth_dasha
        
        # Cycle through dashas
        dasha_lords = list(self.dasha_periods.keys())
        birth_lord_index = dasha_lords.index(birth_dasha_lord)
        
        current_elapsed = 0
        current_index = (birth_lord_index + 1) % len(dasha_lords)
        
        while current_elapsed < elapsed_years:
            current_lord = dasha_lords[current_index]
            period = self.dasha_periods[current_lord]
            
            if current_elapsed + period > elapsed_years:
                return current_lord
                
            current_elapsed += period
            current_index = (current_index + 1) % len(dasha_lords)
        
        return dasha_lords[current_index]
    
    def _score_transit_timing(self, chart: Dict, life_events: List[Dict]) -> float:
        """Score based on transit correlations with life events"""
        if not life_events:
            return 0.5
        
        total_score = 0
        event_count = 0
        
        for event in life_events:
            if 'date' not in event:
                continue
                
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            event_jd = self.enhanced_engine.precise_julian_day(event_date.replace(tzinfo=timezone.utc))
            
            # Calculate transit positions at event time
            transit_jupiter = self.enhanced_engine.enhanced_planetary_positions(event_jd)['jupiter']
            transit_saturn = self.enhanced_engine.enhanced_planetary_positions(event_jd)['saturn']
            
            # Convert to sidereal
            ayanamsa = self.enhanced_engine.calculate_ayanamsa(event_jd, 'LAHIRI')
            transit_jupiter_sidereal = (transit_jupiter - ayanamsa) % 360
            transit_saturn_sidereal = (transit_saturn - ayanamsa) % 360
            
            # Check aspects to natal positions
            aspect_score = 0
            
            # Check Jupiter transits (beneficial events)
            if event['type'].lower() in ['marriage', 'career', 'education', 'children']:
                natal_sun = chart['planets_sidereal']['sun']
                natal_moon = chart['planets_sidereal']['moon']
                ascendant = chart['ascendant']
                
                for natal_point in [natal_sun, natal_moon, ascendant]:
                    if self._is_major_aspect(transit_jupiter_sidereal, natal_point, 2.0):
                        aspect_score += 0.3
            
            # Check Saturn transits (challenging/structural events)
            if event['type'].lower() in ['career', 'health', 'death_family', 'property']:
                natal_sun = chart['planets_sidereal']['sun']
                natal_moon = chart['planets_sidereal']['moon']
                
                for natal_point in [natal_sun, natal_moon]:
                    if self._is_major_aspect(transit_saturn_sidereal, natal_point, 2.0):
                        aspect_score += 0.25
            
            total_score += min(aspect_score, 1.0)
            event_count += 1
        
        return total_score / event_count if event_count > 0 else 0.5
    
    def _score_ascendant_traits(self, chart: Dict, personality: Dict) -> float:
        """Score based on ascendant sign personality correlation"""
        if not personality:
            return 0.5
        
        ascendant_sign = int(chart['ascendant'] // 30)
        
        # Personality traits by ascendant sign
        sign_traits = {
            0: ['energetic', 'impulsive', 'leadership', 'athletic', 'direct'],  # Aries
            1: ['stable', 'practical', 'stubborn', 'artistic', 'patient'],     # Taurus
            2: ['communicative', 'versatile', 'curious', 'restless', 'witty'], # Gemini
            3: ['emotional', 'nurturing', 'moody', 'protective', 'intuitive'], # Cancer
            4: ['confident', 'dramatic', 'generous', 'prideful', 'creative'],  # Leo
            5: ['analytical', 'perfectionist', 'helpful', 'critical', 'precise'], # Virgo
            6: ['diplomatic', 'charming', 'indecisive', 'harmonious', 'social'], # Libra
            7: ['intense', 'mysterious', 'passionate', 'secretive', 'transformative'], # Scorpio
            8: ['adventurous', 'philosophical', 'optimistic', 'direct', 'freedom_loving'], # Sagittarius
            9: ['ambitious', 'disciplined', 'serious', 'responsible', 'structured'], # Capricorn
            10: ['innovative', 'eccentric', 'humanitarian', 'detached', 'progressive'], # Aquarius
            11: ['intuitive', 'dreamy', 'compassionate', 'sensitive', 'artistic']  # Pisces
        }
        
        expected_traits = sign_traits.get(ascendant_sign, [])
        
        match_score = 0
        total_traits = 0
        
        for trait, has_trait in personality.items():
            total_traits += 1
            trait_lower = trait.lower()
            
            if trait_lower in expected_traits:
                match_score += 1 if has_trait else -0.5
            else:
                # Check for opposite traits
                if not has_trait:
                    match_score += 0.2
        
        return max(0, min(1, (match_score / total_traits + 1) / 2)) if total_traits > 0 else 0.5
    
    def _score_house_events(self, chart: Dict, life_events: List[Dict]) -> float:
        """Score based on house activation during life events"""
        if not life_events:
            return 0.5
        
        # This is a simplified house event correlation
        # In a full implementation, you would calculate precise house cusps
        # and check for planetary activations
        
        total_score = 0
        event_count = 0
        
        for event in life_events:
            event_type = event['type'].lower()
            
            # Basic house correlations (simplified)
            house_correlations = {
                'marriage': [7, 1],      # 7th house partnership, 1st house self
                'career': [10, 6],       # 10th house career, 6th house work  
                'education': [5, 9],     # 5th house learning, 9th house higher education
                'children': [5],         # 5th house children
                'health': [6, 8],        # 6th house health, 8th house transformation
                'property': [4],         # 4th house property
                'travel': [9, 3]         # 9th house long travel, 3rd house short travel
            }
            
            if event_type in house_correlations:
                # Assign moderate score for house correlation
                total_score += 0.6
            else:
                total_score += 0.4
                
            event_count += 1
        
        return total_score / event_count if event_count > 0 else 0.5
    
    def _is_major_aspect(self, pos1: float, pos2: float, orb: float) -> bool:
        """Check if two positions form a major aspect within orb"""
        separation = abs(pos1 - pos2)
        if separation > 180:
            separation = 360 - separation
        
        major_aspects = [0, 60, 90, 120, 180]  # Conjunction, sextile, square, trine, opposition
        
        for aspect_angle in major_aspects:
            if abs(separation - aspect_angle) <= orb:
                return True
        
        return False
    
    def _calculate_confidence(self, composite_score: float, method_scores: Dict) -> str:
        """Calculate confidence level based on scores"""
        
        # Check score consistency
        scores_list = list(method_scores.values())
        score_variance = sum((s - composite_score)**2 for s in scores_list) / len(scores_list)
        
        # Adjust confidence based on consistency
        consistency_bonus = 0.1 if score_variance < 0.05 else 0
        adjusted_score = composite_score + consistency_bonus
        
        if adjusted_score >= self.confidence_thresholds['HIGH']:
            return 'HIGH'
        elif adjusted_score >= self.confidence_thresholds['MEDIUM']:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_recommendations(self, best_candidate: Dict, all_candidates: List[Dict]) -> List[str]:
        """Generate recommendations based on rectification results"""
        recommendations = []
        
        confidence = best_candidate['confidence']
        composite_score = best_candidate['composite_score']
        
        if confidence == 'HIGH':
            recommendations.append("High confidence rectification. Time is likely accurate within ±2 minutes.")
        elif confidence == 'MEDIUM':
            recommendations.append("Moderate confidence. Consider additional life events for verification.")
        else:
            recommendations.append("Low confidence. More detailed life events or different approach recommended.")
        
        # Check score distribution
        top_3_scores = [c['composite_score'] for c in all_candidates[:3]]
        score_difference = top_3_scores[0] - top_3_scores[1] if len(top_3_scores) > 1 else 0
        
        if score_difference < 0.1:
            recommendations.append("Multiple times show similar scores. Consider narrower time window.")
        
        # Method-specific recommendations
        method_scores = best_candidate['scores']
        
        if method_scores['dasha_events'] > 0.8:
            recommendations.append("Strong dasha correlation supports this timing.")
        elif method_scores['dasha_events'] < 0.5:
            recommendations.append("Weak dasha correlation. Verify event dates and types.")
        
        if method_scores['transit_timing'] > 0.7:
            recommendations.append("Transit timing supports major life events.")
        
        if method_scores['ascendant_traits'] > 0.8:
            recommendations.append("Personality traits strongly match ascendant sign.")
        elif method_scores['ascendant_traits'] < 0.4:
            recommendations.append("Personality traits don't strongly match. Consider different ascendant.")
        
        return recommendations
