#!/usr/bin/env python3
"""
J.A.R.V.I.S Skills Registry
Defines and manages all capabilities and skills
"""

from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from enum import Enum


class SkillCategory(Enum):
    """Categories of skills"""
    PRODUCTIVITY = "productivity"
    CREATIVITY = "creativity"
    ANALYSIS = "analysis"
    COMMUNICATION = "communication"
    SYSTEM = "system"
    LEARNING = "learning"
    EMOTIONAL = "emotional"
    AUTOMATION = "automation"
    FINANCE = "finance"
    TRADING = "trading"


@dataclass
class Skill:
    """Represents a skill/ability"""
    name: str
    category: SkillCategory
    description: str
    enabled: bool = True
    requires_auth: bool = False
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


class SkillsRegistry:
    """Registry of all J.A.R.V.I.S. skills"""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self._register_default_skills()
    
    def _register_default_skills(self):
        """Register default skills"""
        
        # Core Intelligence Skills
        self.register(Skill(
            name="conversation",
            category=SkillCategory.COMMUNICATION,
            description="Natural language conversation and dialogue",
            enabled=True
        ))
        
        self.register(Skill(
            name="reasoning",
            category=SkillCategory.ANALYSIS,
            description="Logical reasoning and problem solving",
            enabled=True
        ))
        
        self.register(Skill(
            name="learning",
            category=SkillCategory.LEARNING,
            description="Adaptive learning from interactions",
            enabled=True
        ))
        
        # Productivity Skills
        self.register(Skill(
            name="task_management",
            category=SkillCategory.PRODUCTIVITY,
            description="Manage tasks, todos, and schedules",
            enabled=True
        ))
        
        self.register(Skill(
            name="note_taking",
            category=SkillCategory.PRODUCTIVITY,
            description="Create and organize notes",
            enabled=True
        ))
        
        self.register(Skill(
            name="reminder",
            category=SkillCategory.PRODUCTIVITY,
            description="Set and manage reminders",
            enabled=True
        ))
        
        # Creative Skills
        self.register(Skill(
            name="writing",
            category=SkillCategory.CREATIVITY,
            description="Write emails, documents, stories",
            enabled=True
        ))
        
        self.register(Skill(
            name="code_generation",
            category=SkillCategory.CREATIVITY,
            description="Write and explain code",
            enabled=True
        ))
        
        self.register(Skill(
            name="brainstorming",
            category=SkillCategory.CREATIVITY,
            description="Generate ideas and creative solutions",
            enabled=True
        ))
        
        # Analysis Skills
        self.register(Skill(
            name="research",
            category=SkillCategory.ANALYSIS,
            description="Research and information gathering",
            enabled=True
        ))
        
        self.register(Skill(
            name="data_analysis",
            category=SkillCategory.ANALYSIS,
            description="Analyze data and generate insights",
            enabled=True
        ))
        
        self.register(Skill(
            name="summarization",
            category=SkillCategory.ANALYSIS,
            description="Summarize long texts and documents",
            enabled=True
        ))
        
        # System Skills
        self.register(Skill(
            name="file_management",
            category=SkillCategory.SYSTEM,
            description="Create, read, update, and delete files",
            enabled=True
        ))
        
        self.register(Skill(
            name="computer_control",
            category=SkillCategory.SYSTEM,
            description="Control desktop applications and automation",
            enabled=True
        ))
        
        self.register(Skill(
            name="web_browsing",
            category=SkillCategory.SYSTEM,
            description="Browse and interact with web content",
            enabled=True
        ))
        
        # Communication Skills
        self.register(Skill(
            name="email_management",
            category=SkillCategory.COMMUNICATION,
            description="Read, send, and organize emails",
            enabled=True,
            requires_auth=True
        ))
        
        self.register(Skill(
            name="calendar_management",
            category=SkillCategory.COMMUNICATION,
            description="Manage calendar events and appointments",
            enabled=True,
            requires_auth=True
        ))
        
        self.register(Skill(
            name="messaging",
            category=SkillCategory.COMMUNICATION,
            description="Send and receive messages",
            enabled=True
        ))
        
        # Emotional Skills
        self.register(Skill(
            name="emotional_support",
            category=SkillCategory.EMOTIONAL,
            description="Provide emotional support and empathy",
            enabled=True
        ))
        
        self.register(Skill(
            name="mood_tracking",
            category=SkillCategory.EMOTIONAL,
            description="Track and analyze emotional patterns",
            enabled=True
        ))
        
        self.register(Skill(
            name="motivation",
            category=SkillCategory.EMOTIONAL,
            description="Provide motivation and encouragement",
            enabled=True
        ))
        
        # Automation Skills
        self.register(Skill(
            name="workflow_automation",
            category=SkillCategory.AUTOMATION,
            description="Create and manage automated workflows",
            enabled=True
        ))
        
        self.register(Skill(
            name="scheduled_tasks",
            category=SkillCategory.AUTOMATION,
            description="Schedule and automate recurring tasks",
            enabled=True
        ))
        
        # Learning Skills
        self.register(Skill(
            name="skill_acquisition",
            category=SkillCategory.LEARNING,
            description="Learn new skills and adapt to user needs",
            enabled=True
        ))
        
        self.register(Skill(
            name="knowledge_building",
            category=SkillCategory.LEARNING,
            description="Build and maintain knowledge base",
            enabled=True
        ))
    
    def register(self, skill: Skill):
        """Register a new skill"""
        self.skills[skill.name] = skill
    
    def get_skill(self, name: str) -> Skill:
        """Get a skill by name"""
        return self.skills.get(name)
    
    def get_skills_by_category(self, category: SkillCategory) -> List[Skill]:
        """Get all skills in a category"""
        return [s for s in self.skills.values() if s.category == category]
    
    def enable_skill(self, name: str):
        """Enable a skill"""
        if name in self.skills:
            self.skills[name].enabled = True
    
    def disable_skill(self, name: str):
        """Disable a skill"""
        if name in self.skills:
            self.skills[name].enabled = False
    
    def list_enabled(self) -> List[Skill]:
        """List all enabled skills"""
        return [s for s in self.skills.values() if s.enabled]
    
    def get_summary(self) -> Dict:
        """Get summary of all skills"""
        summary = {}
        for category in SkillCategory:
            skills = self.get_skills_by_category(category)
            summary[category.value] = {
                'total': len(skills),
                'enabled': len([s for s in skills if s.enabled]),
                'skills': [s.name for s in skills]
            }
        return summary
    
    def get_capabilities(self) -> List[str]:
        """Get list of all capabilities"""
        return [
            f"{skill.name}: {skill.description}"
            for skill in self.skills.values()
            if skill.enabled
        ]


# Example usage
if __name__ == "__main__":
    registry = SkillsRegistry()
    
    print("=== J.A.R.V.I.S. Capabilities ===\n")
    
    summary = registry.get_summary()
    for category, info in summary.items():
        print(f"\n{category.upper()}")
        print(f"  Skills: {info['total']} total, {info['enabled']} enabled")
        for skill in info['skills']:
            print(f"    - {skill}")
    
    print("\n=== All Capabilities ===")
    for capability in registry.get_capabilities():
        print(f"  • {capability}")
