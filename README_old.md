# 🤖 GregMish AI - Advanced Local AI Assistant

**Your personal AI assistant with surveillance, voice control, and autonomous capabilities.**

Built with Python, GPT4All, and love. 100% free, 100% local, no API keys required.

---

## 🌟 Features

### Core AI Capabilities
- 🧠 **Local AI Brain** - GPT4All with Llama 3.2/Orca Mini models
- 💬 **180+ Python Packages** - Elite AI/ML toolkit
- 🎯 **Multiple AI Modes** - Simple agent, voice control, surveillance mode

### Voice & Audio
- 🎤 **Voice Control** - Speak commands naturally
- 🗣️ **Natural TTS** - Edge-TTS British voices
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Yorkshire Accent Support** - Works with regional accents

### Surveillance & Automation
- 👁️ **OVERSEER Mode** - Constant screen monitoring
- 📸 **Screenshot Analysis** - See what you're working on
- 🎯 **Context Awareness** - AI knows what you're doing

### Content Creation
- 🎬 **TikTok Video Creator** - Automated video generation
- 📱 **Social Media Posting** - Multi-platform support
- 🎨 **AI Image Generation** - Stable Diffusion integration

### Advanced Features
- 🧠 **Agent Memory** - ChromaDB vector database
- 🔍 **Web Scraping** - Scrapy, DrissionPage, Apify
- 🖼️ **Computer Vision** - YOLO, OCR, face detection
- 📊 **Data Science** - Pandas, NumPy, Matplotlib

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Windows (PowerShell)
- Microphone (for voice features)
- ~10GB disk space (for AI models)

### Installation

```powershell
# Clone the repository
git clone https://github.com/yourusername/gregmish-ai.git
cd gregmish-ai

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Download AI model (first time only)
python setup_model.py
```

### Basic Usage

```powershell
# Simple AI agent
python simple_agent.py

# Voice-controlled AI
python voice_agent.py

# OVERSEER surveillance mode
python overseer.py

# TikTok video creator
python tiktok_creator.py
```

---

## 📚 Available Agents

### 1. Simple Agent (`simple_agent.py`)
Basic conversational AI with file operations.

### 2. Voice Agent (`voice_agent.py`)
Push-to-talk voice interface with speech recognition.

### 3. OVERSEER (`overseer.py`)
**The ultimate surveillance AI:**
- 📸 Monitors screen every 2 seconds
- 🎤 Always listening for "Overseer" wake word
- 🧠 Context-aware responses
- 👁️ Tracks your activities

```powershell
python overseer.py
# Say: "Overseer, what am I looking at?"
```

### 4. TikTok Creator (`tiktok_creator.py`)
Automated viral video generation with AI voices and captions.

### 5. Self-Aware Agent (`self_aware_agent.py`)
AI with persistent memory and self-reflection capabilities.

---

## 🎯 Key Components

### AI Models Used
- **GPT4All** - Local LLM (Llama 3.2 3B / Orca Mini 3B)
- **Stable Diffusion** - Image generation
- **YOLO** - Object detection
- **Whisper** - Speech recognition

### Major Libraries
- `transformers`, `torch` - AI/ML core
- `langchain` - LLM orchestration  
- `opencv-python` - Computer vision
- `edge-tts` - Natural text-to-speech
- `scrapy` - Web scraping
- `chromadb` - Vector database

See [AI_CAPABILITIES.md](AI_CAPABILITIES.md) for full list.

---

## 📁 Project Structure

```
gregmish-ai/
├── simple_agent.py          # Basic AI agent
├── voice_agent.py            # Voice-controlled AI
├── overseer.py               # Surveillance AI
├── tiktok_creator.py         # Video automation
├── self_aware_agent.py       # Memory-enabled AI
├── setup_model.py            # Model downloader
├── requirements.txt          # Python dependencies
├── agent_config.json         # Configuration
├── GETTING_STARTED.md        # Detailed setup guide
├── AI_CAPABILITIES.md        # Full capability list
└── AVAILABLE_UPGRADES.md     # Future enhancements
```

---

## ⚙️ Configuration

Edit `agent_config.json`:

```json
{
  "model_name": "orca-mini-3b-gguf2-q4_0.gguf",
  "temperature": 0.7,
  "max_tokens": 2048,
  "system_prompt": "You are a helpful AI assistant."
}
```

---

## 🎤 OVERSEER Voice Commands

```
"Overseer, what am I looking at?"
"Overseer, help me with this"
"Overseer, create a TikTok video"
"Overseer, check my system"
```

---

## 🛠️ Advanced Features

### Autonomous Planning
See [AVAILABLE_UPGRADES.md](AVAILABLE_UPGRADES.md) for:
- BabyAGI integration
- Autonomous task execution
- Multi-agent systems

### Content Pipeline
1. Research competitors
2. Generate video scripts
3. Create videos with AI voices
4. Post to social media
5. Track analytics

---

## 📊 Package Stats

- **180+ Python packages installed**
- **50+ AI/ML libraries**
- **20+ automation tools**
- **Professional web scraping suite**

---

## ⚠️ Important Notes

### Privacy
- **All processing is local** - No data sent to cloud
- OVERSEER mode records screen activity locally only
- Voice data processed via Google Speech API (can be disabled)

### Models
- AI models are downloaded to `~/.cache/gpt4all/`
- First run downloads ~2GB model
- Models are NOT included in repo (too large)

### Performance
- Recommended: 16GB+ RAM
- GPU not required (CPU inference)
- SSD recommended for model loading

---

## 🚧 Roadmap

- [ ] Autonomous planning framework (BabyAGI)
- [ ] YOLO-based GUI automation
- [ ] Professional video pipeline with stock footage
- [ ] Multi-model routing system
- [ ] Complete marketing automation

See [AVAILABLE_UPGRADES.md](AVAILABLE_UPGRADES.md) for 33+ upgrade options.

---

## 🤝 Contributing

Contributions welcome! This is a personal project that's grown into something special.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push and create a Pull Request

---

## 📝 License

MIT License - Use freely, no restrictions.

---

## 🎯 Use Cases

### Content Creation
- Automated TikTok/Instagram videos
- AI-generated social media posts
- Marketing content at scale

### Personal Assistant
- Voice-controlled task automation
- Screen monitoring and context awareness
- File management and organization

### Development Aid
- Code assistance with OVERSEER
- Automated testing and debugging
- Project documentation generation

### Business Automation
- Competitor research and analysis
- Automated reporting and analytics
- Customer support automation

---

## 🔥 What Makes This Special

This isn't just another AI wrapper. It's a complete AI ecosystem:

✅ **Local-first** - No API costs, full privacy  
✅ **Voice-enabled** - Natural conversation  
✅ **Context-aware** - Knows what you're doing  
✅ **Extensible** - 180+ packages ready to use  
✅ **Production-ready** - Real automation capabilities  

---

## 💬 Support

Got questions? Check out:
- [GETTING_STARTED.md](GETTING_STARTED.md) - Detailed setup
- [AI_CAPABILITIES.md](AI_CAPABILITIES.md) - What it can do
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Full overview

---

## 🙏 Acknowledgments

Built with:
- GPT4All (local LLM)
- Nomic AI (embeddings)
- Hugging Face (transformers)
- OpenCV (vision)
- Edge-TTS (voices)

Special thanks to the open-source AI community.

---

**Made with 🤖 and ☕ by Greg**

*"The future of AI is local, private, and under your control."*
