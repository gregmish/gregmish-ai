"""
Voice-Controlled AI Agent - Yorkshire Accent Edition 😄
Talk to your AI - it listens and responds!
Uses OpenAI Whisper for better accent recognition
"""

import speech_recognition as sr
from gpt4all import GPT4All
import pyttsx3
import time
import os
import tempfile
import wave

class VoiceAgent:
    def __init__(self):
        print("🎤 Initializing Voice-Controlled AI Agent...")
        print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Yorkshire accent support enabled!")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust energy threshold for better detection
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 165)  # Slightly slower for clarity
        self.tts_engine.setProperty('volume', 1.0)
        
        # Initialize GPT4All
        model_path = os.path.join(os.path.expanduser("~"), ".cache", "gpt4all", "orca-mini-3b-gguf2-q4_0.gguf")
        print(f"📦 Loading AI model from: {model_path}")
        self.model = GPT4All(model_path)
        
        # Wake word variations for Yorkshire
        self.wake_words = ["hey ai", "ey up ai", "ai", "hey a i", "aye ai"]
        
        print("✅ Voice Agent Ready!")
        self.speak("Ey up, Master! I'm reet ready to help thee. Just say 'hey AI' and tell me what tha needs.")
    
    def speak(self, text):
        """Make the AI speak"""
        print(f"🤖 AI: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for voice commands using Whisper (better for accents!)"""
        with self.microphone as source:
            print("\n🎤 Listening... (Yorkshire accent welcome!)")
            print("   Say 'hey AI' + your command")
            print("   Or say 'stop listening' to exit")
            
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                print("🎙️  Speak now...")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                print("🔄 Processing your Yorkshire voice with Whisper AI...")
                
                # Use Whisper instead of Google - MUCH better with accents!
                try:
                    text = self.recognizer.recognize_whisper(audio, model="base.en", language="english")
                    print(f"👂 Heard: '{text}'")
                    return text.lower()
                except:
                    # Fallback to Google if Whisper fails
                    print("🔄 Trying Google fallback...")
                    text = self.recognizer.recognize_google(audio, language="en-GB")  # British English!
                    print(f"👂 Heard: '{text}'")
                    return text.lower()
                
            except sr.WaitTimeoutError:
                print("⏰ Nowt heard - say summat!")
                return None
            except sr.UnknownValueError:
                print("❓ Couldn't catch that, love. Say it again?")
                return None
            except sr.RequestError as e:
                print(f"❌ Error: {e}")
                return None
    
    def process_command(self, command):
        """Process the voice command with AI"""
        # Remove wake words (Yorkshire variations included!)
        for wake in self.wake_words:
            command = command.replace(wake, "").strip()
        
        if not command:
            return "Aye, what can I do for thee?"
        
        print(f"\n💭 Thinking about: '{command}'")
        
        # Get AI response with Yorkshire charm
        prompt = f"You are a helpful Yorkshire AI assistant. User said: '{command}'. Respond briefly, helpfully, and with a touch of Yorkshire charm."
        
        with self.model.chat_session():
            response = self.model.generate(prompt, max_tokens=200, temp=0.7)
        
        return response.strip()
    
    def run(self):
        """Main loop - listen and respond"""
        print("\n" + "="*60)
        print("🎤 VOICE-CONTROLLED AI AGENT ACTIVE - EY UP!")
        print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Yorkshire Accent Support Enabled")
        print("="*60)
        print("\n💡 Say: 'Hey AI, what can you do?'")
        print("💡 Say: 'Ey up AI, create a TikTok video'")
        print("💡 Say: 'Hey AI, check my system'")
        print("💡 Say: 'Ta ra' or 'Stop listening' to exit\n")
        
        while True:
            # Listen for voice
            text = self.listen()
            
            if text is None:
                continue
            
            # Check for exit command (Yorkshire versions too!)
            exit_words = ["stop listening", "exit", "quit", "goodbye", "ta ra", "see thee", "ta-ra"]
            if any(word in text for word in exit_words):
                self.speak("Ta ra, Master! Gi' us a shout when tha needs me.")
                break
            
            # Check for wake words (more flexible!)
            if any(wake in text for wake in self.wake_words):
                # Process the command
                response = self.process_command(text)
                self.speak(response)
            else:
                print("💤 Waiting for wake word (hey AI, ey up AI, etc.)...")
                time.sleep(0.5)


def main():
    """Start the voice-controlled agent"""
    print("\n" + "="*60)
    print("🎙️  VOICE-CONTROLLED AI AGENT - YORKSHIRE EDITION")
    print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Powered by OpenAI Whisper (understands accents!)")
    print("="*60)
    print("\n⚠️  Requirements:")
    print("   - Microphone connected and working")
    print("   - Internet connection (for Whisper AI)")
    print("   - Speakers/headphones for AI voice")
    print("\n✨ Wake words: 'hey AI' or 'ey up AI'")
    print("✨ Exit words: 'ta ra' or 'stop listening'")
    print("✨ Speak naturally - Yorkshire accent welcome!\n")
    
    input("\n✅ Press Enter when ready to start...")
    
    try:
        agent = VoiceAgent()
        agent.run()
    except KeyboardInterrupt:
        print("\n\n👋 Agent stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
