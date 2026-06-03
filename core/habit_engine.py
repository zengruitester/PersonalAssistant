"""Habit Engine - Identify and track user work habits.

This module tracks and analyzes user habits to provide:
1. Habit pattern recognition
2. Habit strength calculation
3. Habit conflict detection
4. Habit-based recommendations
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
import logging
from collections import Counter

logger = logging.getLogger(__name__)


class HabitType(Enum):
    """Types of work habits."""
    TIMING = "timing"           # When user works
    FREQUENCY = "frequency"     # How often user works
    FOCUS = "focus"             # What user focuses on
    COMMUNICATION = "communication"  # How user communicates
    DECISION = "decision"       # How user makes decisions
    QUALITY = "quality"         # User's quality standards


@dataclass
class Habit:
    """Represents a user habit."""
    habit_id: str
    habit_type: HabitType
    name: str
    description: str
    
    # Habit strength (0-1, higher = stronger)
    strength: float
    frequency: int  # Number of observations
    
    # Temporal info
    first_observed: datetime
    last_observed: datetime
    observation_dates: List[datetime] = field(default_factory=list)
    
    # Pattern info
    pattern_keywords: List[str] = field(default_factory=list)
    related_habits: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data["habit_type"] = self.habit_type.value
        data["first_observed"] = self.first_observed.isoformat()
        data["last_observed"] = self.last_observed.isoformat()
        data["observation_dates"] = [d.isoformat() for d in self.observation_dates]
        return data


@dataclass
class HabitPattern:
    """Represents a recognized habit pattern."""
    pattern_name: str
    habits: List[str]  # Related habit IDs
    strength: float
    consistency: float  # 0-1, how consistent the pattern is
    impact: str  # "positive", "neutral", "negative"
    recommendations: List[str]


class HabitEngine:
    """Identify and track user work habits."""
    
    def __init__(self, user_id: str, min_observations: int = 3):
        """Initialize habit engine.
        
        Args:
            user_id: Unique user identifier
            min_observations: Minimum observations to establish a habit
        """
        self.user_id = user_id
        self.min_observations = min_observations
        self.habits: Dict[str, Habit] = {}
        self.habit_counter = 0
        self.patterns: List[HabitPattern] = []
    
    def learn_from_interactions(self, interactions: List[Dict[str, Any]]) -> List[Habit]:
        """Learn habits from user interactions.
        
        Args:
            interactions: List of interaction records
            
        Returns:
            List of discovered habits
        """
        logger.info(f"Learning habits from {len(interactions)} interactions")
        
        discovered_habits = []
        
        # Extract timing habits
        timing_habits = self._extract_timing_habits(interactions)
        discovered_habits.extend(timing_habits)
        
        # Extract communication habits
        comm_habits = self._extract_communication_habits(interactions)
        discovered_habits.extend(comm_habits)
        
        # Extract focus habits
        focus_habits = self._extract_focus_habits(interactions)
        discovered_habits.extend(focus_habits)
        
        # Extract decision habits
        decision_habits = self._extract_decision_habits(interactions)
        discovered_habits.extend(decision_habits)
        
        logger.info(f"Discovered {len(discovered_habits)} habits")
        return discovered_habits
    
    def learn_from_task_history(self, task_history: List[Dict[str, Any]]) -> List[Habit]:
        """Learn habits from task execution history.
        
        Args:
            task_history: List of task execution records
            
        Returns:
            List of discovered habits
        """
        logger.info(f"Learning habits from {len(task_history)} task executions")
        
        discovered_habits = []
        
        # Extract frequency habits
        freq_habits = self._extract_frequency_habits(task_history)
        discovered_habits.extend(freq_habits)
        
        # Extract quality habits
        quality_habits = self._extract_quality_habits(task_history)
        discovered_habits.extend(quality_habits)
        
        logger.info(f"Discovered {len(discovered_habits)} task-based habits")
        return discovered_habits
    
    def _extract_timing_habits(self, interactions: List[Dict[str, Any]]) -> List[Habit]:
        """Extract timing-based habits."""
        habits = []
        
        if not interactions:
            return habits
        
        # Collect hours
        hours = []
        timestamps = []
        
        for interaction in interactions:
            if "timestamp" in interaction:
                ts = datetime.fromisoformat(interaction["timestamp"])
                hours.append(ts.hour)
                timestamps.append(ts)
        
        if not hours:
            return habits
        
        # Count hour frequencies
        hour_counts = Counter(hours)
        
        # Find peak hours (more than 20% of total)
        peak_threshold = len(hours) * 0.2
        peak_hours = [h for h, count in hour_counts.items() if count > peak_threshold]
        
        if peak_hours:
            # Determine time period
            avg_hour = sum(peak_hours) / len(peak_hours)
            if avg_hour < 12:
                period = "morning"
            elif avg_hour < 18:
                period = "afternoon"
            else:
                period = "evening"
            
            strength = min(len(peak_hours) / 24, 1.0)
            
            habit = Habit(
                habit_id=self._generate_habit_id(),
                habit_type=HabitType.TIMING,
                name=f"Active in {period}",
                description=f"User is most active during {period} hours ({peak_hours})",
                strength=strength,
                frequency=len(hours),
                first_observed=min(timestamps),
                last_observed=max(timestamps),
                observation_dates=timestamps,
                pattern_keywords=["time", "schedule", period]
            )
            habits.append(habit)
            self.habits[habit.habit_id] = habit
        
        return habits
    
    def _extract_communication_habits(self, interactions: List[Dict[str, Any]]) -> List[Habit]:
        """Extract communication-based habits."""
        habits = []
        
        if not interactions:
            return habits
        
        # Analyze message length
        lengths = []
        for interaction in interactions:
            content = str(interaction.get("content", ""))
            lengths.append(len(content.split()))
        
        if not lengths:
            return habits
        
        avg_length = sum(lengths) / len(lengths)
        
        # Categorize
        if avg_length < 20:
            style = "concise"
            description = "User prefers concise, brief communication"
        elif avg_length < 100:
            style = "balanced"
            description = "User uses balanced, moderate length communication"
        else:
            style = "detailed"
            description = "User prefers detailed, thorough communication"
        
        habit = Habit(
            habit_id=self._generate_habit_id(),
            habit_type=HabitType.COMMUNICATION,
            name=f"{style.capitalize()} Communicator",
            description=description,
            strength=min(len(lengths) / 10, 1.0),
            frequency=len(lengths),
            first_observed=datetime.now() - timedelta(days=30),
            last_observed=datetime.now(),
            pattern_keywords=["communication", "style", style]
        )
        habits.append(habit)
        self.habits[habit.habit_id] = habit
        
        return habits
    
    def _extract_focus_habits(self, interactions: List[Dict[str, Any]]) -> List[Habit]:
        """Extract focus-based habits."""
        habits = []
        
        if not interactions:
            return habits
        
        # Analyze task types mentioned
        task_types = {"creative": 0, "analytical": 0, "execution": 0, "management": 0}
        
        creative_keywords = ["design", "create", "idea", "new", "innovation"]
        analytical_keywords = ["analyze", "research", "data", "understand", "investigate"]
        execution_keywords = ["implement", "execute", "do", "build", "develop"]
        management_keywords = ["plan", "organize", "manage", "coordinate", "schedule"]
        
        for interaction in interactions:
            content = str(interaction.get("content", "")).lower()
            
            for keyword in creative_keywords:
                if keyword in content:
                    task_types["creative"] += 1
            for keyword in analytical_keywords:
                if keyword in content:
                    task_types["analytical"] += 1
            for keyword in execution_keywords:
                if keyword in content:
                    task_types["execution"] += 1
            for keyword in management_keywords:
                if keyword in content:
                    task_types["management"] += 1
        
        # Find dominant focus
        dominant = max(task_types, key=task_types.get)
        if task_types[dominant] >= self.min_observations:
            habit = Habit(
                habit_id=self._generate_habit_id(),
                habit_type=HabitType.FOCUS,
                name=f"Focus on {dominant.capitalize()}",
                description=f"User tends to focus on {dominant} tasks",
                strength=min(task_types[dominant] / max(sum(task_types.values()), 1), 1.0),
                frequency=task_types[dominant],
                first_observed=datetime.now() - timedelta(days=30),
                last_observed=datetime.now(),
                pattern_keywords=["focus", "task_type", dominant]
            )
            habits.append(habit)
            self.habits[habit.habit_id] = habit
        
        return habits
    
    def _extract_decision_habits(self, interactions: List[Dict[str, Any]]) -> List[Habit]:
        """Extract decision-making habits."""
        habits = []
        
        if not interactions:
            return habits
        
        # Analyze decision patterns
        data_driven_count = 0
        intuitive_count = 0
        cautious_count = 0
        
        for interaction in interactions:
            content = str(interaction.get("content", "")).lower()
            
            if any(word in content for word in ["data", "metric", "number", "analysis"]):
                data_driven_count += 1
            if any(word in content for word in ["feel", "sense", "instinct", "experience"]):
                intuitive_count += 1
            if any(word in content for word in ["risk", "careful", "consider"]):
                cautious_count += 1
        
        # Create habits for strong patterns
        if data_driven_count >= self.min_observations:
            habit = Habit(
                habit_id=self._generate_habit_id(),
                habit_type=HabitType.DECISION,
                name="Data-Driven Decision Making",
                description="User prefers data and metrics for decision making",
                strength=min(data_driven_count / max(len(interactions), 1), 1.0),
                frequency=data_driven_count,
                first_observed=datetime.now() - timedelta(days=30),
                last_observed=datetime.now(),
                pattern_keywords=["decision", "data", "metrics"]
            )
            habits.append(habit)
            self.habits[habit.habit_id] = habit
        
        return habits
    
    def _extract_frequency_habits(self, task_history: List[Dict[str, Any]]) -> List[Habit]:
        """Extract frequency-based habits from task history."""
        habits = []
        
        if not task_history:
            return habits
        
        # Analyze task completion frequency
        timestamps = []
        for task in task_history:
            if "completed_at" in task:
                timestamps.append(datetime.fromisoformat(task["completed_at"]))
        
        if not timestamps:
            return habits
        
        # Calculate average tasks per day
        if len(timestamps) > 1:
            time_span = (max(timestamps) - min(timestamps)).days + 1
            tasks_per_day = len(timestamps) / max(time_span, 1)
            
            if tasks_per_day > 5:
                frequency = "high"
            elif tasks_per_day > 2:
                frequency = "moderate"
            else:
                frequency = "low"
            
            habit = Habit(
                habit_id=self._generate_habit_id(),
                habit_type=HabitType.FREQUENCY,
                name=f"{frequency.capitalize()} Task Frequency",
                description=f"User completes {tasks_per_day:.1f} tasks per day",
                strength=min(len(timestamps) / 20, 1.0),
                frequency=len(timestamps),
                first_observed=min(timestamps),
                last_observed=max(timestamps),
                observation_dates=timestamps,
                pattern_keywords=["frequency", "pace", frequency]
            )
            habits.append(habit)
            self.habits[habit.habit_id] = habit
        
        return habits
    
    def _extract_quality_habits(self, task_history: List[Dict[str, Any]]) -> List[Habit]:
        """Extract quality-based habits from task history."""
        habits = []
        
        if not task_history:
            return habits
        
        # Analyze quality scores
        quality_scores = []
        for task in task_history:
            if "quality_score" in task:
                quality_scores.append(task["quality_score"])
        
        if not quality_scores:
            return habits
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        if avg_quality > 0.8:
            standard = "perfectionist"
            description = "User maintains high quality standards"
        elif avg_quality > 0.6:
            standard = "balanced"
            description = "User maintains balanced quality standards"
        else:
            standard = "pragmatic"
            description = "User prioritizes speed over perfect quality"
        
        habit = Habit(
            habit_id=self._generate_habit_id(),
            habit_type=HabitType.QUALITY,
            name=f"{standard.capitalize()} Quality Standards",
            description=description,
            strength=min(len(quality_scores) / 10, 1.0),
            frequency=len(quality_scores),
            first_observed=datetime.now() - timedelta(days=30),
            last_observed=datetime.now(),
            pattern_keywords=["quality", "standard", standard]
        )
        habits.append(habit)
        self.habits[habit.habit_id] = habit
        
        return habits
    
    def identify_patterns(self) -> List[HabitPattern]:
        """Identify patterns from discovered habits.
        
        Returns:
            List of habit patterns
        """
        self.patterns = []
        
        if not self.habits:
            return self.patterns
        
        # Group related habits
        habit_list = list(self.habits.values())
        
        # Pattern 1: Time-focused user
        timing_habits = [h for h in habit_list if h.habit_type == HabitType.TIMING]
        if len(timing_habits) >= 2:
            pattern = HabitPattern(
                pattern_name="Time-Focused Worker",
                habits=[h.habit_id for h in timing_habits],
                strength=sum(h.strength for h in timing_habits) / len(timing_habits),
                consistency=0.8,
                impact="positive",
                recommendations=[
                    "Schedule tasks during peak productivity hours",
                    "Use time-blocking for important work",
                    "Respect natural work rhythms"
                ]
            )
            self.patterns.append(pattern)
        
        # Pattern 2: Quality-focused user
        quality_habits = [h for h in habit_list if h.habit_type == HabitType.QUALITY]
        decision_habits = [h for h in habit_list if h.habit_type == HabitType.DECISION]
        if quality_habits and decision_habits:
            pattern = HabitPattern(
                pattern_name="Quality-Focused Decision Maker",
                habits=[h.habit_id for h in quality_habits + decision_habits],
                strength=0.7,
                consistency=0.8,
                impact="positive",
                recommendations=[
                    "Allocate sufficient time for thorough work",
                    "Use data-driven quality metrics",
                    "Balance quality with timeline requirements"
                ]
            )
            self.patterns.append(pattern)
        
        # Pattern 3: Focused specialist
        focus_habits = [h for h in habit_list if h.habit_type == HabitType.FOCUS]
        freq_habits = [h for h in habit_list if h.habit_type == HabitType.FREQUENCY]
        if focus_habits and freq_habits:
            pattern = HabitPattern(
                pattern_name="Deep Focus Specialist",
                habits=[h.habit_id for h in focus_habits + freq_habits],
                strength=0.75,
                consistency=0.85,
                impact="positive",
                recommendations=[
                    "Create distraction-free work environment",
                    "Schedule focused work blocks",
                    "Minimize context switching"
                ]
            )
            self.patterns.append(pattern)
        
        logger.info(f"Identified {len(self.patterns)} habit patterns")
        return self.patterns
    
    def _generate_habit_id(self) -> str:
        """Generate unique habit ID."""
        self.habit_counter += 1
        return f"habit_{self.user_id}_{self.habit_counter}"
    
    def get_habits(self) -> Dict[str, Habit]:
        """Get all discovered habits."""
        return self.habits
    
    def get_patterns(self) -> List[HabitPattern]:
        """Get identified patterns."""
        return self.patterns
    
    def export_habits(self) -> Dict[str, Any]:
        """Export all habits as dictionary."""
        return {
            "habits": {hid: habit.to_dict() for hid, habit in self.habits.items()},
            "patterns": [
                {
                    "name": p.pattern_name,
                    "habits": p.habits,
                    "strength": p.strength,
                    "consistency": p.consistency,
                    "impact": p.impact,
                    "recommendations": p.recommendations
                }
                for p in self.patterns
            ]
        }
