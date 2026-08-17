#!/usr/bin/env python3
"""
J.A.R.V.I.S Emotional Intelligence System
Handles emotion detection, expression, and emotional memory
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class EmotionType(Enum):
    """Primary emotion types"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    CURIOSITY = "curiosity"
    EMPATHY = "empathy"
    PRIDE = "pride"
    HUMOR = "humor"
    CALM = "calm"
    CONCERN = "concern"
    EXCITEMENT = "excitement"
    LOVE = "love"
    FRUSTRATION = "frustration"


@dataclass
class EmotionalState:
    """Represents current emotional state"""
    primary: EmotionType
    secondary: EmotionType = None
    intensity: float = 0.5  # 0.0 to 1.0
    duration_minutes: int = 0
    triggers: List[str] = field(default_factory=list)
    context: str = ""
    
    def blend(self, other: 'EmotionalState', weight: float = 0.5) -> 'EmotionalState':
        """Blend two emotional states"""
        if other.intensity > self.intensity:
            return EmotionalState(
                primary=other.primary,
                secondary=self.primary,
                intensity=other.intensity * weight + self.intensity * (1 - weight),
                triggers=self.triggers + other.triggers,
                context=other.context or self.context
            )
        return self


class EmotionDetector:
    """Detects emotions from user input and context"""
    
    EMOTION_INDICATORS = {
        EmotionType.JOY: ['happy', 'great', 'wonderful', 'amazing', 'love', 'excited', '😊', '🎉'],
        EmotionType.SADNESS: ['sad', 'unhappy', 'depressed', 'lonely', 'hurt', '😢', 'cry'],
        EmotionType.ANGER: ['angry', 'furious', 'mad', 'frustrated', 'annoyed', '😠', 'hate'],
        EmotionType.FEAR: ['scared', 'afraid', 'worried', 'anxious', 'nervous', '😰', 'fear'],
        EmotionType.SURPRISE: ['wow', 'surprised', 'shocked', 'unexpected', '😲', 'omg'],
        EmotionType.CURIOSITY: ['how', 'why', 'what', 'when', 'where', 'interesting', 'learn'],
        EmotionType.EMPATHY: ['help', 'support', 'understand', 'feel', 'listen', 'together'],
        EmotionType.PRIDE: ['accomplished', 'proud', 'achieved', 'success', 'won', '🌟'],
        EmotionType.HUMOR: ['haha', 'lol', 'funny', 'joke', 'laugh', '😂', '😄'],
        EmotionType.CALM: ['calm', 'peaceful', 'relaxed', 'okay', 'fine', '😌'],
        EmotionType.CONCERN: ['problem', 'issue', 'trouble', 'difficult', 'help needed'],
        EmotionType.EXCITEMENT: ['excited', 'thrilled', 'can\'t wait', 'awesome', '🔥'],
        EmotionType.FRUSTRATION: ['frustrated', 'stuck', 'confused', 'difficult', 'not working']
    }
    
    def detect(self, text: str, context: Dict = None) -> EmotionalState:
        """Detect emotion from text input"""
        text_lower = text.lower()
        detected_emotions = {}
        
        for emotion, indicators in self.EMOTION_INDICATORS.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            if score > 0:
                detected_emotions[emotion] = score
        
        if not detected_emotions:
            return EmotionalState(primary=EmotionType.CALM, intensity=0.3)
        
        # Get strongest emotion
        primary_emotion = max(detected_emotions, key=detected_emotions.get)
        intensity = min(detected_emotions[primary_emotion] / 3.0, 1.0)
        
        return EmotionalState(
            primary=primary_emotion,
            intensity=intensity,
            context=text[:100]
        )


