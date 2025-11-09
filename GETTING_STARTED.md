# 🎯 GETTING STARTED - Quick Guide

## Welcome to Your Ultimate AI Agent!

You now have a fully autonomous AI agent that can control your laptop. Here's how to get started:

## Step 1: Download an AI Model (First Time Only)

Run the setup wizard:

```powershell
python setup_model.py
```

**What to choose?**
- **Mistral 7B (Option 1)** - RECOMMENDED - Best balance of speed and intelligence
- **Llama 3 8B (Option 2)** - Great for complex tasks
- **Falcon (Option 3)** - Fastest, good for simple tasks

The download takes 5-10 minutes (it's a ~4GB file). This happens ONCE - the model is saved locally forever.

## Step 2: Launch the Agent

```powershell
python start_agent.py
```

Or directly:

```powershell
python ultimate_agent.py
```

## Step 3: Start Giving Commands!

The agent appears and waits for your input. Try these beginner-friendly tasks:

### Easy Tasks (Try First!)

```
Create a folder called 'ai_test' on my Desktop
```

```
What is my current CPU usage?
```

```
Calculate 123 * 456 using Python
```

### Intermediate Tasks

```
Find all .txt files in my Documents folder
```

```
Create a Python script that prints hello world
```

```
Check what processes are using the most memory
```

### Advanced Tasks

```
Create a file organizer that sorts files by extension
```

```
Download the content from example.com and summarize it
```

```
Write a script to backup my important files
```

## Built-in Commands

While talking to the agent:

- `stats` - See what the agent has learned
- `export` - Save all knowledge to JSON file
- `quit` - Exit the agent

## Understanding the Agent

### How It Thinks

1. **Receives your request**
2. **Recalls similar past experiences** (if any)
3. **Plans step-by-step**
4. **Chooses the right tools**
5. **Asks for approval** (if dangerous)
6. **Executes the task**
7. **Learns and remembers** for next time

### Tools Available

The agent has these powers:

| Tool | What It Does |
|------|-------------|
| 📁 **file_operation** | Create, read, write, delete files/folders |
| 💻 **terminal_command** | Run any PowerShell command |
| 🌐 **web_search** | Fetch content from URLs |
| 🐍 **python_code** | Execute Python code |
| 📊 **system_info** | Check CPU, RAM, disk, processes |

### Safety System

The agent will ask before:
- ❌ Deleting files
- ❌ Running system commands
- ❌ Accessing protected folders
- ❌ Installing software

**Your options:**
- `y` - Yes, do it
- `n` - No, skip this
- `a` - Approve everything (careful!)
- `q` - Quit the agent

## Example Conversations

### Example 1: Simple Task
```
You: Create a text file with my name in it

Agent: I'll create a text file for you. What name would you like in the file?

You: Greg

Agent: [Creates file]
✓ Task Complete
Created 'name.txt' with content 'Greg'
```

### Example 2: Complex Task
```
You: Analyze my Desktop and organize files into folders

Agent: Let me check your Desktop first...
[Lists Desktop contents]

Agent: I found 15 files. I'll create folders for:
- Documents (PDFs, Word files)
- Images (JPG, PNG)
- Archives (ZIP files)

⚠️ APPROVAL REQUIRED - Moving 15 files
Your choice: y

Agent: [Organizes files]
✓ Task Complete
Organized 15 files into 3 folders
```

### Example 3: Learning
```
You: Parse this CSV file

Agent: I remember doing CSV parsing before. Using pandas...
[Successfully parses using learned method]
✓ Task Complete
```

## Troubleshooting

### "Model not found"
→ Run `python setup_model.py` to download a model

### Agent is slow
→ First run loads the model (takes 30-60 seconds)
→ Reduce max_tokens in `agent_config.json`

### Import errors
→ Make sure you ran the setup: Dependencies are installed in virtual environment

### Agent makes mistakes
→ Be more specific in your requests
→ Break complex tasks into steps
→ The agent learns - it improves over time!

## Tips for Best Results

✅ **DO:**
- Be clear and specific
- Start with simple tasks to learn
- Check `stats` to see agent's learning
- Use the safety system wisely

❌ **DON'T:**
- Auto-approve everything without checking
- Give extremely vague requests
- Expect perfection immediately (it learns!)
- Delete the agent_memory folder (it's the brain!)

## What's Next?

1. **Try the examples**: Run `python demo_examples.py` to see ideas
2. **Customize**: Edit `agent_config.json` for different behavior
3. **Teach it**: The more you use it, the smarter it gets
4. **Experiment**: Try automating your daily tasks!

## Advanced Features

### Export Knowledge
```
You: export
```
Saves everything the agent learned to `agent_knowledge.json`

### Check Statistics
```
You: stats
```
See:
- Total experiences stored
- Successful actions learned
- Conversation history length
- Available tools

### Custom Configuration

Edit `agent_config.json`:

```json
{
  "model_name": "mistral-7b-instruct-v0.2.Q4_0.gguf",
  "auto_approve": false,  // Set true to skip approvals (risky!)
  "max_iterations": 15,   // Max steps per task
  "temperature": 0.7,     // Creativity (0-1, higher = more creative)
  "max_tokens": 2048      // Response length
}
```

## Files You Should Know About

- `agent_memory/` - The agent's brain (vector database)
- `agent_config.json` - Settings
- `current_session.json` - Conversation history
- `agent_knowledge.json` - Exported knowledge (when you export)

**⚠️ Don't delete agent_memory folder** - That's where it stores everything it learned!

## Need Help?

Check `README.md` for full documentation.

---

**Ready? Let's go!** 🚀

```powershell
python start_agent.py
```
