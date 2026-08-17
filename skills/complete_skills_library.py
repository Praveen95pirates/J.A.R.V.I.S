#!/usr/bin/env python3
"""
J.A.R.V.I.S Complete Skills Library
All available skills organized by category
"""

from skills.skills_registry import SkillsRegistry, Skill, SkillCategory

def create_complete_skills_library() -> SkillsRegistry:
    """Create and return a complete skills library with ALL capabilities"""
    registry = SkillsRegistry()
    
    # Clear default skills and add comprehensive ones
    registry.skills.clear()
    
    # ==================== CORE INTELLIGENCE ====================
    registry.register(Skill(
        name="conversation",
        category=SkillCategory.COMMUNICATION,
        description="Natural language conversation and dialogue management",
        enabled=True
    ))
    
    registry.register(Skill(
        name="reasoning",
        category=SkillCategory.ANALYSIS,
        description="Logical reasoning, critical thinking, and problem solving",
        enabled=True
    ))
    
    registry.register(Skill(
        name="learning",
        category=SkillCategory.LEARNING,
        description="Adaptive learning from interactions and user feedback",
        enabled=True
    ))
    
    registry.register(Skill(
        name="memory_management",
        category=SkillCategory.SYSTEM,
        description="Short-term and long-term memory management",
        enabled=True
    ))
    
    registry.register(Skill(
        name="context_awareness",
        category=SkillCategory.ANALYSIS,
        description="Understand and maintain conversation context",
        enabled=True
    ))
    
    # ==================== PRODUCTIVITY ====================
    registry.register(Skill(
        name="task_management",
        category=SkillCategory.PRODUCTIVITY,
        description="Create, update, and manage tasks and todo lists",
        enabled=True
    ))
    
    registry.register(Skill(
        name="note_taking",
        category=SkillCategory.PRODUCTIVITY,
        description="Create, organize, and search notes",
        enabled=True
    ))
    
    registry.register(Skill(
        name="reminder_setting",
        category=SkillCategory.PRODUCTIVITY,
        description="Set and manage reminders and alarms",
        enabled=True
    ))
    
    registry.register(Skill(
        name="calendar_management",
        category=SkillCategory.COMMUNICATION,
        description="Manage calendar events, appointments, and schedules",
        enabled=True,
        requires_auth=True
    ))
    
    registry.register(Skill(
        name="time_tracking",
        category=SkillCategory.PRODUCTIVITY,
        description="Track time spent on tasks and activities",
        enabled=True
    ))
    
    registry.register(Skill(
        name="goal_setting",
        category=SkillCategory.PRODUCTIVITY,
        description="Help set and track personal and professional goals",
        enabled=True
    ))
    
    registry.register(Skill(
        name="project_management",
        category=SkillCategory.PRODUCTIVITY,
        description="Manage projects, milestones, and deliverables",
        enabled=True
    ))
    
    # ==================== CREATIVITY ====================
    registry.register(Skill(
        name="writing",
        category=SkillCategory.CREATIVITY,
        description="Write emails, documents, stories, and creative content",
        enabled=True
    ))
    
    registry.register(Skill(
        name="code_generation",
        category=SkillCategory.CREATIVITY,
        description="Write, debug, and explain code in multiple languages",
        enabled=True
    ))
    
    registry.register(Skill(
        name="brainstorming",
        category=SkillCategory.CREATIVITY,
        description="Generate ideas, solutions, and creative concepts",
        enabled=True
    ))
    
    registry.register(Skill(
        name="storytelling",
        category=SkillCategory.CREATIVITY,
        description="Create and narrate engaging stories",
        enabled=True
    ))
    
    registry.register(Skill(
        name="poetry",
        category=SkillCategory.CREATIVITY,
        description="Write poems and creative verse",
        enabled=True
    ))
    
    registry.register(Skill(
        name="music_generation",
        category=SkillCategory.CREATIVITY,
        description="Generate and compose music concepts and lyrics",
        enabled=True
    ))
    
    registry.register(Skill(
        name="design_thinking",
        category=SkillCategory.CREATIVITY,
        description="Creative problem-solving and design solutions",
        enabled=True
    ))
    
    # ==================== ANALYSIS ====================
    registry.register(Skill(
        name="research",
        category=SkillCategory.ANALYSIS,
        description="Research topics and gather information",
        enabled=True
    ))
    
    registry.register(Skill(
        name="data_analysis",
        category=SkillCategory.ANALYSIS,
        description="Analyze data, statistics, and generate insights",
        enabled=True
    ))
    
    registry.register(Skill(
        name="summarization",
        category=SkillCategory.ANALYSIS,
        description="Summarize long texts, documents, and articles",
        enabled=True
    ))
    
    registry.register(Skill(
        name="trend_analysis",
        category=SkillCategory.ANALYSIS,
        description="Analyze trends and patterns",
        enabled=True
    ))
    
    registry.register(Skill(
        name="comparison",
        category=SkillCategory.ANALYSIS,
        description="Compare options, products, or choices",
        enabled=True
    ))
    
    registry.register(Skill(
        name="risk_assessment",
        category=SkillCategory.ANALYSIS,
        description="Evaluate risks and provide risk assessments",
        enabled=True
    ))
    
    # ==================== COMMUNICATION ====================
    registry.register(Skill(
        name="email_management",
        category=SkillCategory.COMMUNICATION,
        description="Read, send, organize, and respond to emails",
        enabled=True,
        requires_auth=True
    ))
    
    registry.register(Skill(
        name="messaging",
        category=SkillCategory.COMMUNICATION,
        description="Send and receive messages across platforms",
        enabled=True
    ))
    
    registry.register(Skill(
        name="phone_calls",
        category=SkillCategory.COMMUNICATION,
        description="Make and manage phone calls",
        enabled=True,
        requires_auth=True
    ))
    
    registry.register(Skill(
        name="meeting_scheduling",
        category=SkillCategory.COMMUNICATION,
        description="Schedule and manage meetings",
        enabled=True,
        requires_auth=True
    ))
    
    registry.register(Skill(
        name="translation",
        category=SkillCategory.COMMUNICATION,
        description="Translate text between languages",
        enabled=True
    ))
    
    registry.register(Skill(
        name="presentation_creation",
        category=SkillCategory.COMMUNICATION,
        description="Create presentations and visual content",
        enabled=True
    ))
    
    # ==================== SYSTEM CONTROL ====================
    registry.register(Skill(
        name="file_management",
        category=SkillCategory.SYSTEM,
        description="Create, read, update, delete, and organize files",
        enabled=True
    ))
    
    registry.register(Skill(
        name="computer_control",
        category=SkillCategory.SYSTEM,
        description="Control desktop applications and automate tasks",
        enabled=True
    ))
    
    registry.register(Skill(
        name="web_browsing",
        category=SkillCategory.SYSTEM,
        description="Browse web, search information, interact with websites",
        enabled=True
    ))
    
    registry.register(Skill(
        name="system_automation",
        category=SkillCategory.AUTOMATION,
        description="Automate system tasks and workflows",
        enabled=True
    ))
    
    registry.register(Skill(
        name="app_control",
        category=SkillCategory.SYSTEM,
        description="Launch and control desktop applications",
        enabled=True
    ))
    
    registry.register(Skill(
        name="media_control",
        category=SkillCategory.SYSTEM,
        description="Control media playback and volume",
        enabled=True
    ))
    
    registry.register(Skill(
        name="screenshot",
        category=SkillCategory.SYSTEM,
        description="Take and analyze screenshots",
        enabled=True
    ))
    
    registry.register(Skill(
        name="system_monitoring",
        category=SkillCategory.SYSTEM,
        description="Monitor system performance and resources",
        enabled=True
    ))
    
    # ==================== EMOTIONAL SUPPORT ====================
    registry.register(Skill(
        name="emotional_support",
        category=SkillCategory.EMOTIONAL,
        description="Provide emotional support, empathy, and comfort",
        enabled=True
    ))
    
    registry.register(Skill(
        name="mood_tracking",
        category=SkillCategory.EMOTIONAL,
        description="Track and analyze emotional patterns",
        enabled=True
    ))
    
    registry.register(Skill(
        name="motivation",
        category=SkillCategory.EMOTIONAL,
        description="Provide motivation, encouragement, and inspiration",
        enabled=True
    ))
    
    registry.register(Skill(
        name="stress_management",
        category=SkillCategory.EMOTIONAL,
        description="Help manage stress and anxiety",
        enabled=True
    ))
    
    registry.register(Skill(
        name="mindfulness",
        category=SkillCategory.EMOTIONAL,
        description="Guide meditation and mindfulness exercises",
        enabled=True
    ))
    
    registry.register(Skill(
        name="relationship_advice",
        category=SkillCategory.EMOTIONAL,
        description="Provide thoughtful relationship guidance",
        enabled=True
    ))
    
    registry.register(Skill(
        name="crisis_support",
        category=SkillCategory.EMOTIONAL,
        description="Detect crisis indicators and provide immediate support",
        enabled=True
    ))
    
    # ==================== AUTOMATION ====================
    registry.register(Skill(
        name="workflow_automation",
        category=SkillCategory.AUTOMATION,
        description="Create and manage automated workflows",
        enabled=True
    ))
    
    registry.register(Skill(
        name="scheduled_tasks",
        category=SkillCategory.AUTOMATION,
        description="Schedule and automate recurring tasks",
        enabled=True
    ))
    
    registry.register(Skill(
        name="email_automation",
        category=SkillCategory.AUTOMATION,
        description="Automate email responses and management",
        enabled=True,
        requires_auth=True
    ))
    
    registry.register(Skill(
        name="backup_automation",
        category=SkillCategory.AUTOMATION,
        description="Automate file and data backups",
        enabled=True
    ))
    
    registry.register(Skill(
        name="report_generation",
        category=SkillCategory.AUTOMATION,
        description="Generate automated reports and summaries",
        enabled=True
    ))
    
    # ==================== LEARNING ====================
    registry.register(Skill(
        name="skill_acquisition",
        category=SkillCategory.LEARNING,
        description="Learn new skills and adapt to user needs",
        enabled=True
    ))
    
    registry.register(Skill(
        name="knowledge_building",
        category=SkillCategory.LEARNING,
        description="Build and maintain knowledge base",
        enabled=True
    ))
    
    registry.register(Skill(
        name="tutoring",
        category=SkillCategory.LEARNING,
        description="Tutor and explain concepts in various subjects",
        enabled=True
    ))
    
    registry.register(Skill(
        name="language_learning",
        category=SkillCategory.LEARNING,
        description="Assist with learning new languages",
        enabled=True
    ))
    
    registry.register(Skill(
        name="reading_comprehension",
        category=SkillCategory.LEARNING,
        description="Analyze and explain complex texts",
        enabled=True
    ))
    
    # ==================== INFORMATION ====================
    registry.register(Skill(
        name="weather",
        category=SkillCategory.ANALYSIS,
        description="Get weather information and forecasts",
        enabled=True
    ))
    
    registry.register(Skill(
        name="news",
        category=SkillCategory.ANALYSIS,
        description="Get latest news and updates",
        enabled=True
    ))
    
    registry.register(Skill(
        name="stock_market",
        category=SkillCategory.ANALYSIS,
        description="Track stocks and financial markets",
        enabled=True
    ))
    
    registry.register(Skill(
        name="dictionary",
        category=SkillCategory.ANALYSIS,
        description="Look up words and definitions",
        enabled=True
    ))
    
    registry.register(Skill(
        name="calculation",
        category=SkillCategory.ANALYSIS,
        description="Perform mathematical calculations",
        enabled=True
    ))
    
    registry.register(Skill(
        name="unit_conversion",
        category=SkillCategory.ANALYSIS,
        description="Convert between units and measurements",
        enabled=True
    ))
    
    # ==================== ENTERTAINMENT ====================
    registry.register(Skill(
        name="jokes",
        category=SkillCategory.CREATIVITY,
        description="Tell jokes and humor",
        enabled=True
    ))
    
    registry.register(Skill(
        name="games",
        category=SkillCategory.CREATIVITY,
        description="Play text-based games",
        enabled=True
    ))
    
    registry.register(Skill(
        name="music_recommendations",
        category=SkillCategory.CREATIVITY,
        description="Recommend music based on mood and preference",
        enabled=True
    ))
    
    registry.register(Skill(
        name="movie_recommendations",
        category=SkillCategory.CREATIVITY,
        description="Recommend movies and shows",
        enabled=True
    ))
    
    # ==================== SECURITY & PRIVACY ====================
    registry.register(Skill(
        name="password_generation",
        category=SkillCategory.SYSTEM,
        description="Generate secure passwords",
        enabled=True
    ))
    
    registry.register(Skill(
        name="security_advice",
        category=SkillCategory.SYSTEM,
        description="Provide cybersecurity guidance",
        enabled=True
    ))
    
    registry.register(Skill(
        name="privacy_protection",
        category=SkillCategory.SYSTEM,
        description="Advise on privacy protection",
        enabled=True
    ))

    # ==================== FINANCE & TRADING ====================
    registry.register(Skill(
        name="market_data",
        category=SkillCategory.FINANCE,
        description="Fetch live market data for stocks, crypto, forex, and commodities",
        enabled=True
    ))
    registry.register(Skill(
        name="stock_quotes",
        category=SkillCategory.TRADING,
        description="Get real-time stock quotes, charts, and price analysis",
        enabled=True
    ))
    registry.register(Skill(
        name="crypto_trading",
        category=SkillCategory.TRADING,
        description="Monitor crypto prices, portfolio, and execute trades via broker APIs",
        enabled=True
    ))
    registry.register(Skill(
        name="forex_trading",
        category=SkillCategory.TRADING,
        description="Track forex pairs, analyze trends, and manage currency trades",
        enabled=True
    ))
    registry.register(Skill(
        name="technical_analysis",
        category=SkillCategory.TRADING,
        description="Generate RSI, MACD, Bollinger Bands, moving averages, and candlestick signals",
        enabled=True
    ))
    registry.register(Skill(
        name="portfolio_tracking",
        category=SkillCategory.FINANCE,
        description="Track holdings, P&L, asset allocation, and performance across brokers",
        enabled=True
    ))
    registry.register(Skill(
        name="risk_management",
        category=SkillCategory.TRADING,
        description="Calculate position sizing, stop loss, take profit, and max drawdown limits",
        enabled=True
    ))
    registry.register(Skill(
        name="trade_execution",
        category=SkillCategory.TRADING,
        description="Place, modify, and cancel orders via broker APIs with confirmation flow",
        enabled=True,
        requires_auth=True
    ))
    registry.register(Skill(
        name="broker_integration",
        category=SkillCategory.TRADING,
        description="Connect and authenticate to brokers like Zerodha, Interactive Brokers, etc.",
        enabled=True,
        requires_auth=True
    ))
    registry.register(Skill(
        name="options_analytics",
        category=SkillCategory.TRADING,
        description="Analyze option chains, greeks, IV, and build option strategies",
        enabled=True
    ))
    registry.register(Skill(
        name="futures_analytics",
        category=SkillCategory.TRADING,
        description="Analyze futures curves, open interest, and roll costs",
        enabled=True
    ))
    registry.register(Skill(
        name="backtesting",
        category=SkillCategory.TRADING,
        description="Run strategy backtests over historical data with performance metrics",
        enabled=True
    ))
    registry.register(Skill(
        name="paper_trading",
        category=SkillCategory.TRADING,
        description="Simulate trades with virtual balance for strategy validation",
        enabled=True
    ))
    registry.register(Skill(
        name="alert_management",
        category=SkillCategory.TRADING,
        description="Create price, indicator, and news alerts with notifications",
        enabled=True
    ))
    registry.register(Skill(
        name="economic_calendar",
        category=SkillCategory.FINANCE,
        description="Track macro events, earnings, RBI/Fed meetings, and high-impact news",
        enabled=True
    ))
    registry.register(Skill(
        name="news_sentiment",
        category=SkillCategory.FINANCE,
        description="Analyze market news sentiment and impact on holdings",
        enabled=True
    ))
    registry.register(Skill(
        name="mutual_funds",
        category=SkillCategory.FINANCE,
        description="Compare MF schemes, NAV history, SIP plans, and tax implications",
        enabled=True
    ))
    registry.register(Skill(
        name="bond_analytics",
        category=SkillCategory.FINANCE,
        description="Analyze bonds, yield curves, duration, and credit risk",
        enabled=True
    ))
    registry.register(Skill(
        name="tax_reporting",
        category=SkillCategory.FINANCE,
        description="Generate P&L reports, tax summaries, and compliance statements",
        enabled=True
    ))
    registry.register(Skill(
        name="commodities_trading",
        category=SkillCategory.TRADING,
        description="Trade and analyze gold, silver, crude, and agricultural commodities",
        enabled=True
    ))
    registry.register(Skill(
        name="trading_journal",
        category=SkillCategory.TRADING,
        description="Log trades, review mistakes, and track strategy performance over time",
        enabled=True
    ))
    registry.register(Skill(
        name="algo_trading",
        category=SkillCategory.TRADING,
        description="Create, test, and deploy algorithmic trading strategies",
        enabled=True,
        requires_auth=True
    ))
    
    return registry


if __name__ == "__main__":
    registry = create_complete_skills_library()
    
    print("=== J.A.R.V.I.S. Complete Skills Library ===\n")
    summary = registry.get_summary()
    
    total_skills = 0
    for category, info in summary.items():
        print(f"\n{category.upper()}")
        for skill in info['skills']:
            status = "✓" if skill in [s.name for s in registry.list_enabled()] else "✗"
            print(f"  {status} {skill}")
            total_skills += 1
    
    print(f"\n\nTotal Skills: {total_skills}")
    print(f"Enabled: {len(registry.list_enabled())}")
    print(f"Categories: {len(summary)}")
