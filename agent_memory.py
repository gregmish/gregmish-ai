"""
Memory System for AI Agent
Provides persistent memory, experience storage, and learning capabilities
"""

import json
import chromadb
from chromadb.config import Settings
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class AgentMemory:
    """Persistent memory system using ChromaDB for vector storage"""
    
    def __init__(self, memory_dir: str = "./agent_memory"):
        """Initialize memory system"""
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.memory_dir / "chroma_db"),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create collections
        self.experiences = self.client.get_or_create_collection(
            name="experiences",
            metadata={"description": "Agent experiences and learnings"}
        )
        
        self.successful_actions = self.client.get_or_create_collection(
            name="successful_actions",
            metadata={"description": "Successfully executed actions"}
        )
        
        self.conversation_history = []
        self.session_file = self.memory_dir / "current_session.json"
        self._load_session()
    
    def _load_session(self):
        """Load current session history"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    self.conversation_history = json.load(f)
            except:
                self.conversation_history = []
    
    def _save_session(self):
        """Save current session history"""
        with open(self.session_file, 'w') as f:
            json.dump(self.conversation_history[-100:], f, indent=2)  # Keep last 100
    
    def add_experience(self, task: str, action: str, result: str, success: bool):
        """Store an experience for learning"""
        timestamp = datetime.now().isoformat()
        
        experience = {
            "task": task,
            "action": action,
            "result": result,
            "success": success,
            "timestamp": timestamp
        }
        
        # Store in vector DB
        doc_id = f"exp_{timestamp}_{hash(task)}"
        document = f"Task: {task}\nAction: {action}\nResult: {result}\nSuccess: {success}"
        
        self.experiences.add(
            documents=[document],
            metadatas=[experience],
            ids=[doc_id]
        )
        
        # If successful, also store in successful actions
        if success:
            self.successful_actions.add(
                documents=[f"Task: {task}\nAction: {action}"],
                metadatas={"task": task, "action": action, "timestamp": timestamp},
                ids=[f"success_{doc_id}"]
            )
    
    def recall_similar_experiences(self, query: str, n_results: int = 3) -> List[Dict]:
        """Recall similar past experiences"""
        try:
            results = self.experiences.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            experiences = []
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                experiences.append({
                    "content": doc,
                    "metadata": metadata
                })
            
            return experiences
        except:
            return []
    
    def recall_successful_actions(self, query: str, n_results: int = 3) -> List[Dict]:
        """Recall successful actions for similar tasks"""
        try:
            results = self.successful_actions.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            actions = []
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                actions.append({
                    "content": doc,
                    "metadata": metadata
                })
            
            return actions
        except:
            return []
    
    def add_to_conversation(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._save_session()
    
    def get_conversation_context(self, last_n: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-last_n:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_experiences": self.experiences.count(),
            "successful_actions": self.successful_actions.count(),
            "conversation_length": len(self.conversation_history),
            "memory_location": str(self.memory_dir)
        }
    
    def clear_session(self):
        """Clear current session (not permanent memory)"""
        self.conversation_history = []
        self._save_session()
    
    def export_knowledge(self, output_file: str):
        """Export all learned knowledge to JSON"""
        knowledge = {
            "experiences": [],
            "successful_actions": [],
            "conversation_history": self.conversation_history,
            "exported_at": datetime.now().isoformat()
        }
        
        # Get all experiences
        try:
            all_exp = self.experiences.get()
            if all_exp['documents']:
                for doc, meta in zip(all_exp['documents'], all_exp['metadatas']):
                    knowledge["experiences"].append({
                        "content": doc,
                        "metadata": meta
                    })
        except:
            pass
        
        # Get all successful actions
        try:
            all_success = self.successful_actions.get()
            if all_success['documents']:
                for doc, meta in zip(all_success['documents'], all_success['metadatas']):
                    knowledge["successful_actions"].append({
                        "content": doc,
                        "metadata": meta
                    })
        except:
            pass
        
        with open(output_file, 'w') as f:
            json.dump(knowledge, f, indent=2)
        
        return f"Exported {len(knowledge['experiences'])} experiences and {len(knowledge['successful_actions'])} successful actions"
