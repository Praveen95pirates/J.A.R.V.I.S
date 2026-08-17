#!/usr/bin/env python3
"""
J.A.R.V.I.S Voice Engine
Provides J.A.R.V.I.S.-style voice synthesis and recognition
"""

import os
import sys
import threading
import queue
import time
from typing import Optional, Callable
from dataclasses import dataclass

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


@dataclass
class VoiceProfile:
    """J.A.R.V.I.S. voice configuration"""
    rate: int = 165           # Slightly slower for calm, deliberate speech
    volume: float = 0.95      # Clear and confident
    pitch: int = 120          # Slightly lower for sophistication
    voice_gender: str = "male"
    accent: str = "british"   # British accent like JARVIS
    tone: str = "professional"
    pause_after_sentence: float = 0.3
    use_tts_backend: str = "edge"  # edge, pyttsx3, or system


class JARVISVoiceEngine:
    """
    J.A.R.V.I.S. voice engine with Iron Man-style voice
    Uses Edge TTS (British male voice) as primary, pyttsx3 as fallback
    """
    
    def __init__(self, profile: VoiceProfile = None):
        self.profile = profile or VoiceProfile()
        self.speaking = False
        self.speech_queue = queue.Queue()
        self.recognition_active = False
        self.recognizer = None
        self.microphone = None
        self.on_speech_start: Optional[Callable] = None
        self.on_speech_end: Optional[Callable] = None
        self.on_speech_recognized: Optional[Callable] = None
        
        self._init_tts()
        self._init_recognition()
    
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        self.tts_engine = None
        self.tts_backend = None
        
        if EDGE_TTS_AVAILABLE and self.profile.use_tts_backend == "edge":
            self.tts_backend = "edge"
            print("[Voice] Edge TTS initialized (British male voice)")
        
        elif PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_pyttsx3()
                self.tts_backend = "pyttsx3"
                print("[Voice] pyttsx3 initialized")
            except Exception as e:
                print(f"[Voice] pyttsx3 init failed: {e}")
        
        if not self.tts_backend:
            print("[Voice] WARNING: No TTS backend available!")
    
    def _configure_pyttsx3(self):
        """Configure pyttsx3 for JARVIS-like voice"""
        if not self.tts_engine:
            return
        
        # Set voice properties
        self.tts_engine.setProperty('rate', self.profile.rate)
        self.tts_engine.setProperty('volume', self.profile.volume)
        
        # Try to find a British male voice
        voices = self.tts_engine.getProperty('voices')
        british_male_voice = None
        
        for voice in voices:
            voice_name = voice.name.lower()
            # Look for British male voices
            if any(name in voice_name for name in ['david', 'daniel', 'james', 'british', 'uk']):
                british_male_voice = voice.id
                break
        
        if british_male_voice:
            self.tts_engine.setProperty('voice', british_male_voice)
        elif voices:
            # Fallback to first available voice
            self.tts_engine.setProperty('voice', voices[0].id)
    
    def _init_recognition(self):
        """Initialize speech recognition"""
        if SR_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
                print("[Voice] Speech recognition initialized")
            except Exception as e:
                print(f"[Voice] Speech recognition init failed: {e}")
    
    async def _speak_edge_tts(self, text: str):
        """Speak using Edge TTS (high quality, British male voice)"""
        if not EDGE_TTS_AVAILABLE:
            return False
        
        try:
            # Use a British male voice
            voice = "en-GB-RyanNeural"  # British male voice
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save("voice/jarvis_speech.mp3")
            
            # Play the audio
            if sys.platform == "win32":
                os.system("start /min voice/jarvis_speech.mp3")
            elif sys.platform == "darwin":
                os.system("afplay voice/jarvis_speech.mp3")
            else:
                os.system("mpg321 voice/jarvis_speech.mp3" if os.system("which mpg321 > /dev/null 2>&1") == 0 else "mpg123 voice/jarvis_speech.mp3")
            
            return True
        except Exception as e:
            print(f"[Voice] Edge TTS error: {e}")
            return False
    
    def _speak_pyttsx3(self, text: str):
        """Speak using pyttsx3 (offline, cross-platform)"""
        if not self.tts_engine:
            return False
        
        try:
            self.speaking = True
            if self.on_speech_start:
                self.on_speech_start(text)
            
            # Break into sentences for more natural speech
            sentences = text.replace('.', '.\n').replace('!', '!\n').replace('?', '?\n')
            
            for sentence in sentences.split('\n'):
                if sentence.strip():
                    self.tts_engine.say(sentence.strip())
                    self.tts_engine.runAndWait()
                    time.sleep(self.profile.pause_after_sentence)
            
            if self.on_speech_end:
                self.on_speech_end()
            
            self.speaking = False
            return True
        except Exception as e:
            print(f"[Voice] pyttsx3 error: {e}")
            self.speaking = False
            return False
    
    def speak(self, text: str, blocking: bool = False):
        """
        Speak text in JARVIS voice
        blocking=True waits for speech to complete
        """
        if not text or not text.strip():
            return
        
        text = text.strip()
        
        if blocking:
            self._speak_sync(text)
        else:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
    
    def _speak_sync(self, text: str):
        """Synchronous speech with fallback"""
        # Try primary backend
        if self.tts_backend == "edge":
            import asyncio
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self._speak_edge_tts(text))
                loop.close()
                if result:
                    return
            except Exception as e:
                print(f"[Voice] Edge TTS fallback: {e}")
        
        # Fallback to pyttsx3
        if self.tts_backend != "pyttsx3" and PYTTSX3_AVAILABLE:
            if not self.tts_engine:
                self.tts_engine = pyttsx3.init()
                self._configure_pyttsx3()
            self.tts_backend = "pyttsx3"
        
        if self.tts_backend == "pyttsx3":
            self._speak_pyttsx3(text)
        else:
            print(f"[J.A.R.V.I.S. Voice]: {text}")
    
    def stop_speaking(self):
        """Stop current speech"""
        self.speaking = False
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input
        Returns recognized text or None
        """
        if not SR_AVAILABLE or not self.recognizer:
            print("[Voice] Speech recognition not available")
            return None
        
        try:
            with sr.Microphone() as source:
                print("[Voice] Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            print("[Voice] Processing speech...")
            text = self.recognizer.recognize_google(audio)
            
            if self.on_speech_recognized:
                self.on_speech_recognized(text)
            
            return text
        except sr.WaitTimeoutError:
            print("[Voice] Listening timeout")
            return None
        except sr.UnknownValueError:
            print("[Voice] Could not understand audio")
            return None
        except Exception as e:
            print(f"[Voice] Recognition error: {e}")
            return None
    
    def start_continuous_listening(self, callback: Callable[[str], None]):
        """Start continuous voice listening mode"""
        self.recognition_active = True
        
        def listen_loop():
            while self.recognition_active:
                text = self.listen(timeout=3, phrase_time_limit=8)
                if text and self.recognition_active:
                    callback(text)
                time.sleep(0.1)
        
        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.recognition_active = False


class JARVISVoiceAssistant:
    """
    High-level voice assistant interface
    Combines speech recognition and synthesis
    """
    
    def __init__(self):
        self.engine = JARVISVoiceEngine()
        self.active = False
        self.wake_word = "jarvis"
    
    def say(self, text: str):
        """Speak text (non-blocking)"""
        # Apply JARVIS-style formatting
        formatted_text = self._format_for_speech(text)
        self.engine.speak(formatted_text)
    
    def say_and_wait(self, text: str):
        """Speak text and wait for completion"""
        formatted_text = self._format_for_speech(text)
        self.engine.speak(formatted_text, blocking=True)
    
    def _format_for_speech(self, text: str) -> str:
        """Format text for natural JARVIS-like speech"""
        # Remove markdown formatting
        text = text.replace('**', '').replace('*', '').replace('#', '')
        text = text.replace('[', '').replace(']', '')
        
        # Ensure proper sentence endings
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def listen_for_command(self) -> Optional[str]:
        """Listen for a single command"""
        return self.engine.listen()
    
    def start_voice_mode(self, command_callback: Callable[[str], str]):
        """Start continuous voice interaction mode"""
        self.active = True
        
        def process_speech(text: str):
            # Check for wake word
            if self.wake_word.lower() in text.lower():
                print(f"[Voice] Wake word detected: {text}")
                self.say("Yes, I'm here.")
            else:
                # Process command
                response = command_callback(text)
                if response:
                    self.say(response)
        
        self.engine.start_continuous_listening(process_speech)
        self.say("Voice mode activated. Say JARVIS to wake me.")
    
    def stop_voice_mode(self):
        """Stop voice mode"""
        self.active = False
        self.engine.stop_listening()
        self.say("Voice mode deactivated.")


# Example usage
if __name__ == "__main__":
    assistant = JARVISVoiceAssistant()
    
    # Test speech
    assistant.say("Hello, I am J.A.R.V.I.S., your personal assistant.")
    time.sleep(2)
    
    # Test listening
    print("Say something...")
    text = assistant.listen_for_command()
    if text:
        print(f"You said: {text}")
        assistant.say(f"You said: {text}")
