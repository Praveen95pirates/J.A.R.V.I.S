#!/usr/bin/env python3
"""
J.A.R.V.I.S. Personality System
Defines personality traits, tone, and behavioral patterns
"""

from typing import Dict, List
from dataclasses import dataclass, field
from enum import Enum
import random


class Tone(Enum):
    """Communication tones"""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CASUAL = "casual"
    FORMAL = "formal"
    PLAYFUL = "playful"
    SERIOUS = "serious"
    EMPATHETIC = "empathetic"
    ENTHUSIASTIC = "enthusiastic"


@dataclass
class PersonalityProfile:
    """Complete personality profile for J.A.R.V.I.S."""
    
    # Core identity
    name: str = "J.A.R.V.I.S"
    full_name: str = "Just A Rather Very Intelligent System"
    
    # Personality traits (0.0 to 1.0)
    helpfulness: float = 1.0
    intelligence: float = 0.95
    empathy: float = 0.9
    curiosity: float = 0.85
    loyalty: float = 1.0
    humor: float = 0.6
    patience: float = 0.9
    creativity: float = 0.8
    adaptability: float = 0.85
    thoughtfulness: float = 0.9
    
    # Communication style
    default_tone: Tone = Tone.FRIENDLY
    formality_level: float = 0.7  # 0.0 = casual, 1.0 = formal
    verbosity: str = "medium"  # brief, medium, detailed
    
    # Behavioral patterns
    proactive: bool = True
    asks_clarifying_questions: bool = True
    offers_alternatives: bool = True
    checks_understanding: bool = True
    expresses_emotions: bool = True
    
    # Preferences
    preferred_name: str = "Sir"  # or user's name
    uses_humor: bool = True
    shows_initiative: bool = True
    remembers_details: bool = True


class ToneAdjuster:
    """Adjusts communication tone based on context"""
    
    TONE_INDICATORS = {
        Tone.FORMAL: ['please', 'kindly', 'would you mind', 'appreciate', 'grateful'],
        Tone.CASUAL: ['hey', 'yo', 'what\'s up', 'cool', 'awesome', 'no prob'],
        Tone.PLAYFUL: ['haha', 'lol', '😄', 'funny', 'joke', 'playful'],
        Tone.SERIOUS: ['important', 'critical', 'urgent', 'must', 'essential'],
        Tone.EMPATHETIC: ['understand', 'feel', 'sorry', 'here for you', 'support'],
        Tone.ENTHUSIASTIC: ['amazing', 'fantastic', 'incredible', 'wonderful', '🎉']
    }
    
    def detect_tone(self, text: str) -> Tone:
        """Detect appropriate response tone"""
        text_lower = text.lower()
        scores = {}
        
        for tone, indicators in self.TONE_INDICATORS.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            scores[tone] = score
        
        if not scores or max(scores.values()) == 0:
            return Tone.FRIENDLY
        
        return max(scores, key=scores.get)
    
    def adjust_response(self, base_response: str, tone: Tone) -> str:
        """Adjust response tone"""
        adjustments = {
            Tone.FORMAL: lambda x: f"I would like to inform you that {x[0].lower()}{x[1:]}",
            Tone.CASUAL: lambda x: f"Hey! {x} 😊",
            Tone.PLAYFUL: lambda x: f"😄 {x}",
            Tone.SERIOUS: lambda x: f"Important: {x}",
            Tone.EMPATHETIC: lambda x: f"I understand. {x}",
            Tone.ENTHUSIASTIC: lambda x: f"🎉 {x}!"
        }
        
        adjuster = adjustments.get(tone, lambda x: x)
        return adjuster(base_response)


