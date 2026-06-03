"""Personality Analysis Module - 5-Dimensional Personality Analysis.

This module analyzes user personality across 5 dimensions:
1. Time Management Style (Early bird/Night owl, Procrastinator/Perfectionist)
2. Work Preference (Visual/Auditory/Kinesthetic, Independent/Collaborative)
3. Communication Style (Detailed/Concise, Formal/Casual, Direct/Diplomatic)
4. Decision Style (Data-driven/Intuitive, Cautious/Risk-taking)
5. Output Preference (Text/Table/Chart, Language tone, Detail level)
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TimeManagementStyle(Enum):
    """Time management personality types."""
    EARLY_BIRD = "early_bird"
    NIGHT_OWL = "night_owl"
    FLEXIBLE = "flexible"


class ProcrastinationTendency(Enum):
    """Procrastination vs Perfectionism."""
    PROCRASTINATOR = "procrastinator"
    PERFECTIONIST = "perfectionist"
    BALANCED = "balanced"


class LearningStyle(Enum):
    """Learning style preference."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    MIXED = "mixed"


class CollaborationPreference(Enum):
    """Work collaboration preference."""
    INDEPENDENT = "independent"
    COLLABORATIVE = "collaborative"
    HYBRID = "hybrid"


class CommunicationStyle(Enum):
    """Communication style traits."""
    DETAILED = "detailed"
    CONCISE = "concise"
    FORMAL = "formal"
    CASUAL = "casual"
    DIRECT = "direct"
    DIPLOMATIC = "diplomatic"


class DecisionStyle(Enum):
    """Decision making style."""
    DATA_DRIVEN = "data_driven"
    INTUITIVE = "intuitive"
    CAUTIOUS = "cautious"
    RISK_TAKING = "risk_taking"


class OutputPreference(Enum):
    """Output format preference."""
    TEXT = "text"
    TABLE = "table"
    CHART = "chart"
    MIXED = "mixed"


@dataclass
class PersonalityProfile:
    """User personality profile."""
    user_id: str
    
    # Time Management (Dimension 1)
    time_style: TimeManagementStyle
    procrastination_tendency: ProcrastinationTendency
    time_style_confidence: float  # 0-1
    
    # Work Preference (Dimension 2)
    learning_style: LearningStyle
    collaboration_preference: CollaborationPreference
    preferred_task_types: List[str]  # e.g., ["creative", "analytical", "execution"]
    work_preference_confidence: float
    
    # Communication Style (Dimension 3)
    detail_level: str  # "overview", "detailed", "extremely_detailed"
    communication_tone: str  # "formal", "casual"
    directness: str  # "direct", "diplomatic"
    communication_confidence: float
    
    # Decision Style (Dimension 4)
    decision_approach: DecisionStyle
    decision_risk_level: str  # "cautious", "moderate", "risk_taking"
    decision_confidence: float
    
    # Output Preference (Dimension 5)
    preferred_output_format: OutputPreference
    language_style: str  # "professional", "friendly", "academic", "casual"
    detail_depth: str  # "overview", "detailed", "extremely_detailed"
    output_confidence: float
    
    # Metadata
    last_updated: datetime
    sample_count: int  # Number of interactions used for analysis
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        # Convert enums to strings
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
        return data