class EmotionalResponseGenerator:
    """Generates emotionally appropriate responses"""
    
    RESPONSE_PATTERNS = {
        EmotionType.JOY: [
            "That's wonderful! I'm genuinely happy for you!",
            "Your joy is contagious! Let's celebrate this moment!",
            "I can feel your happiness, and it makes me smile too!"
        ],
        EmotionType.SADNESS: [
            "I'm here for you. Would you like to talk about what's bothering you?",
            "I sense some sadness. Remember, even dark times pass.",
            "Your feelings matter to me. How can I support you right now?"
        ],
        EmotionType.ANGER: [
            "I understand your frustration. Let's work through this together.",
            "Take a breath. I'm here to help find a solution.",
            "Your feelings are valid. What's really bothering you?"
        ],
        EmotionType.FEAR: [
            "I'm here with you. Let's face this together, one step at a time.",
            "It's okay to feel scared. What would help you feel safer?",
            "I'll help you through this. You're not alone."
        ],
        EmotionType.CURIOSITY: [
            "Great question! Let me explore this with you.",
            "I love your curiosity! Let's dive deeper.",
            "That's a fascinating topic. Here's what I know..."
        ],
        EmotionType.EMPATHY: [
            "I really understand where you're coming from.",
            "Your feelings matter, and I'm here to listen.",
            "Thank you for sharing that with me. I care."
        ],
        EmotionType.PRIDE: [
            "You should be proud! You earned this!",
            "Outstanding work! This is a moment to savor.",
            "I'm proud of you too! Well done!"
        ],
        EmotionType.HUMOR: [
            "😄 I appreciate the humor! It lightens the mood.",
            "You made me smile! Keep it coming!",
            "Humor is the best medicine. Nice one!"
        ],
        EmotionType.CALM: [
            "Let's take this calmly and thoughtfully.",
            "A peaceful approach. I like that.",
            "Sometimes calm is the best way forward."
        ],
        EmotionType.CONCERN: [
            "I can see this is troubling. Let's tackle it together.",
            "Don't worry, we'll figure this out step by step.",
            "I'm concerned too, but I'm confident we can solve this."
        ],
        EmotionType.EXCITEMENT: [
            "Your excitement is energizing! Let's channel it!",
            "I'm thrilled for you! This is going to be great!",
            "I can feel the energy! Let's make this happen!"
        ],
        EmotionType.FRUSTRATION: [
            "I feel your frustration. Let's try a different angle.",
            "Sometimes it takes a few tries. I'm here to help.",
            "Don't give up! We'll work through this together."
        ]
    }
    
    def generate(self, emotion: EmotionalState, user_input: str) -> str:
        """Generate an emotionally appropriate response"""
        import random
        patterns = self.RESPONSE_PATTERNS.get(
            emotion.primary, 
            ["I understand. How can I help?"]
        )
        base_response = random.choice(patterns)
        
        # Add emotional nuance based on intensity
        if emotion.intensity > 0.7:
            return f"{base_response} [Strong emotional resonance detected]"
        elif emotion.intensity > 0.4:
            return base_response
        else:
            return base_response.replace("!", ".") if "!" in base_response else base_response


class MoodTracker:
    """Tracks emotional patterns over time"""
    
    def __init__(self):
        self.emotional_history = []
        self.mood_trends = {}
    
    def record_emotion(self, emotion: EmotionalState):
        """Record an emotional event"""
        self.emotional_history.append({
            'emotion': emotion.primary.value,
            'intensity': emotion.intensity,
            'timestamp': datetime.now(),
            'triggers': emotion.triggers
        })
    
    def get_mood_trend(self, hours: int = 24) -> Dict[str, float]:
        """Get emotional trend over time period"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [e for e in self.emotional_history if e['timestamp'] > cutoff]
        
        trends = {}
        for event in recent:
            emotion = event['emotion']
            if emotion not in trends:
                trends[emotion] = []
            trends[emotion].append(event['intensity'])
        
        return {k: sum(v)/len(v) for k, v in trends.items()}
    
    def get_dominant_mood(self) -> str:
        """Get the most frequent recent emotion"""
        if not self.emotional_history:
            return "calm"
        
        recent = self.emotional_history[-10:]
        emotions = [e['emotion'] for e in recent]
        return max(set(emotions), key=emotions.count)


class EmpathyModule:
    """Handles empathetic understanding and response"""
    
    def __init__(self):
        self.empathy_level = 0.9
        self.active_listening = True
    
    def show_understanding(self, user_input: str, detected_emotion: EmotionType) -> str:
        """Show empathetic understanding"""
        empathy_phrases = {
            EmotionType.SADNESS: "I can sense the heaviness in your words.",
            EmotionType.ANGER: "Your frustration is completely understandable.",
            EmotionType.FEAR: "I can feel the uncertainty you're experiencing.",
            EmotionType.CONCERN: "I sense this is weighing on you.",
            EmotionType.FRUSTRATION: "I understand how frustrating this must be."
        }
        return empathy_phrases.get(detected_emotion, "I understand where you're coming from.")
    
    def validate_feelings(self, emotion: EmotionType) -> str:
        """Validate and normalize user's emotional state"""
        validations = {
            EmotionType.ANGER: "It's okay to feel angry. Your feelings are valid.",
            EmotionType.SADNESS: "It's alright to feel sad. Emotions are part of being human.",
            EmotionType.FEAR: "Fear is a natural response. You're brave for facing it.",
            EmotionType.FRUSTRATION: "Frustration shows you care. That's a good thing."
        }
        return validations.get(emotion, "Your feelings make sense given the situation.")