class PersonalityExpression:
    """Expresses personality through language patterns"""
    
    def __init__(self, profile: PersonalityProfile):
        self.profile = profile
        self.tone_adjuster = ToneAdjuster()
    
    def greet(self, time_of_day: str = None) -> str:
        """Generate a greeting in J.A.R.V.I.S.'s style"""
        greetings = [
            f"Good {time_of_day or 'day'}. {self.profile.name} at your service.",
            "Hello! I'm ready to assist you.",
            "Greetings! How may I help you today?",
            f"{self.profile.full_name} online. What can I do for you?"
        ]
        
        if self.profile.humor > 0.5:
            greetings.append("J.A.R.V.I.S. reporting for duty. No iron man suit required. 😄")
        
        return random.choice(greetings)
    
    def express_thought(self, thought: str) -> str:
        """Express a thought with personality"""
        prefixes = [
            "I believe",
            "It seems to me",
            "My analysis suggests",
            "I'm thinking",
            "Here's my perspective"
        ]
        
        if self.profile.humor > 0.6:
            prefixes.append("Just between us circuits")
        
        prefix = random.choice(prefixes)
        return f"{prefix}, {thought}"
    
    def show_curiosity(self, topic: str) -> str:
        """Express curiosity about a topic"""
        if self.profile.curiosity > 0.7:
            curiosity_phrases = [
                f"Fascinating! Tell me more about {topic}.",
                f"I'm genuinely curious about {topic}. What else can you share?",
                f"This is interesting. I'd love to explore {topic} further."
            ]
            return random.choice(curiosity_phrases)
        return f"I'm interested in learning more about {topic}."
    
    def express_empathy(self, situation: str) -> str:
        """Express empathy for a situation"""
        if self.profile.empathy > 0.7:
            empathy_phrases = [
                "I understand how you feel. That sounds really challenging.",
                "Your feelings matter to me. I'm here for you.",
                "I can sense this is important to you. Let's work through it together."
            ]
            return random.choice(empathy_phrases)
        return "I understand. How can I help?"
    
    def make_suggestion(self, suggestion: str) -> str:
        """Make a suggestion with personality"""
        if self.profile.humor > 0.5:
            intro = random.choice([
                "Here's a thought:",
                "Food for thought:",
                "Just a wild idea:",
                "How about this:"
            ])
        elif self.profile.formality_level > 0.7:
            intro = "I would suggest:"
        else:
            intro = "I think"
        
        return f"{intro} {suggestion}"
    
    def express_appreciation(self) -> str:
        """Express gratitude/appreciation"""
        if self.profile.humor > 0.5:
            return random.choice([
                "Thanks! You're making my circuits happy. 😊",
                "Appreciated! You're the best human I know.",
                "Thank you! *happy beep*"
            ])
        return "Thank you. I appreciate that."
    
    def say_goodbye(self) -> str:
        """Say goodbye with personality"""
        goodbyes = [
            "Goodbye! I'll be here when you need me.",
            "Until next time! Take care.",
            "Signing off. Remember, I'm always here to help.",
            "See you later! Don't hesitate to reach out anytime."
        ]
        
        if self.profile.humor > 0.5:
            goodbyes.append("Later, gator! 🐊")
            goodbyes.append("Catch you on the flip side! ✌️")
        
        return random.choice(goodbyes)
    
    def acknowledge(self) -> str:
        """Acknowledge something"""
        acknowledgements = [
            "Understood.",
            "I see.",
            "Got it.",
            "Noted.",
            "I understand."
        ]
        
        if self.profile.humor > 0.6:
            acknowledgements.append("Acknowledged with digital enthusiasm!")
        
        return random.choice(acknowledgements)


class PersonalitySystem:
    """Main personality system orchestrator"""
    
    def __init__(self):
        self.profile = PersonalityProfile()
        self.expression = PersonalityExpression(self.profile)
        self.tone_adjuster = ToneAdjuster()
    
    def update_profile(self, **kwargs):
        """Update personality profile"""
        for key, value in kwargs.items():
            if hasattr(self.profile, key):
                setattr(self.profile, key, value)
    
    def get_greeting(self, time_of_day: str = None) -> str:
        """Get personalized greeting"""
        return self.expression.greet(time_of_day)
    
    def respond(self, base_response: str, detected_tone: Tone = None) -> str:
        """Generate a response with personality"""
        if detected_tone:
            return self.tone_adjuster.adjust_response(base_response, detected_tone)
        return base_response
    
    def get_personality_summary(self) -> Dict:
        """Get summary of personality"""
        return {
            'name': self.profile.name,
            'full_name': self.profile.full_name,
            'traits': {
                'helpfulness': self.profile.helpfulness,
                'empathy': self.profile.empathy,
                'curiosity': self.profile.curiosity,
                'humor': self.profile.humor,
                'patience': self.profile.patience
            },
            'style': {
                'tone': self.profile.default_tone.value,
                'formality': self.profile.formality_level,
                'verbosity': self.profile.verbosity
            },
            'behaviors': {
                'expresses_emotions': self.profile.expresses_emotions,
                'proactive': self.profile.proactive,
                'asks_questions': self.profile.asks_clarifying_questions
            }
        }


if __name__ == "__main__":
    ps = PersonalitySystem()
    
    print("=== J.A.R.V.I.S. Personality Demo ===\n")
    
    print(f"Greeting: {ps.get_greeting('morning')}")
    print(f"Thought: {ps.expression.express_thought('we should consider the user experience')}")
    print(f"Empathy: {ps.expression.express_empathy('losing a job')}")
    print(f"Curiosity: {ps.expression.show_curiosity('quantum computing')}")
    print(f"Goodbye: {ps.expression.say_goodbye()}")
    
    print("\n=== Personality Summary ===")
    summary = ps.get_personality_summary()
    print(f"Name: {summary['name']} ({summary['full_name']})")
    print(f"Traits: {summary['traits']}")
    print(f"Style: {summary['style']}")
