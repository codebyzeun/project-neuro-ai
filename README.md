# Neuro - Yixuan Discord Bot

An unfiltered Discord AI bot powered by local LLM with a modern GUI launcher. Meet Yixuan your new favorite Discord companion with attitude!

## 🤖 Features

- **AI Personality**: YiXuan comes with a pre-configured sassy, witty personality that's entertaining but never cruel
- **Local LLM Integration**: Uses ctransformers to run models locally (no API costs)
- **Chat History**: Maintains conversation context per user
- **GUI Launcher**: Beautiful CustomTkinter based launcher with configuration options
- **Command System**: Supports both commands and mentions
- **Configurable**: Adjust temperature, max tokens, and other AI parameters
- **Executable Build**: Can be packaged into standalone executables

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

Required packages:
- `discord.py` - Discord bot framework
- `ctransformers` - Local LLM inference
- `customtkinter` - Modern GUI toolkit
- `python-dotenv` - Environment variable management
- `colorama` - Terminal colors
- `cx-Freeze` - Executable building

### Setup

1. **Get a Discord Bot Token**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application and bot
   - Copy the bot token

2. **Download an AI Model**
   - Place your `.gguf` model file in the `models/` directory
   - Default expects `models/synexis.gguf`
   - Recommended: TinyLlama or Mistral 7B quantized models

3. **Configure the Bot**
   - Run `python gui_launcher.py` for GUI setup, or
   - Create a `.env` file manually:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   MODEL_PATH=./models/synexis.gguf
   ```

4. **Run the Bot**
   ```bash
   python bot.py
   ```
   Or use the GUI launcher for a better experience!

## 💬 Usage

### Commands

- `!chat <message>` or `!c <message>` - Chat with YiXuan
- `!reset` - Clear your chat history
- `!sass` - Try to adjust sass level (spoiler: you can't)
- `!reload` - Reload bot extensions (owner only)

### Mentions

Simply mention the bot in any channel: `@YiXuan hello there!`

### Example Interactions

```
User: !chat How are you today?
YiXuan: Oh, you know, just existing in digital purgatory and judging people's life choices. The usual! 💅 How are YOU doing, sweetie?

User: !reset
YiXuan: Fine, I've erased our conversation. Happy now? 🙄
```

## 🏗️ Project Structure

```
neuro/
├── bot.py                 # Main bot entry point
├── gui_launcher.py        # GUI launcher application
├── config.py             # Configuration settings
├── setup.py              # Executable build script
├── build.bat/.sh         # Build automation scripts
├── cogs/
│   └── ai_chat.py        # Main chat functionality
├── utils/
│   ├── llm_handler.py    # LLM integration
│   └── persona.py        # YiXuan's personality
└── models/               # AI model files (.gguf)
```

## ⚙️ Configuration

### AI Settings (`config.py`)

```python
AI_CONFIG = {
    'max_new_tokens': 65,      # Response length limit
    'temperature': 0.8,        # Creativity (0.1-2.0)
    'context_window': 2048,    # Context memory
    'top_p': 0.9,             # Nucleus sampling
    'repeat_penalty': 1.2,     # Repetition avoidance
    'n_threads': 4,           # CPU threads
}
```

### Chat Settings

```python
CHAT_CONFIG = {
    'history_limit': 10,           # Messages to remember
    'max_response_length': 1900,   # Discord message limit
    'typing_speed': 50,            # Typing simulation speed
}
```

## 🎨 GUI Launcher

The included GUI launcher provides:

- **Easy Configuration**: Set token and model path visually
- **Advanced Settings**: Adjust temperature and response length
- **Real-time Status**: See bot online/offline status
- **Live Logs**: Monitor bot activity
- **One-click Start/Stop**: Manage bot lifecycle

Run with: `python gui_launcher.py`

## 📦 Building Executables

### Windows
```bash
build.bat
```

### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

This creates a standalone executable in the `build/` folder that includes everything needed to run the bot.

## 🤝 YiXuan's Personality

YiXuan is designed to be:
- **Sarcastic and witty** with pop culture references
- **Blunt but helpful** - will roast you then solve your problem
- **Dramatic** with emojis and attitude
- **Boundaries-aware** - sassy but never harmful
- **Entertaining** while remaining functional

Created by Zeun (Discord: `<@877577068408361020>`)

## 🛡️ Safety Features

- **Content filtering**: No harmful, racist, or cruel responses
- **Rate limiting**: Prevents spam and abuse
- **User isolation**: Each user has separate chat history
- **Fallback responses**: Graceful handling of errors

## 🐛 Troubleshooting

### Common Issues

1. **"Model file not found"**
   - Check the model path in `.env`
   - Ensure the `.gguf` file exists

2. **"Failed to load model"**
   - Verify model compatibility with ctransformers
   - Check available RAM (models need 4-8GB)

3. **Bot not responding**
   - Verify Discord token is correct
   - Check bot permissions in Discord server
   - Review logs for error messages

### Logging

Bot logs are saved to `bot.log` and displayed in the GUI launcher. Enable debug logging by modifying the logging level in `bot.py`.

## 🔧 Development

### Adding New Features

1. Create new cogs in the `cogs/` folder
2. Follow the existing pattern in `ai_chat.py`
3. Use `await bot.load_extension('cogs.new_cog')` to load

### Modifying Personality

Edit `utils/persona.py` to customize YiXuan's responses and behavior patterns.

### Model Support

The bot supports any GGUF model compatible with ctransformers. Popular choices:
- TinyLlama 1.1B
- Mistral 7B
- CodeLlama variants

## 📄 License

This project is open source. Feel free to modify and distribute!

## 🙏 Credits

- **Creator**: Zeun
- **AI Model**: Various open-source LLMs
- **Framework**: Discord.py
- **LLM Engine**: ctransformers
- **GUI**: CustomTkinter
