# 🌊 Tides DXT - Rhythmic Workflow Management

A Model Context Protocol (MCP) server that brings the natural rhythm of ocean tides to your productivity workflow. Tides helps you create sustainable work patterns by aligning your tasks with tidal cycles.

## 🌟 Why Tides?

Just as ocean tides follow predictable patterns of ebb and flow, our productivity naturally cycles through periods of deep focus and necessary rest. Tides DXT embraces this rhythm, helping you:

- **Work with your natural energy**: Choose from gentle, moderate, or strong flow intensities
- **Build sustainable habits**: Daily, weekly, project, and seasonal tide cycles
- **Track your patterns**: Monitor your productivity flows over time
- **Honor rest periods**: Built-in recognition that ebb is as important as flow

## 🚀 Features

### Core Tools

1. **create_tide** - Initialize a new tidal workflow
   - Daily tides for consistent routines
   - Weekly tides for recurring projects
   - Project tides for specific goals
   - Seasonal tides for long-term cycles

2. **list_tides** - View your active workflows
   - Filter by type or status
   - See upcoming flow times
   - Track completion patterns

3. **flow_tide** - Start a focused work session
   - Choose your intensity level
   - Get contextual guidance
   - Automatic tracking and next flow scheduling

## 📦 Installation

### For Claude Desktop

1. Install the MCP server:
```bash
git clone https://github.com/yourusername/tides-dxt.git
cd tides-dxt
pip install -e .
```

2. Configure Claude Desktop:
```json
{
  "mcpServers": {
    "tides": {
      "command": "python",
      "args": [
        "/path/to/tides-dxt/server/main.py"
      ],
      "env": {
        "TIDES_STORAGE_PATH": "~/Documents/TidesData"
      }
    }
  }
}
```

## 🌊 Usage Examples

### Starting Your Day
```
Claude: Let me create a daily tide for your morning routine.
> create_tide(name="Morning Deep Work", flow_type="daily", description="Core focused work before meetings")
```

### Beginning a Flow Session
```
Claude: Ready to start your morning flow? I'll set up a moderate 25-minute session.
> flow_tide(tide_id="tide_123", intensity="moderate", duration=25)
```

### Checking Your Patterns
```
Claude: Let's see your active workflows.
> list_tides(active_only=true)
```

## 🎯 Philosophy

Tides is built on the principle that sustainable productivity comes from working WITH your natural rhythms, not against them. Each flow type serves a purpose:

- **Gentle flows**: For warming up, administrative tasks, or low-energy periods
- **Moderate flows**: Your standard focused work sessions
- **Strong flows**: Deep work requiring maximum concentration

## 🛠️ Development

### Running Tests
```bash
pytest tests/ -v
```

### Architecture
- Pure Python implementation using MCP SDK
- File-based storage for simplicity and portability
- Async/await patterns for responsive interactions
- Comprehensive test coverage

## 📝 Future Enhancements

- Integration with calendar systems for smart scheduling
- Analytics dashboard for productivity insights
- Team tides for synchronized group work
- Biometric integration for energy-aware scheduling

## 🤝 Contributing

We welcome contributions! Whether it's:
- New tide types or flow patterns
- Integration with productivity tools
- Visualization improvements
- Documentation enhancements

## 📄 License

MIT License - see LICENSE file for details

---

*Built with 🌊 by developers who understand that rest is not the absence of productivity, but an essential part of it.*