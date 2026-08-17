#!/usr/bin/env python3
"""
J.A.R.V.I.S - Just A Rather Very Intelligent System
Main Entry Point with Voice, Skills, and Cross-Platform Support
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.jarvis_core import JARVISCore
from core.personality import PersonalitySystem
from emotions.emotional_intelligence import EmotionalIntelligenceSystem, EmotionType
from skills.complete_skills_library import create_complete_skills_library
from voice.voice_engine import JARVISVoiceAssistant

# Wake word configuration
WAKE_WORD = "jarvis"
WAKE_WORD_VARIANTS = ["jarvis", "hey jarvis", "ok jarvis", "jarvis please"]

# Wake word configuration
WAKE_WORD = "jarvis"
WAKE_WORD_VARIANTS = ["jarvis", "hey jarvis", "ok jarvis", "jarvis please"]


def print_banner():
    """Print J.A.R.V.I.S. banner with voice indicator"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ██╗ █████╗ ██████╗ ██╗   ██╗██╗██████╗                ║
    ║   ██║██╔══██╗██╔══██╗██║   ██║██║██╔══██╗               ║
    ║   ██║███████║██████╔╝██║   ██║██║██║  ██║               ║
    ║   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║██║  ██║               ║
    ║   ██║██║  ██║██████╔╝ ╚████╔╝ ██║██████╔╝               ║
    ║   ╚═╝╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝╚════╝                ║
    ║                                                           ║
    ║        Just A Rather Very Intelligent System              ║
    ║                    v1.0.0                                 ║
    ║                                                           ║
    ║   Voice: ON | Skills: ALL | Emotion: ACTIVE              ║
    ║                                                           ║
    ║   Type 'help' for commands, 'exit' to quit                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print available commands"""
    help_text = """
    Available Commands:
    -------------------
    help          - Show this help message
    status        - Show system status and current mood
    skills        - List all available skills
    mood          - Check current emotional state
    history       - Show recent emotional history
    memory        - Show system memory status
    personality   - Show personality profile
    voice on      - Enable voice mode
    voice off     - Disable voice mode
    speak         - Test voice output
    listen        - Test voice input
    web           - Start web interface
    android       - Show Android connection info
    clear         - Clear screen
    exit/quit     - Shut down J.A.R.V.I.S.

    Or just chat naturally - I'll understand and respond with emotion! :)
    """
    print(help_text)


class JARVISInterface:
    """User interface for J.A.R.V.I.S."""
    
    def __init__(self):
        self.core = JARVISCore()
        self.personality_system = PersonalitySystem()
        self.emotional_system = EmotionalIntelligenceSystem()
        self.skills_registry = create_complete_skills_library()
        self.voice = JARVISVoiceAssistant()
        self.running = False
        self.web_mode = False
    
    def start(self):
        """Start the interactive interface"""
        self.running = True
        print_banner()
        print(self.personality_system.get_greeting())
        
        # Greet with voice
        self.voice.say("Hello, I am JARVIS. Just A Rather Very Intelligent System. How may I help you?")
        
        print()
        
        while self.running:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit', 'shutdown']:
                    self.shutdown()
                    break
                elif user_input.lower() == 'help':
                    print_help()
                elif user_input.lower() == 'status':
                    self.show_status()
                elif user_input.lower() == 'skills':
                    self.show_skills()
                elif user_input.lower() == 'mood':
                    self.show_mood()
                elif user_input.lower() == 'history':
                    self.show_emotional_history()
                elif user_input.lower() == 'memory':
                    self.show_memory_status()
                elif user_input.lower() == 'personality':
                    self.show_personality()
                elif user_input.lower() == 'voice on':
                    self.voice.start_voice_mode(self.handle_voice_command)
                    print("Voice mode activated. Say 'JARVIS' to wake me.")
                elif user_input.lower() == 'voice off':
                    self.voice.stop_voice_mode()
                    print("Voice mode deactivated.")
                elif user_input.lower() == 'speak':
                    text = input("Enter text to speak: ")
                    self.voice.say(text)
                elif user_input.lower() == 'listen':
                    print("Listening...")
                    text = self.voice.listen()
                    if text:
                        print(f"You said: {text}")
                        self.voice.say(f"You said: {text}")
                elif user_input.lower() == 'web':
                    self.start_web_interface()
                elif user_input.lower() == 'android':
                    self.show_android_info()
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner()
                else:
                    # Normal conversation
                    self.chat(user_input)
                    
            except KeyboardInterrupt:
                print("\n\nInterrupt detected. Type 'exit' to quit safely.")
            except Exception as e:
                print(f"\n[Error] {e}")
                print("I apologize for the inconvenience. Let's try again.")
    
    def handle_voice_command(self, text: str) -> str:
        """Handle voice command"""
        print(f"\nVoice: {text}")
        
        if text.lower() in ['exit', 'quit', 'shutdown']:
            self.shutdown()
            return "Goodbye."
        
        # Process through emotional system
        emotion, emotional_response = self.emotional_system.process_emotional_input(text)
        
        # Process through core
        response = self.core.process_input(text)
        
        return response
    
    def chat(self, user_input: str):
        """Process a chat message"""
        # Process through emotional system
        emotion, emotional_response = self.emotional_system.process_emotional_input(
            user_input
        )
        
        # Process through core
        response = self.core.process_input(user_input)
        
        # Output response
        print(f"\nJ.A.R.V.I.S.: {response}")
        
        # Speak response
        self.voice.say(response)
        
        # Show emotional state occasionally
        if emotion.intensity > 0.6:
            mood = emotion.primary.value
            print(f"  [Expressing {mood} at {emotion.intensity:.0%} intensity]")
    
    def show_status(self):
        """Show system status"""
        print("\n=== J.A.R.V.I.S. System Status ===")
        print(f"Name: {self.personality_system.profile.name}")
        print(f"Version: 1.0.0")
        print(f"Status: {'Active' if self.running else 'Offline'}")
        print(f"Current Mood: {self.emotional_system.get_current_mood()}")
        print(f"Voice: {'ON' if self.voice.tts_backend else 'OFF'}")
        
        summary = self.emotional_system.get_emotional_summary()
        print(f"Dominant Trend: {summary['dominant_trend']}")
        print(f"Skills Loaded: {len(self.skills_registry.list_enabled())}")
    
    def show_skills(self):
        """Show available skills"""
        print("\n=== J.A.R.V.I.S. Skills ===")
        summary = self.skills_registry.get_summary()
        
        total = 0
        enabled = 0
        
        for category, info in summary.items():
            print(f"\n{category.upper()}")
            for skill in info['skills']:
                status = "✓" if skill in [s.name for s in self.skills_registry.list_enabled()] else "✗"
                print(f"  {status} {skill}")
                total += 1
                if status == "✓":
                    enabled += 1
        
        print(f"\nTotal: {total} skills, {enabled} enabled")
    
    def show_mood(self):
        """Show current mood and trends"""
        print("\n=== Emotional State ===")
        print(f"Current: {self.emotional_system.get_current_mood()}")
        
        trends = self.emotional_system.mood_tracker.get_mood_trend(hours=24)
        if trends:
            print("\n24-hour trends:")
            for emotion, avg_intensity in sorted(trends.items(), key=lambda x: x[1], reverse=True):
                bar = "█" * int(avg_intensity * 10)
                print(f"  {emotion:15s} {bar} ({avg_intensity:.2f})")
    
    def show_emotional_history(self):
        """Show recent emotional history"""
        history = self.emotional_system.mood_tracker.emotional_history[-10:]
        
        if not history:
            print("\nNo emotional history yet.")
            return
        
        print("\n=== Recent Emotional History ===")
        for i, event in enumerate(history, 1):
            timestamp = event.get('timestamp', 'N/A')
            emotion = event['emotion']
            intensity = event['intensity']
            print(f"{i}. {emotion:15s} ({intensity:.2f}) - {timestamp}")
    
    def show_memory_status(self):
        """Show memory system status"""
        print("\n=== Memory System ===")
        print(f"Short-term memories: {len(self.core.memory.short_term)}")
        print(f"Long-term memories: {len(self.core.memory.long_term)}")
        print(f"Emotional memories: {len(self.core.memory.emotional_memory.significant_memories)}")
    
    def show_personality(self):
        """Show personality profile"""
        print("\n=== Personality Profile ===")
        summary = self.personality_system.get_personality_summary()
        
        print(f"\nName: {summary['name']}")
        print(f"Full Name: {summary['full_name']}")
        
        print("\nTraits:")
        for trait, value in summary['traits'].items():
            bar = "█" * int(value * 10)
            print(f"  {trait:15s} {bar} ({value:.2f})")
        
        print("\nCommunication Style:")
        print(f"  Tone: {summary['style']['tone']}")
        print(f"  Formality: {summary['style']['formality']:.1f}")
        print(f"  Verbosity: {summary['style']['verbosity']}")
    
    def show_android_info(self):
        """Show Android connection information"""
        import socket
        
        # Get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "localhost"
        
        print("\n=== Android Connection ===")
        print(f"\n1. Make sure your phone and PC are on the same WiFi network")
        print(f"\n2. Start web interface: python web/web_interface.py")
        print(f"\n3. On Android browser, go to:")
        print(f"   http://{local_ip}:5000")
        print(f"\n4. Or use the JARVIS Android app:")
        print(f"   Download from: [Build Android APK]")
        print(f"\nFeatures available on Android:")
        print(f"  - Voice commands")
        print(f"  - Text chat")
        print(f"  - All skills")
        print(f"  - Real-time status")
    
    def start_web_interface(self):
        """Start web interface"""
        print("\nStarting web interface...")
        print("Android users can connect via http://YOUR_PC_IP:5000")
        
        try:
            from web.web_interface import WebJARVIS
            web = WebJARVIS()
            web.run()
        except Exception as e:
            print(f"Error starting web interface: {e}")
    
    def shutdown(self):
        """Shutdown J.A.R.V.I.S."""
        print("\nInitiating shutdown sequence...")
        self.voice.say("Shutting down. Goodbye!")
        time.sleep(1)
        print("Thank you for using J.A.R.V.I.S. Goodbye!")
        self.running = False


def main():
    """Main entry point"""
    import time
    
    try:
        interface = JARVISInterface()
        interface.start()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