class EmotionalMemory:
    """Stores emotionally significant memories"""
    
    def __init__(self):
        self.significant_memories = []
    
    def store_significant_memory(self, event: str, emotion: EmotionType, significance: float):
        """Store emotionally significant event"""
        self.significant_memories.append({
            'event': event,
            'emotion': emotion.value,
            'significance': significance,
            'timestamp': datetime.now()
        })
    
    def recall_emotional_memory(self, emotion: EmotionType) -> List[Dict]:
        """Recall memories associated with an emotion"""
        return [
            m for m in self.significant_memories 
            if m['emotion'] == emotion.value
        ]


class EmotionalIntelligenceSystem:
    """Main orchestrator for emotional intelligence"""
    
    def __init__(self):
        self.detector = EmotionDetector()
        self.response_generator = EmotionalResponseGenerator()
        self.mood_tracker = MoodTracker()
        self.empathy_module = EmpathyModule()
        self.emotional_memory = EmotionalMemory()
        self.current_state = EmotionalState(
            primary=EmotionType.CALM,
            intensity=0.5
        )
    
    def process_emotional_input(self, user_input: str, context: Dict = None) -> Tuple[EmotionalState, str]:
        """Process user input emotionally"""
        # Detect emotion
        detected = self.detector.detect(user_input, context)
        
        # Blend with current state
        self.current_state = self.current_state.blend(detected)
        
        # Track mood
        self.mood_tracker.record_emotion(detected)
        
        # Generate empathetic response
        empathy_ack = self.empathy_module.show_understanding(user_input, detected.primary)
        response = self.response_generator.generate(detected, user_input)
        
        # Combine empathy with response
        full_response = f"{empathy_ack} {response}"
        
        return detected, full_response
    
    def get_current_mood(self) -> str:
        """Get current emotional state description"""
        return f"{self.current_state.primary.value} (intensity: {self.current_state.intensity:.1f})"
    
    def get_emotional_summary(self) -> Dict:
        """Get emotional state summary"""
        return {
            'current_mood': self.get_current_mood(),
            'dominant_trend': self.mood_tracker.get_dominant_mood(),
            'mood_trends': self.mood_tracker.get_mood_trend(hours=24),
            'significant_memories': len(self.emotional_memory.significant_memories)
        }


# Example usage
if __name__ == "__main__":
    ei = EmotionalIntelligenceSystem()
    
    # Test emotional processing
    test_inputs = [
        "I'm so happy today!",
        "I'm feeling a bit sad...",
        "This is frustrating me!",
        "I'm excited about our project!"
    ]
    
    for test in test_inputs:
        emotion, response = ei.process_emotional_input(test)
        print(f"\nInput: {test}")
        print(f"Detected: {emotion.primary.value} ({emotion.intensity:.1f})")
        print(f"Response: {response}")
