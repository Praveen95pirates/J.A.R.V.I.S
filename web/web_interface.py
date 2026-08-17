#!/usr/bin/env python3
"""
J.A.R.V.I.S Web Interface
Flask-based web interface accessible from any device including Android
"""

import os
import sys
import json
import time
import queue
import threading
from datetime import datetime
from typing import Dict, List, Optional

try:
    from flask import Flask, render_template, request, jsonify, Response, stream_with_context
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jarvis_core import JARVISCore
from core.personality import PersonalitySystem
from emotions.emotional_intelligence import EmotionalIntelligenceSystem
from skills.skills_registry import SkillsRegistry
from voice.voice_engine import JARVISVoiceAssistant
from voice.background_voice_assistant import BackgroundVoiceAssistant
from skills.trading_skills import handle_request as handle_trading_request
from skills.skill_manager import get_skill_manager


class WebJARVIS:
    """J.A.R.V.I.S. web interface"""
    
    def __init__(self, host='0.0.0.0', port=5000):
        if not FLASK_AVAILABLE:
            print("[Web] ERROR: Flask not installed!")
            sys.exit(1)
        
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        
        # Initialize J.A.R.V.I.S. components
        self.core = JARVISCore()
        self.personality = PersonalitySystem()
        self.emotional_system = EmotionalIntelligenceSystem()
        self.skills_registry = SkillsRegistry()
        self.skill_manager = get_skill_manager()
        self.voice = JARVISVoiceAssistant()
        
        # Chat history
        self.chat_history = []
        self.max_history = 100
        
        # Voice mode state
        self.voice_mode_active = False
        
        # Background voice assistant
        self.background_voice = BackgroundVoiceAssistant(command_callback=self._handle_voice_command)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main chat interface"""
            return render_template('index.html')
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            """Handle chat messages"""
            data = request.get_json()
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({'error': 'Empty message'}), 400
            
            # Process through emotional system
            emotion, emotional_response = self.emotional_system.process_emotional_input(
                user_message
            )
            
            # Process through core
            response = self.core.process_input(user_message)
            
            # Store in history
            self.chat_history.append({
                'user': user_message,
                'jarvis': response,
                'emotion': emotion.primary.value,
                'intensity': emotion.intensity,
                'timestamp': datetime.now().isoformat()
            })
            
            # Limit history
            if len(self.chat_history) > self.max_history:
                self.chat_history = self.chat_history[-self.max_history:]
            
            return jsonify({
                'response': response,
                'emotion': emotion.primary.value,
                'intensity': emotion.intensity,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/status')
        def status():
            """Get system status"""
            return jsonify({
                'status': 'online',
                'name': 'J.A.R.V.I.S.',
                'version': '1.0.0',
                'mood': self.emotional_system.get_current_mood(),
                'voice_mode': self.voice_mode_active,
                'skills_count': len(self.skills_registry.list_enabled())
            })
        
        @self.app.route('/api/skills')
        def get_skills():
            """Get all skills"""
            return jsonify(self.skills_registry.get_summary())
        
        @self.app.route('/api/trading/<skill_name>', methods=['POST'])
        def trading_skill(skill_name):
            """Handle trading skill requests"""
            data = request.get_json() or {}
            result = handle_trading_request(skill_name, data)
            return jsonify(result)
        
        @self.app.route('/api/skill-manager/skills', methods=['GET'])
        def list_all_skills():
            """Get all skills with full details"""
            return jsonify(self.skill_manager.get_all_skills())
        
        @self.app.route('/api/skill-manager/enable', methods=['POST'])
        def enable_skill():
            """Enable a skill"""
            data = request.get_json() or {}
            name = data.get('name')
            if not name:
                return jsonify({'error': 'name_required'}), 400
            return jsonify(self.skill_manager.enable_skill(name))
        
        @self.app.route('/api/skill-manager/disable', methods=['POST'])
        def disable_skill():
            """Disable a skill"""
            data = request.get_json() or {}
            name = data.get('name')
            if not name:
                return jsonify({'error': 'name_required'}), 400
            return jsonify(self.skill_manager.disable_skill(name))
        
        @self.app.route('/api/skill-manager/update', methods=['POST'])
        def update_skills():
            """Update skills from remote configuration"""
            data = request.get_json() or {}
            result = self.skill_manager.update_from_remote(data)
            return jsonify(result)
        
        @self.app.route('/api/mood')
        def get_mood():
            """Get current mood and trends"""
            return jsonify({
                'current': self.emotional_system.get_current_mood(),
                'trends': self.emotional_system.mood_tracker.get_mood_trend(hours=24),
                'summary': self.emotional_system.get_emotional_summary()
            })
        
        @self.app.route('/api/history')
        def get_history():
            """Get chat history"""
            return jsonify(self.chat_history)
        
        @self.app.route('/api/voice/speak', methods=['POST'])
        def voice_speak():
            """Speak text"""
            data = request.get_json()
            text = data.get('text', '')
            if text:
                self.voice.say(text)
                return jsonify({'status': 'speaking'})
            return jsonify({'error': 'No text provided'}), 400
        
        @self.app.route('/api/voice/listen', methods=['POST'])
        def voice_listen():
            """Listen for voice input"""
            text = self.voice.listen()
            if text:
                return jsonify({'text': text})
            return jsonify({'text': None, 'error': 'Could not understand'})
        
        @self.app.route('/api/voice/mode', methods=['POST'])
        def voice_mode():
            """Toggle voice mode"""
            data = request.get_json()
            enable = data.get('enable', False)
            
            if enable:
                self.voice_mode_active = True
                self.voice.say("Voice mode activated")
                return jsonify({'status': 'activated'})
            else:
                self.voice_mode_active = False
                self.voice.stop_voice_mode()
                return jsonify({'status': 'deactivated'})
        
        @self.app.route('/api/personality')
        def get_personality():
            """Get personality profile"""
            return jsonify(self.personality.get_personality_summary())
        
        @self.app.route('/api/help')
        def get_help():
            """Get help information"""
            return jsonify({
                'commands': [
                    {'command': 'help', 'description': 'Show available commands'},
                    {'command': 'status', 'description': 'Show system status'},
                    {'command': 'skills', 'description': 'List all skills'},
                    {'command': 'mood', 'description': 'Show current mood'},
                    {'command': 'history', 'description': 'Show chat history'},
                    {'command': 'voice', 'description': 'Toggle voice mode'},
                    {'command': 'clear', 'description': 'Clear chat'}
                ],
                'greeting': self.personality.get_greeting()
            })
        
        @self.app.route('/api/voice/background', methods=['POST'])
        def background_voice():
            """Start/stop background voice with wake word"""
            data = request.get_json()
            enable = data.get('enable', False)
            
            if enable:
                self.background_voice.start(command_callback=self._handle_voice_command)
                return jsonify({'status': 'background_voice_started', 'wake_word': 'JARVIS'})
            else:
                self.background_voice.stop()
                return jsonify({'status': 'background_voice_stopped'})
    
    def _handle_voice_command(self, text: str) -> str:
        """Handle voice command after wake word"""
        # Process through emotional system
        emotion, emotional_response = self.emotional_system.process_emotional_input(text)
        
        # Process through core
        response = self.core.process_input(text)
        
        # Speak response
        self.voice.say(response)
        
        # Store in history
        self.chat_history.append({
            'user': text,
            'jarvis': response,
            'emotion': emotion.primary.value,
            'intensity': emotion.intensity,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def run(self):
        """Run the web server"""
        print(f"[Web] Starting J.A.R.V.I.S. Web Interface")
        print(f"[Web] Server running at http://{self.host}:{self.port}")
        print(f"[Web] Access from Android: http://YOUR_PC_IP:{self.port}")
        
        self.app.run(host=self.host, port=self.port, debug=False, threaded=True)


def main():
    """Main entry point"""
    web_jarvis = WebJARVIS()
    web_jarvis.run()


if __name__ == "__main__":
    main()
