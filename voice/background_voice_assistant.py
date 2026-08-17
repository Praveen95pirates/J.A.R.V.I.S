#!/usr/bin/env python3
"""
J.A.R.V.I.S. Voice Module - Background Wake Word Detection
Implements always-listening wake word "JARVIS" with speech recognition
"""

import os
import sys
import time
import threading
import queue
import re
from typing import Optional, Callable, List
from dataclasses import dataclass

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    import vosk
    import json as json_module
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False


@dataclass
class WakeWordConfig:
    """Wake word configuration"""
    word: str = "jarvis"
    variants: List[str] = None
    sensitivity: float = 0.7
    active_timeout: float = 5.0  # seconds after wake word to listen for command
    
    def __post_init__(self):
        if self.variants is None:
            self.variants = ["jarvis", "hey jarvis", "ok jarvis", "jarvis please", "hi jarvis"]


class WakeWordDetector:
    """
    Background wake word detection using Vosk for offline recognition
    Falls back to Google Speech Recognition if Vosk is not available
    """
    
    def __init__(self, config: WakeWordConfig = None):
        self.config = config or WakeWordConfig()
        self.listening = False
        self.active = False
        self.recognizer = None
        self.microphone = None
        self.command_callback: Optional[Callable[[str], str]] = None
        self.on_wake_word: Optional[Callable[[], None]] = None
        self.audio_queue = queue.Queue()
        self.worker_thread = None
        
        # Vosk setup
        self.vosk_model = None
        self.vosk_recognizer = None
        
        self._init_recognition()
    
    def _init_recognition(self):
        """Initialize recognition system"""
        if not SR_AVAILABLE:
            print("[WakeWord] SpeechRecognition not available")
            return
        
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 400
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            
            print("[WakeWord] Speech recognition initialized")
        except Exception as e:
            print(f"[WakeWord] Init failed: {e}")
    
    def _init_vosk(self, model_path: str = None):
        """Initialize Vosk for offline wake word detection"""
        if not VOSK_AVAILABLE:
            return False
        
        try:
            if model_path is None:
                # Try to download or use bundled model
                model_path = os.path.join(os.path.dirname(__file__), "vosk-model-small-en-us-0.15")
            
            if os.path.exists(model_path):
                self.vosk_model = vosk.Model(model_path)
                self.vosk_recognizer = vosk.KaldiRecognizer(self.vosk_model, 16000)
                print("[WakeWord] Vosk model loaded for offline recognition")
                return True
        except Exception as e:
            print(f"[WakeWord] Vosk init failed: {e}")
        
        return False
    
    def _check_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        text_lower = text.lower()
        
        # Check for exact wake word or variants
        for variant in self.config.variants:
            if variant in text_lower:
                return True
        
        # Check with fuzzy matching for main word
        if self.config.word in text_lower:
            return True
        
        return False
    
    def _process_audio_chunk(self, audio_data, sample_rate=16000) -> Optional[str]:
        """Process audio chunk and return recognized text"""
        if not self.recognizer:
            return None
        
        try:
            # Try Google recognition first
            audio = sr.AudioData(audio_data, sample_rate, 2)
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            # Fallback to offline recognition if available
            if self.vosk_recognizer:
                try:
                    if self.vosk_recognizer.AcceptWaveform(audio_data):
                        result = json_module.loads(self.vosk_recognizer.Result())
                        return result.get('text', '').lower()
                except:
                    pass
            return None
        except Exception:
            return None
    
    def _listen_loop(self):
        """Main listening loop for wake word detection"""
        print("[WakeWord] Listening loop started")
        
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                while self.listening:
                    try:
                        # Listen for audio
                        audio = self.recognizer.listen(
                            source,
                            timeout=1,
                            phrase_time_limit=3
                        )
                        
                        # Convert to raw audio data
                        raw_data = audio.frame_data
                        sample_rate = audio.sample_rate
                        
                        # Process audio
                        text = self._process_audio_chunk(raw_data, sample_rate)
                        
                        if text:
                            print(f"[WakeWord] Heard: {text}")
                            
                            # Check for wake word
                            if self._check_wake_word(text):
                                print(f"[WakeWord] Wake word detected!")
                                
                                # Remove wake word from text
                                command_text = text
                                for variant in self.config.variants:
                                    command_text = command_text.replace(variant, '')
                                command_text = command_text.strip()
                                
                                # Trigger wake word callback
                                if self.on_wake_word:
                                    self.on_wake_word()
                                
                                # If there's a command after wake word, process it
                                if command_text and self.command_callback:
                                    response = self.command_callback(command_text)
                                    print(f"[WakeWord] Response: {response}")
                                
                                # Continue listening for more commands
                                time.sleep(self.config.active_timeout)
                        
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        print(f"[WakeWord] Loop error: {e}")
                        time.sleep(0.1)
        
        except Exception as e:
            print(f"[WakeWord] Microphone error: {e}")
    
    def start(self, command_callback: Callable[[str], str], on_wake_word: Callable[[], None] = None):
        """
        Start wake word detection in background
        
        Args:
            command_callback: Function to call when command is detected after wake word
            on_wake_word: Optional callback when wake word is detected
        """
        if self.listening:
            return
        
        self.listening = True
        self.command_callback = command_callback
        self.on_wake_word = on_wake_word
        
        self.worker_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.worker_thread.start()
        
        print("[WakeWord] Wake word detection started")
        print(f"[WakeWord] Say '{self.config.word}' to activate J.A.R.V.I.S.")
    
    def stop(self):
        """Stop wake word detection"""
        self.listening = False
        print("[WakeWord] Wake word detection stopped")


class BackgroundVoiceAssistant:
    """
    Background voice assistant with always-on wake word detection
    Runs continuously in background, listens for "JARVIS"
    """
    
    def __init__(self, command_callback: Callable[[str], str] = None):
        self.wake_detector = WakeWordDetector()
        self.command_callback = command_callback
        self.active = False
        self.last_activation = 0
        self.activation_timeout = 10  # seconds
    
    def start(self, command_callback: Callable[[str], str] = None):
        """Start background voice assistant"""
        if self.active:
            return
        
        if command_callback:
            self.command_callback = command_callback
        
        self.active = True
        
        def on_wake():
            self.last_activation = time.time()
            print("[Voice] J.A.R.V.I.S. activated!")
        
        def on_command(text):
            if time.time() - self.last_activation > self.activation_timeout:
                return "Session expired. Say JARVIS again."
            
            if self.command_callback:
                try:
                    return self.command_callback(text)
                except Exception as e:
                    print(f"[Voice] Command error: {e}")
                    return "I encountered an error processing your request."
            return "Command received."
        
        self.wake_detector.start(on_command, on_wake)
        print("[Voice] Background voice assistant started")
    
    def stop(self):
        """Stop background voice assistant"""
        self.active = False
        self.wake_detector.stop()
        print("[Voice] Background voice assistant stopped")


# Example usage
if __name__ == "__main__":
    def handle_command(text):
        print(f"Command received: {text}")
        return f"Processing: {text}"
    
    assistant = BackgroundVoiceAssistant(handle_command)
    assistant.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        assistant.stop()
        print("\nShutting down...")
