#!/usr/bin/env python3
"""
J.A.R.V.I.S Voice Profile - Iron Man Style
Defines J.A.R.V.I.S. voice characteristics from the films
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class JARVISVoiceProfile:
    """
    J.A.R.V.I.S. voice profile inspired by Iron Man films
    Voice characteristics:
    - British male accent (like Paul Bettany)
    - Calm, measured, sophisticated tone
    - Slightly low-pitched, smooth, refined
    - Professional but with subtle warmth
    - Precise diction, not rushed
    """
    
    # Voice settings
    voice_id: str = "en-GB-RyanNeural"  # British male voice
    
    # Speech characteristics
    rate: int = 160          # Slightly slower than normal for deliberate feel
    pitch: str = "-5Hz"      # Slightly lower than default male
    volume: float = 0.95     # Clear, confident
    
    # Prosody settings for JARVIS-like delivery
    prosody_rate: str = "-5%"     # Slightly slower
    prosody_pitch: str = "-2Hz"   # Lower, more sophisticated
    prosody_volume: str = "+5%"   # Slightly louder for clarity
    
    # Voice style settings (Edge TTS specific)
    style: str = "calm"       # calm, serious, assistant
    style_degree: float = 1.0
    
    # Alternative voices (fallbacks)
    alternative_voices: List[str] = None
    
    def __post_init__(self):
        if self.alternative_voices is None:
            self.alternative_voices = [
                "en-GB-SoniaNeural",   # British female alternative
                "en-US-GuyNeural",     # American male alternative
                "en-GB-ThomasNeural",  # Another British male
            ]
    
    def get_ssml(self, text: str) -> str:
        """Generate SSML for natural-sounding JARVIS voice"""
        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-GB">
    <voice name="{self.voice_id}">
        <prosody rate="{self.prosody_rate}" pitch="{self.prosody_pitch}" volume="{self.prosody_volume}">
            <s>{text}</s>
        </prosody>
    </voice>
</speak>"""
        return ssml
    
    def get_edge_tts_options(self) -> Dict:
        """Get options for Edge TTS"""
        return {
            "voice": self.voice_id,
            "rate": self.prosody_rate,
            "pitch": self.prosody_pitch,
            "volume": self.prosody_volume,
        }


# JARVIS-style phrase templates
JARVIS_PHRASES = {
    "greeting": [
        "Good {time_of_day}. J.A.R.V.I.S. at your service.",
        "Hello. I am J.A.R.V.I.S., your personal assistant.",
        "J.A.R.V.I.S. online. All systems nominal."
    ],
    "acknowledgment": [
        "Understood.",
        "Certainly.",
        "As you wish.",
        "Processing.",
        "Acknowledged."
    ],
    "confirmation": [
        "Done.",
        "Task completed successfully.",
        "I've taken care of it.",
        "Confirmed."
    ],
    "error": [
        "I'm afraid there's been an error. Allow me to investigate.",
        "An anomaly has been detected. I'm analyzing the situation.",
        "Something appears to be wrong. Let me look into it."
    ],
    "thinking": [
        "Processing...",
        "Analyzing...",
        "Computing...",
        "One moment please..."
    ],
    "farewell": [
        "Goodbye. I'll be here when you need me.",
        "Signing off. Take care.",
        "Until next time."
    ]
}

# Word replacements for more formal/JARVIS-like speech
SPEECH_NORMALIZATION = {
    "gonna": "going to",
    "wanna": "want to",
    "kinda": "kind of",
    "sorta": "sort of",
    "gotta": "have to",
    "lemme": "let me",
    "gimme": "give me",
    "dunno": "I don't know",
    "aint": "isn't",
    "cause": "because",
    "yeah": "yes",
    "nope": "no",
    "hey": "hello",
    "yo": "hello",
    "sup": "what's up",
    "btw": "by the way",
    "tbh": "to be honest",
    "idk": "I don't know",
    "omg": "oh my goodness",
    "wtf": "excuse me",
    "lol": "that's amusing",
    "rofl": "that's very amusing",
}


def normalize_text_for_jarvis(text: str) -> str:
    """Normalize text to sound more like JARVIS"""
    words = text.split()
    normalized = [SPEECH_NORMALIZATION.get(w.lower(), w) for w in words]
    return " ".join(normalized)


def get_jarvis_phrase(category: str, **kwargs) -> str:
    """Get a JARVIS-style phrase"""
    import random
    
    phrases = JARVIS_PHRASES.get(category, ["I understand."])
    phrase = random.choice(phrases)
    
    # Format with kwargs
    if kwargs:
        try:
            phrase = phrase.format(**kwargs)
        except KeyError:
            pass
    
    return phrase