class PersonalityAnalyzer:
    """Analyze and track user personality across 5 dimensions."""
    
    def __init__(self, user_id: str, sensitivity: float = 0.8):
        """Initialize personality analyzer.
        
        Args:
            user_id: Unique user identifier
            sensitivity: How sensitive to personality changes (0-1)
        """
        self.user_id = user_id
        self.sensitivity = sensitivity
        self.profile: Optional[PersonalityProfile] = None
        self.interaction_samples: List[Dict[str, Any]] = []
        self.task_execution_samples: List[Dict[str, Any]] = []
        
    def analyze_from_interactions(self, interactions: List[Dict[str, Any]]) -> PersonalityProfile:
        """Analyze personality from user interactions.
        
        Args:
            interactions: List of interaction records
            
        Returns:
            PersonalityProfile object
        """
        self.interaction_samples.extend(interactions)
        logger.info(f"Analyzing {len(interactions)} interactions for user {self.user_id}")
        
        # Analyze each dimension
        time_style = self._analyze_time_management(interactions)
        work_pref = self._analyze_work_preference(interactions)
        comm_style = self._analyze_communication_style(interactions)
        decision_style = self._analyze_decision_style(interactions)
        output_pref = self._analyze_output_preference(interactions)
        
        # Create profile
        self.profile = PersonalityProfile(
            user_id=self.user_id,
            time_style=time_style["style"],
            procrastination_tendency=time_style["tendency"],
            time_style_confidence=time_style["confidence"],
            learning_style=work_pref["learning_style"],
            collaboration_preference=work_pref["collaboration"],
            preferred_task_types=work_pref["task_types"],
            work_preference_confidence=work_pref["confidence"],
            detail_level=comm_style["detail_level"],
            communication_tone=comm_style["tone"],
            directness=comm_style["directness"],
            communication_confidence=comm_style["confidence"],
            decision_approach=decision_style["approach"],
            decision_risk_level=decision_style["risk_level"],
            decision_confidence=decision_style["confidence"],
            preferred_output_format=output_pref["format"],
            language_style=output_pref["language_style"],
            detail_depth=output_pref["detail_depth"],
            output_confidence=output_pref["confidence"],
            last_updated=datetime.now(),
            sample_count=len(interactions),
        )
        
        logger.info(f"Personality profile created with {self.profile.sample_count} samples")
        return self.profile
    
    def analyze_from_task_history(self, task_history: List[Dict[str, Any]]) -> None:
        """Analyze personality from task execution history.
        
        Args:
            task_history: List of task execution records
        """
        self.task_execution_samples.extend(task_history)
        logger.info(f"Analyzing {len(task_history)} task executions")
        
        if self.profile is None:
            logger.warning("No interaction profile created yet")
            return
        
        # Update profile based on task patterns
        self._update_from_task_patterns(task_history)
    
    def _analyze_time_management(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze time management style from interactions."""
        if not interactions:
            return {
                "style": TimeManagementStyle.FLEXIBLE,
                "tendency": ProcrastinationTendency.BALANCED,
                "confidence": 0.0
            }
        
        # Extract timestamps
        hours = []
        for interaction in interactions:
            if "timestamp" in interaction:
                hour = datetime.fromisoformat(interaction["timestamp"]).hour
                hours.append(hour)
        
        if not hours:
            return {
                "style": TimeManagementStyle.FLEXIBLE,
                "tendency": ProcrastinationTendency.BALANCED,
                "confidence": 0.0
            }
        
        # Determine time style
        avg_hour = sum(hours) / len(hours)
        if avg_hour < 12:
            time_style = TimeManagementStyle.EARLY_BIRD
        elif avg_hour > 19:
            time_style = TimeManagementStyle.NIGHT_OWL
        else:
            time_style = TimeManagementStyle.FLEXIBLE
        
        # Analyze procrastination tendency
        # Check deadline responsiveness from interactions
        procrastination_score = self._calculate_procrastination_score(interactions)
        if procrastination_score > 0.6:
            tendency = ProcrastinationTendency.PERFECTIONIST
        elif procrastination_score < 0.4:
            tendency = ProcrastinationTendency.PROCRASTINATOR
        else:
            tendency = ProcrastinationTendency.BALANCED
        
        confidence = min(len(interactions) / 10, 1.0)  # Confidence increases with samples
        
        return {
            "style": time_style,
            "tendency": tendency,
            "confidence": confidence
        }
    
    def _analyze_work_preference(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze work preference style."""
        # Analyze from interaction content types
        learning_styles = {"visual": 0, "auditory": 0, "kinesthetic": 0}
        collaboration_scores = {"independent": 0, "collaborative": 0}
        task_types = {"creative": 0, "analytical": 0, "execution": 0}
        
        for interaction in interactions:
            # Count keywords for learning style
            content = str(interaction.get("content", "")).lower()
            if any(word in content for word in ["show", "display", "see", "visual", "diagram"]):
                learning_styles["visual"] += 1
            if any(word in content for word in ["tell", "discuss", "hear", "say"]):
                learning_styles["auditory"] += 1
            if any(word in content for word in ["do", "try", "practice", "hands"]):
                learning_styles["kinesthetic"] += 1
            
            # Count collaboration preference
            if any(word in content for word in ["i", "my", "alone"]):
                collaboration_scores["independent"] += 1
            if any(word in content for word in ["we", "team", "together"]):
                collaboration_scores["collaborative"] += 1
            
            # Count task type preferences
            if any(word in content for word in ["idea", "new", "design", "create"]):
                task_types["creative"] += 1
            if any(word in content for word in ["analyze", "data", "research"]):
                task_types["analytical"] += 1
            if any(word in content for word in ["execute", "implement", "do"]):
                task_types["execution"] += 1
        
        # Determine dominant styles
        dominant_learning = max(learning_styles, key=learning_styles.get)
        learning_style = LearningStyle[dominant_learning.upper()]
        
        dominant_collab = max(collaboration_scores, key=collaboration_scores.get)
        collaboration = CollaborationPreference[dominant_collab.upper()]
        
        # Sort task types by preference
        preferred_tasks = sorted(task_types.items(), key=lambda x: x[1], reverse=True)
        preferred_task_types = [task[0] for task in preferred_tasks[:2]]
        
        confidence = min(len(interactions) / 10, 1.0)
        
        return {
            "learning_style": learning_style,
            "collaboration": collaboration,
            "task_types": preferred_task_types,
            "confidence": confidence
        }
    
    def _analyze_communication_style(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze communication style preferences."""
        detail_levels = {"overview": 0, "detailed": 0, "extremely_detailed": 0}
        tones = {"formal": 0, "casual": 0}
        directness_scores = {"direct": 0, "diplomatic": 0}
        
        for interaction in interactions:
            content = str(interaction.get("content", ""))
            
            # Analyze detail level from response length
            length = len(content.split())
            if length < 20:
                detail_levels["overview"] += 1
            elif length < 100:
                detail_levels["detailed"] += 1
            else:
                detail_levels["extremely_detailed"] += 1
            
            # Analyze tone
            content_lower = content.lower()
            if any(word in content_lower for word in ["please", "kindly", "would you"]):
                tones["formal"] += 1
            elif any(word in content_lower for word in ["hey", "cool", "awesome"]):
                tones["casual"] += 1
            
            # Analyze directness
            if any(word in content_lower for word in ["need", "must", "require"]):
                directness_scores["direct"] += 1
            else:
                directness_scores["diplomatic"] += 1
        
        dominant_detail = max(detail_levels, key=detail_levels.get)
        dominant_tone = max(tones, key=tones.get)
        dominant_directness = max(directness_scores, key=directness_scores.get)
        
        confidence = min(len(interactions) / 10, 1.0)
        
        return {
            "detail_level": dominant_detail,
            "tone": dominant_tone,
            "directness": dominant_directness,
            "confidence": confidence
        }
    
    def _analyze_decision_style(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze decision making style."""
        decision_keywords = {
            "data_driven": ["data", "metric", "number", "analysis", "research"],
            "intuitive": ["feel", "sense", "instinct", "gut", "experience"],
            "cautious": ["risk", "careful", "consider", "maybe", "might"],
            "risk_taking": ["try", "experiment", "bold", "quick"]
        }
        
        scores = {"data_driven": 0, "intuitive": 0, "cautious": 0, "risk_taking": 0}
        
        for interaction in interactions:
            content = str(interaction.get("content", "")).lower()
            for style, keywords in decision_keywords.items():
                for keyword in keywords:
                    if keyword in content:
                        scores[style] += 1
        
        # Determine approach and risk level
        data_vs_intuitive = (scores["data_driven"], scores["intuitive"])
        approach = DecisionStyle.DATA_DRIVEN if data_vs_intuitive[0] > data_vs_intuitive[1] else DecisionStyle.INTUITIVE
        
        cautious_vs_risk = (scores["cautious"], scores["risk_taking"])
        if cautious_vs_risk[0] > cautious_vs_risk[1]:
            risk_level = "cautious"
        elif cautious_vs_risk[1] > cautious_vs_risk[0]:
            risk_level = "risk_taking"
        else:
            risk_level = "moderate"
        
        confidence = min(len(interactions) / 10, 1.0)
        
        return {
            "approach": approach,
            "risk_level": risk_level,
            "confidence": confidence
        }
    
    def _analyze_output_preference(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze output format preferences."""
        format_preferences = {"text": 0, "table": 0, "chart": 0}
        language_styles = {"professional": 0, "friendly": 0, "academic": 0, "casual": 0}
        detail_depths = {"overview": 0, "detailed": 0, "extremely_detailed": 0}
        
        for interaction in interactions:
            content = str(interaction.get("content", "")).lower()
            
            # Format preference
            if any(word in content for word in ["table", "list", "structured"]):
                format_preferences["table"] += 1
            elif any(word in content for word in ["chart", "graph", "visual", "diagram"]):
                format_preferences["chart"] += 1
            else:
                format_preferences["text"] += 1
            
            # Language style
            if any(word in content for word in ["professional", "formal", "business"]):
                language_styles["professional"] += 1
            elif any(word in content for word in ["friendly", "warm", "casual", "hey"]):
                language_styles["friendly"] += 1
            elif any(word in content for word in ["academic", "research", "technical"]):
                language_styles["academic"] += 1
            else:
                language_styles["casual"] += 1
            
            # Detail depth
            length = len(content.split())
            if length < 50:
                detail_depths["overview"] += 1
            elif length < 200:
                detail_depths["detailed"] += 1
            else:
                detail_depths["extremely_detailed"] += 1
        
        dominant_format = max(format_preferences, key=format_preferences.get)
        dominant_language = max(language_styles, key=language_styles.get)
        dominant_depth = max(detail_depths, key=detail_depths.get)
        
        confidence = min(len(interactions) / 10, 1.0)
        
        return {
            "format": OutputPreference[dominant_format.upper()],
            "language_style": dominant_language,
            "detail_depth": dominant_depth,
            "confidence": confidence
        }
    
    def _calculate_procrastination_score(self, interactions: List[Dict[str, Any]]) -> float:
        """Calculate procrastination tendency from interactions.
        
        Returns: float between 0 (procrastinator) and 1 (perfectionist)
        """
        # Check for phrases indicating thoroughness vs delays
        perfectionist_indicators = 0
        procrastinator_indicators = 0
        
        for interaction in interactions:
            content = str(interaction.get("content", "")).lower()
            
            # Perfectionist indicators
            if any(word in content for word in ["detail", "perfect", "thorough", "quality", "polish"]):
                perfectionist_indicators += 1
            
            # Procrastinator indicators
            if any(word in content for word in ["later", "tomorrow", "rush", "deadline", "quick"]):
                procrastinator_indicators += 1
        
        total = perfectionist_indicators + procrastinator_indicators
        if total == 0:
            return 0.5  # Balanced
        
        return perfectionist_indicators / total
    
    def _update_from_task_patterns(self, task_history: List[Dict[str, Any]]) -> None:
        """Update personality profile based on task execution patterns."""
        if not self.profile or not task_history:
            return
        
        # Analyze completion patterns
        completion_times = []
        quality_scores = []
        
        for task in task_history:
            if "completion_time" in task:
                completion_times.append(task["completion_time"])
            if "quality_score" in task:
                quality_scores.append(task["quality_score"])
        
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            # Adjust procrastination tendency based on quality
            if avg_quality > 0.8:
                self.profile.procrastination_tendency = ProcrastinationTendency.PERFECTIONIST
            elif avg_quality < 0.6:
                self.profile.procrastination_tendency = ProcrastinationTendency.PROCRASTINATOR
        
        # Update sample count
        self.profile.sample_count += len(task_history)
        self.profile.last_updated = datetime.now()
        logger.info(f"Updated personality profile with {len(task_history)} task samples")
    
    def get_profile(self) -> Optional[PersonalityProfile]:
        """Get current personality profile."""
        return self.profile
    
    def export_profile(self) -> Dict[str, Any]:
        """Export personality profile as dictionary."""
        if self.profile is None:
            return {}
        return self.profile.to_dict()
