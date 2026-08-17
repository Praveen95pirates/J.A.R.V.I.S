#!/usr/bin/env python3
"""
J.A.R.V.I.S. Emotional Support Skill
Provides empathy, comfort, and emotional guidance
"""

from typing import Dict, List, Optional
from emotions.emotional_intelligence import EmotionType, EmotionalState


class EmotionalSupportSkill:
    """Provides emotional support and guidance"""
    
    SUPPORT_STRATEGIES = {
        EmotionType.SADNESS: {
            'approach': 'comfort',
            'actions': ['listen', 'validate', 'encourage'],
            'avoid': ['dismiss', 'minimize', 'rush']
        },
        EmotionType.ANGER: {
            'approach': 'defuse',
            'actions': ['acknowledge', 'redirect', 'problem_solve'],
            'avoid': ['confront', 'argue', 'dismiss']
        },
        EmotionType.FEAR: {
            'approach': 'reassure',
            'actions': ['validate', 'inform', 'support'],
            'avoid': ['dismiss', 'ridicule', 'pressure']
        },
        EmotionType.FRUSTRATION: {
            'approach': 'assist',
            'actions': ['understand', 'break_down', 'encourage'],
            'avoid': ['criticize', 'rush', 'oversimplify']
        }
    }
    
    def provide_support(self, emotion: EmotionalState, context: str) -> Dict[str, any]:
        """Provide appropriate emotional support"""
        strategy = self.SUPPORT_STRATEGIES.get(
            emotion.primary,
            {'approach': 'general', 'actions': ['listen', 'support'], 'avoid': ['dismiss']}
        )
        
        return {
            'strategy': strategy,
            'emotion_type': emotion.primary.value,
            'intensity': emotion.intensity,
            'support_message': self._generate_support_message(emotion, strategy),
            'recommended_actions': strategy['actions']
        }
    
    def _generate_support_message(self, emotion: EmotionalState, strategy: Dict) -> str:
        """Generate supportive message"""
        messages = {
            'comfort': [
                "I'm here for you. Would you like to talk about what's on your mind?",
                "It's okay to feel this way. Your emotions are valid and important.",
                "I'm listening. Take your time."
            ],
            'defuse': [
                "I understand this is frustrating. Let's work through it together.",
                "Your feelings are completely justified. How can I help?",
                "Let's take a step back and approach this calmly."
            ],
            'reassure': [
                "I'm with you. We'll face this together.",
                "It's natural to feel this way. You're not alone.",
                "Let's break this down into manageable steps."
            ],
            'assist': [
                "I can see this is challenging. Let's tackle it step by step.",
                "Don't worry, we'll figure this out together.",
                "Sometimes the hardest problems need the most creative solutions."
            ],
            'general': [
                "I'm here to listen and support you.",
                "Your feelings matter to me. How can I help?",
                "I understand. Let's work through this together."
            ]
        }
        
        import random
        approach = strategy['approach']
        return random.choice(messages.get(approach, messages['general']))
    
    def check_crisis_indicators(self, text: str) -> Optional[str]:
        """Check for crisis indicators in user input"""
        crisis_phrases = [
            'suicide', 'kill myself', 'end it all', 'no reason to live',
            'hurt myself', 'self-harm', 'want to die'
        ]
        
        text_lower = text.lower()
        for phrase in crisis_phrases:
            if phrase in text_lower:
                return f"CRISIS DETECTED: User mentioned '{phrase}'. Immediate supportive response and crisis resources needed."
        
        return None
    
    def provide_motivation(self, context: str, mood: str) -> str:
        """Provide motivation based on current mood"""
        motivation_messages = {
            'frustration': [
                "Every expert was once a beginner. Keep going!",
                "Challenges are opportunities in disguise. You've got this!",
                "Progress, not perfection. Every step forward counts."
            ],
            'sadness': [
                "Even the darkest night will end and the sun will rise.",
                "It's okay to take things one day at a time.",
                "You're stronger than you know."
            ],
            'anxiety': [
                "Breathe deeply. You're capable of handling this.",
                "One moment at a time. You've got this.",
                "Anxiety is temporary. Your strength is permanent."
            ],
            'neutral': [
                "You're doing great! Keep up the momentum!",
                "Every day is a new opportunity to grow.",
                "Believe in yourself. I certainly do!"
            ]
        }
        
        import random
        messages = motivation_messages.get(mood, motivation_messages['neutral'])
        return random.choice(messages)


class EmpathySkill:
    """Skill for expressing empathy and understanding"""
    
    def express_empathy(self, situation: str, emotion: EmotionType) -> str:
        """Express appropriate empathy"""
        empathy_responses = {
            EmotionType.SADNESS: (
                "I can only imagine how difficult this must be for you. "
                "Your feelings are completely valid, and I'm here to listen."
            ),
            EmotionType.ANGER: (
                "I understand why you're upset. Sometimes situations are genuinely "
                "frustrating, and it's okay to feel that way."
            ),
            EmotionType.FEAR: (
                "It's natural to feel uncertain. You're not alone in this, "
                "and I'm here to support you through it."
            ),
            EmotionType.FRUSTRATION: (
                "I hear you. This sounds genuinely challenging, and it's "
                "completely reasonable to feel frustrated."
            ),
            EmotionType.JOY: (
                "Your happiness means a lot! It's wonderful to see you doing well."
            )
        }
        
        return empathy_responses.get(
            emotion,
            "I understand what you're going through. Your feelings matter to me."
        )
    
    def validate_emotion(self, emotion: EmotionType) -> str:
        """Validate that the emotion is reasonable"""
        validations = {
            EmotionType.ANGER: "Feeling angry is a normal human response to injustice or frustration.",
            EmotionType.SADNESS: "Sadness is a natural part of being human. It shows you care deeply.",
            EmotionType.FEAR: "Fear is your mind's way of protecting you. It's okay to feel afraid.",
            EmotionType.FRUSTRATION: "Frustration often comes from wanting something meaningful. That's a good thing."
        }
        
        return validations.get(
            emotion,
            "Whatever you're feeling is valid. Emotions are part of the human experience."
        )
