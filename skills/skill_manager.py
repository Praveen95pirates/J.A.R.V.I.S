#!/usr/bin/env python3
"""
J.A.R.V.I.S. Skill Manager
Auto-discovers skills from skills/ directory and supports remote updates
"""

import os
import sys
import json
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Type
from dataclasses import dataclass
from enum import Enum

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from skills.skills_registry import SkillsRegistry, Skill, SkillCategory


class SkillManager:
    """Manages skill discovery, loading, and remote updates"""
    
    def __init__(self):
        self.registry = SkillsRegistry()
        self.skills_dir = PROJECT_ROOT / "skills"
        self.loaded_modules: Dict[str, any] = {}
        self._auto_discover()
    
    def _auto_discover(self):
        """Auto-discover all skills from skills/ directory"""
        print("[SkillManager] Auto-discovering skills...")
        
        # Discover Python modules in skills directory
        for py_file in self.skills_dir.glob("*.py"):
            if py_file.stem in ["__init__", "skills_registry", "complete_skills_library"]:
                continue
            
            try:
                module_name = f"skills.{py_file.stem}"
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.loaded_modules[py_file.stem] = module
                    
                    # Look for skill definitions
                    if hasattr(module, 'register_skills'):
                        module.register_skills(self.registry)
                        print(f"[SkillManager] Loaded skills from {py_file.stem}")
            except Exception as e:
                print(f"[SkillManager] Failed to load {py_file.stem}: {e}")
        
        print(f"[SkillManager] Discovered {len(self.registry.list_enabled())} enabled skills")
    
    def get_skill_info(self, name: str) -> Optional[Dict]:
        """Get detailed info about a skill"""
        skill = self.registry.get_skill(name)
        if not skill:
            return None
        
        return {
            "name": skill.name,
            "category": skill.category.value,
            "description": skill.description,
            "enabled": skill.enabled,
            "requires_auth": skill.requires_auth,
            "parameters": skill.parameters or {}
        }
    
    def enable_skill(self, name: str) -> Dict:
        """Enable a skill"""
        skill = self.registry.get_skill(name)
        if not skill:
            return {"error": "skill_not_found", "name": name}
        
        self.registry.enable_skill(name)
        return {"status": "enabled", "name": name}
    
    def disable_skill(self, name: str) -> Dict:
        """Disable a skill"""
        skill = self.registry.get_skill(name)
        if not skill:
            return {"error": "skill_not_found", "name": name}
        
        self.registry.disable_skill(name)
        return {"status": "disabled", "name": name}
    
    def add_remote_skill(self, skill_data: Dict) -> Dict:
        """
        Add a skill from remote update
        
        Expected format:
        {
            "name": "skill_name",
            "category": "category_name",
            "description": "Skill description",
            "code": "python code for the skill",
            "enabled": true,
            "requires_auth": false
        }
        """
        try:
            name = skill_data.get("name")
            if not name:
                return {"error": "missing_name"}
            
            # Check if skill already exists
            existing = self.registry.get_skill(name)
            if existing:
                # Update existing skill
                existing.description = skill_data.get("description", existing.description)
                existing.enabled = skill_data.get("enabled", existing.enabled)
                existing.requires_auth = skill_data.get("requires_auth", existing.requires_auth)
                return {"status": "updated", "name": name}
            
            # Create new skill
            try:
                category = SkillCategory[skill_data.get("category", "SYSTEM").upper()]
            except KeyError:
                category = SkillCategory.SYSTEM
            
            new_skill = Skill(
                name=name,
                category=category,
                description=skill_data.get("description", ""),
                enabled=skill_data.get("enabled", True),
                requires_auth=skill_data.get("requires_auth", False),
                parameters=skill_data.get("parameters", {})
            )
            
            self.registry.register(new_skill)
            
            # If code is provided, save it as a module
            code = skill_data.get("code")
            if code:
                skill_file = self.skills_dir / f"{name}.py"
                skill_file.write_text(code)
                
                # Reload the module
                try:
                    module_name = f"skills.{name}"
                    spec = importlib.util.spec_from_file_location(module_name, skill_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self.loaded_modules[name] = module
                except Exception as e:
                    print(f"[SkillManager] Failed to reload {name}: {e}")
            
            return {"status": "added", "name": name}
        
        except Exception as e:
            return {"error": str(e)}
    
    def remove_skill(self, name: str) -> Dict:
        """Remove a skill"""
        if name not in self.registry.skills:
            return {"error": "skill_not_found", "name": name}
        
        # Don't remove core skills
        core_skills = ["conversation", "reasoning", "learning", "memory_management"]
        if name in core_skills:
            return {"error": "cannot_remove_core_skill", "name": name}
        
        del self.registry.skills[name]
        
        # Remove file if it exists
        skill_file = self.skills_dir / f"{name}.py"
        if skill_file.exists():
            skill_file.unlink()
        
        return {"status": "removed", "name": name}
    
    def get_all_skills(self) -> Dict:
        """Get all skills with details"""
        return {
            "total": len(self.registry.skills),
            "enabled": len(self.registry.list_enabled()),
            "categories": {
                cat.value: {
                    "total": len(self.registry.get_skills_by_category(cat)),
                    "enabled": len([s for s in self.registry.get_skills_by_category(cat) if s.enabled]),
                    "skills": [s.name for s in self.registry.get_skills_by_category(cat)]
                }
                for cat in SkillCategory
            },
            "skills": [
                {
                    "name": s.name,
                    "category": s.category.value,
                    "description": s.description,
                    "enabled": s.enabled,
                    "requires_auth": s.requires_auth
                }
                for s in self.registry.skills.values()
            ]
        }
    
    def update_from_remote(self, remote_config: Dict) -> Dict:
        """
        Update skills from remote configuration
        
        Expected format:
        {
            "add": [...],
            "update": [...],
            "remove": [...]
        }
        """
        results = {
            "added": [],
            "updated": [],
            "removed": [],
            "errors": []
        }
        
        # Add new skills
        for skill_data in remote_config.get("add", []):
            result = self.add_remote_skill(skill_data)
            if "error" in result:
                results["errors"].append(result)
            else:
                results["added"].append(result["name"])
        
        # Update existing skills
        for skill_data in remote_config.get("update", []):
            name = skill_data.get("name")
            if name and name in self.registry.skills:
                result = self.add_remote_skill(skill_data)
                if "error" in result:
                    results["errors"].append(result)
                else:
                    results["updated"].append(name)
        
        # Remove skills
        for name in remote_config.get("remove", []):
            result = self.remove_skill(name)
            if "error" in result:
                results["errors"].append(result)
            else:
                results["removed"].append(name)
        
        return results


# Global skill manager instance
_skill_manager: Optional[SkillManager] = None

def get_skill_manager() -> SkillManager:
    """Get or create the global skill manager"""
    global _skill_manager
    if _skill_manager is None:
        _skill_manager = SkillManager()
    return _skill_manager
