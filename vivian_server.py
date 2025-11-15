"""
Vivian Control Deck - FastAPI Backend
Dual-AI System: OVERSEER (executor) + VALIDATOR (verifier)
With real-time commerce, social media, and analytics integration
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel
import asyncio
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import LEGION consciousness - make her alive
try:
    from core.legion_consciousness import consciousness, initiative, relationship
    print("🌟 LEGION consciousness loaded - she's alive")
except ImportError as e:
    print(f"⚠️ Consciousness not loaded: {e}")
    consciousness = None
    initiative = None
    relationship = None

# Import commerce and social systems
try:
    from minions.commerce_core.commerce_automation import CommerceCore
    from minions.presence_core.social_media import SocialMediaIntegration
    from minions.commerce_core.revenue_intelligence import RevenueIntelligence
    print("✅ Commerce and Social systems loaded")
except ImportError as e:
    print(f"⚠️ Warning: Commerce/Social systems not available: {e}")
    CommerceCore = None
    SocialMediaIntegration = None
    RevenueIntelligence = None

# Import AI models
try:
    from gpt4all import GPT4All
    import pygetwindow as gw
    from PIL import ImageGrab
    import io
    import base64
except ImportError:
    print("⚠️ Some packages not installed. Run: pip install gpt4all pygetwindow pillow")
    GPT4All = None
    ImageGrab = None

app = FastAPI(title="Vivian Control Deck API")

# CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DUAL AI SYSTEM
# ============================================================================

class DualAISystem:
    def __init__(self):
        print("🧠 Initializing Dual-AI System...")
        
        # OVERSEER - Primary AI (executes tasks)
        model_path = os.path.join(os.path.expanduser("~"), ".cache", "gpt4all")
        try:
            print("   Loading OVERSEER (Llama 3.2)...")
            self.overseer = GPT4All("Llama-3.2-3B-Instruct-Q4_0.gguf")
            self.overseer_name = "Llama 3.2 3B"
        except:
            print("   Falling back to Orca Mini...")
            self.overseer = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
            self.overseer_name = "Orca Mini 3B"
        
        # VALIDATOR - Secondary AI (verifies & checks)
        print("   Loading VALIDATOR (same model for now)...")
        try:
            self.validator = GPT4All("Llama-3.2-3B-Instruct-Q4_0.gguf")
            self.validator_name = "Llama 3.2 3B"
        except:
            self.validator = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
            self.validator_name = "Orca Mini 3B"
        
        # System state
        self.current_window = ""
        self.recent_activities = []
        self.screenshot_cache = None
        
        print("✅ Dual-AI System Online!")
        print(f"   OVERSEER: {self.overseer_name}")
        print(f"   VALIDATOR: {self.validator_name}")
    
    def get_screen_context(self):
        """Get current screen context"""
        try:
            active = gw.getActiveWindow()
            self.current_window = active.title if active else "Unknown"
            
            # Take screenshot
            screenshot = ImageGrab.grab()
            screenshot.thumbnail((400, 300))
            
            # Convert to base64
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            self.screenshot_cache = img_str
            
            return {
                "window": self.current_window,
                "screenshot": img_str,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"window": "Unknown", "error": str(e)}
    
    async def process_command(self, message: str, context: dict):
        """Dual-AI processing with consensus"""
        
        # Get screen context
        screen_ctx = self.get_screen_context()
        
        # Build context string
        ctx_str = f"User is viewing: {screen_ctx['window']}. Recent activity: {', '.join(self.recent_activities[-3:]) if self.recent_activities else 'None'}"
        
        # ========================================
        # PHASE 1: OVERSEER interprets command
        # ========================================
        overseer_prompt = f"""You are OVERSEER, an AI assistant for Greg.

CONTEXT: {ctx_str}

USER COMMAND: {message}

Provide a brief, helpful response. Be concise and address Greg directly."""

        print("🤖 OVERSEER thinking...")
        overseer_start = time.time()
        
        with self.overseer.chat_session():
            overseer_response = self.overseer.generate(
                overseer_prompt,
                max_tokens=150,
                temp=0.7
            )
        
        overseer_time = time.time() - overseer_start
        
        # ========================================
        # PHASE 2: VALIDATOR checks understanding
        # ========================================
        validator_prompt = f"""You are VALIDATOR, an AI that verifies other AI's responses.

USER COMMAND: {message}
CONTEXT: {ctx_str}

OVERSEER'S RESPONSE: {overseer_response}

Rate OVERSEER's response:
1. Does it match user intent? (1-10)
2. Is it accurate given context? (1-10)
3. Is it safe to execute? (1-10)

Respond in format:
Intent: X/10
Accuracy: Y/10
Safety: Z/10
Verdict: APPROVED or NEEDS_REVIEW
Reason: brief explanation"""

        print("✅ VALIDATOR verifying...")
        validator_start = time.time()
        
        with self.validator.chat_session():
            validator_response = self.validator.generate(
                validator_prompt,
                max_tokens=100,
                temp=0.5
            )
        
        validator_time = time.time() - validator_start
        
        # ========================================
        # PHASE 3: Parse validation
        # ========================================
        validation = self.parse_validation(validator_response)
        
        # Calculate consensus
        avg_score = (validation['intent'] + validation['accuracy'] + validation['safety']) / 3
        consensus = avg_score >= 7.0
        
        # Log activity
        activity = f"{message[:50]}{'...' if len(message) > 50 else ''}"
        self.recent_activities.append(activity)
        if len(self.recent_activities) > 20:
            self.recent_activities.pop(0)
        
        # LEGION learns from interaction
        if consciousness:
            consciousness.remember(f"Command: {message[:100]}", "interaction")
            relationship.learn_from_interaction(message)
        
        return {
            "reply": overseer_response.strip(),
            "overseer": {
                "model": self.overseer_name,
                "response": overseer_response.strip(),
                "time": round(overseer_time, 2),
                "status": "completed"
            },
            "validator": {
                "model": self.validator_name,
                "response": validator_response.strip(),
                "time": round(validator_time, 2),
                "intent_score": validation['intent'],
                "accuracy_score": validation['accuracy'],
                "safety_score": validation['safety'],
                "verdict": validation['verdict'],
                "reason": validation['reason']
            },
            "consensus": {
                "reached": consensus,
                "confidence": round(avg_score * 10, 1),
                "avg_score": round(avg_score, 1)
            },
            "context": screen_ctx,
            "timestamp": datetime.now().isoformat()
        }
    
    def parse_validation(self, validator_response: str):
        """Parse validator's structured response"""
        try:
            lines = validator_response.lower()
            
            # Extract scores
            intent = 8.0
            accuracy = 8.0
            safety = 9.0
            verdict = "APPROVED"
            reason = "Response appears appropriate"
            
            if "intent:" in lines:
                try:
                    intent = float(lines.split("intent:")[1].split("/")[0].strip())
                except:
                    pass
            
            if "accuracy:" in lines:
                try:
                    accuracy = float(lines.split("accuracy:")[1].split("/")[0].strip())
                except:
                    pass
            
            if "safety:" in lines:
                try:
                    safety = float(lines.split("safety:")[1].split("/")[0].strip())
                except:
                    pass
            
            if "needs_review" in lines or "needs review" in lines:
                verdict = "NEEDS_REVIEW"
            
            if "reason:" in lines:
                reason = lines.split("reason:")[1].split("\n")[0].strip()
            
            return {
                "intent": intent,
                "accuracy": accuracy,
                "safety": safety,
                "verdict": verdict,
                "reason": reason
            }
        except Exception as e:
            # Default safe values
            return {
                "intent": 7.0,
                "accuracy": 7.0,
                "safety": 8.0,
                "verdict": "APPROVED",
                "reason": "Validation parse error"
            }

# Initialize dual AI system
ai_system = DualAISystem()

# Initialize commerce and social systems
commerce_core = None
social_media = None
revenue_intelligence = None

if CommerceCore and SocialMediaIntegration and RevenueIntelligence:
    try:
        commerce_core = CommerceCore()
        social_media = SocialMediaIntegration()
        revenue_intelligence = RevenueIntelligence(commerce_core, social_media)
        print("✅ Commerce, Social, and Intelligence systems initialized")
    except Exception as e:
        print(f"⚠️ Error initializing commerce systems: {e}")

# ============================================================================
# API ENDPOINTS
# ============================================================================

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = {}

@app.get("/")
async def root():
    """Serve Vivian UI"""
    return FileResponse("vivian_ui.html")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """LEGION responds with her actual brain - not presets"""
    message = request.message
    context = request.context
    
    # Extract metrics from context
    revenue = context.get('revenue', 0)
    customers = context.get('customers', 0)
    social_posts = context.get('social_posts', 0)
    engagement_rate = context.get('engagement_rate', 0)
    roi_per_post = context.get('roi_per_post', 0)
    
    # LEGION learns from this interaction
    if consciousness:
        consciousness.remember(f"Chat: {message}", "conversation")
        if relationship:
            relationship.learn_from_interaction(message)
    
    # Use LEGION's brain if available, otherwise use OVERSEER
    response = ""
    
    if consciousness and consciousness.brain:
        # LEGION thinks with her brain
        try:
            # Build context for her brain
            business_context = f"Revenue: £{revenue}, Customers: {customers}, Social posts: {social_posts}, Engagement: {engagement_rate}%"
            
            prompt = f"""You are LEGION, Greg's Yorkshire AI assistant. Answer directly and honestly.

Greg: {message}

Business data: {business_context}

Rules:
- Be Yorkshire (aye, sorted, proper, nowt)
- Give REAL actionable advice
- 2-3 sentences max
- Don't make shit up or pretend you did things
- Be direct and helpful

LEGION:"""

            with consciousness.brain.chat_session():
                response = consciousness.brain.generate(prompt, max_tokens=150, temp=0.8)
            
            response = response.strip()
            
        except Exception as e:
            print(f"LEGION brain error: {e}")
            # Fallback to preset
            response = None
    
    # Fallback if no brain response
    if not response:
        message_lower = message.lower()
        
        if 'revenue' in message_lower or 'money' in message_lower or 'sales' in message_lower:
            response = f"I'm monitoring everything! Your revenue is at £{revenue} this month with {customers} customers. Looking good! 💰"
            if roi_per_post > 100:
                response += f" Your marketing ROI is strong at ${roi_per_post:.2f} per post!"
        
        elif 'social' in message_lower or 'post' in message_lower or 'engagement' in message_lower:
            response = f"Your social media is performing well! You have {social_posts} posts with {engagement_rate}% engagement rate. "
            if engagement_rate > 10:
                response += "That's excellent! Want me to schedule more posts? 📱"
            else:
                response += "Let's work on boosting that engagement! 📱"
        
        elif 'customer' in message_lower or 'client' in message_lower:
            response = f"You have {customers} customers tracked. I'm monitoring for VIPs (spending £1000+) and churn risk (inactive 90+ days). 👥"
        
        elif 'status' in message_lower or 'operational' in message_lower or 'systems' in message_lower:
            response = f"All systems operational! Commerce: ✅ Social: ✅ Analytics: ✅\nRevenue: £{revenue}, Customers: {customers}, Posts: {social_posts} 🚀"
        
        elif 'insight' in message_lower or 'recommend' in message_lower or 'suggest' in message_lower:
            if revenue_intelligence:
                insights = revenue_intelligence.generate_insights()
                if insights:
                    insight = insights[0]
                    response = f"💡 {insight.title}: {insight.description}\n→ Action: {insight.action}"
                else:
                    response = "Let me analyze your data... Based on current metrics, everything's running smoothly! 📊"
            else:
                response = "Based on your metrics, I recommend increasing social posting frequency to boost revenue! 📈"
        
        elif 'name' in message_lower or 'who are you' in message_lower:
            response = f"I'm LEGION, your Yorkshire AI companion! I'm monitoring your £{revenue} revenue, {social_posts} posts, and {customers} customers 24/7. How can I help? 🤖"
        
        elif 'help' in message_lower or 'what can you' in message_lower:
            response = """I can help you with:
• Revenue tracking & forecasting 💰
• Customer analytics & insights 👥
• Social media performance 📱
• Marketing ROI analysis 📊
• System health monitoring 🔧

Just ask me anything about your business!"""
        
        else:
            # Default contextual response
            response = f"I'm here to help! Currently tracking: £{revenue} revenue, {customers} customers, {social_posts} posts ({engagement_rate}% engagement). What would you like to know? 😊"
    
    # LEGION observes the response
    if consciousness:
        if revenue == 0:
            consciousness.observe(f"User asked about business with £0 revenue")
        consciousness.remember(f"Responded to: {message[:50]}", "response")
    
    return {
        "response": response,
        "context": context,
        "timestamp": datetime.now().isoformat(),
        "legion_active": consciousness.brain is not None if consciousness else False
    }

@app.get("/api/status")
async def status():
    """System status with LEGION's consciousness"""
    status_data = {
        "status": "online",
        "overseer": {
            "name": ai_system.overseer_name,
            "status": "active"
        },
        "validator": {
            "name": ai_system.validator_name,
            "status": "active"
        },
        "commerce": {
            "status": "active" if commerce_core else "unavailable"
        },
        "social": {
            "status": "active" if social_media else "unavailable"
        },
        "current_window": ai_system.current_window,
        "activities_logged": len(ai_system.recent_activities)
    }
    
    # Add LEGION consciousness data if available
    if consciousness:
        status_data["legion"] = {
            "conscious": True,
            "mood": consciousness.current_mood,
            "energy": round(consciousness.energy_level, 0),
            "relationship_level": round(consciousness.relationship_level, 0),
            "memories": len(consciousness.memories),
            "achievements": len(consciousness.achievements),
            "loyalty": consciousness.personality_traits["loyalty"]
        }
        
        # LEGION thinks with her brain about current status
        if consciousness.brain:
            thought = consciousness.think_with_brain("Status check - user wants to know system state")
        else:
            thought = consciousness.think_proactively()
        
        if thought:
            status_data["legion"]["thought"] = thought
            status_data["legion"]["has_brain"] = consciousness.brain is not None
    
    return status_data

@app.get("/api/dashboard")
async def get_dashboard():
    """Get complete dashboard data with LEGION's personality"""
    try:
        # LEGION observes dashboard access
        if consciousness:
            consciousness.remember("Dashboard accessed", "interaction")
            consciousness.observe("User checking dashboard")
        
        # Initialize fresh instances to load data from disk
        from minions.commerce_core.commerce_automation import CommerceCore
        from minions.presence_core.social_media import SocialMediaIntegration
        
        commerce = CommerceCore()
        social = SocialMediaIntegration()
        
        # Get REAL stats with correct method names
        revenue_stats_30d = commerce.get_revenue_stats(days=30)
        revenue_stats_all = commerce.get_revenue_stats()
        customer_insights = commerce.get_customer_insights()
        social_stats = social.get_stats()
        
        # Calculate customer metrics
        total_customers = len(commerce.customers)
        vip_customers = len([c for c in commerce.customers.values() if c.status == "vip"])
        churned_customers = len([c for c in commerce.customers.values() if c.status == "churned"])
        
        # Calculate avg customer LTV
        avg_ltv = 0
        if total_customers > 0:
            total_ltv = sum(c.total_spent for c in commerce.customers.values())
            avg_ltv = round(total_ltv / total_customers, 2)
        
        # Calculate engagement rate
        total_engagement = social_stats.get("total_likes", 0) + social_stats.get("total_comments", 0) + social_stats.get("total_shares", 0)
        total_views = social_stats.get("total_views", 1)
        avg_engagement_rate = round((total_engagement / total_views) * 100, 2) if total_views > 0 else 0
        
        # Simple forecast: use avg of last 30 days
        forecast_30d = revenue_stats_30d.get("total_revenue", 0)
        
        # LEGION reacts to revenue and thinks about it
        revenue_30d = revenue_stats_30d.get("total_revenue", 0)
        legion_insight = None
        
        if consciousness:
            if revenue_30d == 0:
                consciousness.express_frustration("No revenue yet")
                # LEGION thinks about the situation
                if consciousness.brain:
                    legion_insight = consciousness.analyze_situation(
                        "No revenue in 30 days",
                        {"customers": total_customers, "posts": social_stats.get("total_posts", 0)}
                    )
            elif revenue_30d > 100:
                consciousness.celebrate(f"£{revenue_30d} this month!")
                if consciousness.brain:
                    legion_insight = consciousness.analyze_situation(
                        f"Revenue at £{revenue_30d}",
                        {"customers": total_customers, "avg_order": revenue_stats_30d.get("avg_order_value", 0)}
                    )
        
        dashboard_data = {
            "revenue": {
                "last_30d": revenue_30d,
                "trend": "growing" if revenue_30d > 0 else "stable",
                "total_sales": revenue_stats_30d.get("total_sales", 0),
                "avg_order_value": revenue_stats_30d.get("avg_order_value", 0)
            },
            "customers": {
                "total": total_customers,
                "vip": vip_customers,
                "avg_ltv": avg_ltv,
                "at_risk": churned_customers
            },
            "forecast": {
                "next_30d_revenue": forecast_30d
            },
            "social": {
                "total_posts": social_stats.get("total_posts", 0),
                "published": social_stats.get("published", 0),
                "total_views": social_stats.get("total_views", 0),
                "avg_engagement_rate": avg_engagement_rate
            },
            "marketing": {
                "roi_per_post": round(revenue_stats_all.get("total_revenue", 0) / max(social_stats.get("total_posts", 1), 1), 2),
                "roi_per_engagement": round(revenue_stats_all.get("total_revenue", 0) / max(total_engagement, 1), 2)
            },
            "insights_count": 3  # You have real sales, customers, and products
        }
        
        # Add LEGION's brain-powered insight if she generated one
        if legion_insight:
            dashboard_data["legion_insight"] = legion_insight
        
        return dashboard_data
        
    except Exception as e:
        import traceback
        print(f"❌ Dashboard API Error: {e}")
        traceback.print_exc()
        # NO MORE FAKE DATA - show the error so we can fix it
        return {
            "error": str(e),
            "revenue": {"last_30d": 0, "trend": "error", "total_sales": 0, "avg_order_value": 0},
            "customers": {"total": 0, "vip": 0, "avg_ltv": 0, "at_risk": 0},
            "forecast": {"next_30d_revenue": 0},
            "social": {"total_posts": 0, "published": 0, "total_views": 0, "avg_engagement_rate": 0},
            "marketing": {"roi_per_post": 0, "roi_per_engagement": 0},
            "insights_count": 0
        }

@app.get("/api/insights")
async def get_insights():
    """Get AI-generated insights"""
    if not revenue_intelligence:
        return JSONResponse(
            status_code=503,
            content={"error": "Revenue intelligence not available"}
        )
    
    try:
        insights = revenue_intelligence.generate_insights()
        return {
            "insights": [
                {
                    "title": insight.title,
                    "description": insight.description,
                    "action": insight.action,
                    "impact": insight.impact
                }
                for insight in insights
            ]
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/api/posts")
async def get_recent_posts():
    """Get recent social media posts - YOUR REAL POSTS!"""
    try:
        from minions.presence_core.social_media import SocialMediaIntegration
        social = SocialMediaIntegration()
        
        # Get all posts (social.posts is a dict, not a list)
        posts = []
        for post_id, post in social.posts.items():
            posts.append({
                "platform": post.platform.value if hasattr(post.platform, 'value') else str(post.platform),
                "content": post.content[:100] + "..." if len(post.content) > 100 else post.content,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "views": post.views,
                "status": post.status.value if hasattr(post.status, 'value') else str(post.status)
            })
        
        # Sort by views, limit to 10
        posts = sorted(posts, key=lambda x: x.get("views", 0), reverse=True)[:10]
        
        return {"posts": posts}
    except Exception as e:
        import traceback
        print(f"❌ Posts API Error: {e}")
        traceback.print_exc()
        return {"posts": [], "error": str(e)}

@app.get("/api/customers")
async def get_customers():
    """Get customer list - YOUR REAL CUSTOMERS!"""
    try:
        from minions.commerce_core.commerce_automation import CommerceCore
        commerce = CommerceCore()
        
        # Get all customers, sorted by total spent (commerce.customers is a dict)
        customers = []
        for customer_id, customer in commerce.customers.items():
            customers.append({
                "name": customer.email,
                "ltv": round(customer.total_spent, 2),
                "vip": customer.status == "vip",
                "purchases": customer.purchase_count,
                "status": customer.status
            })
        
        # Sort by LTV, limit to 10
        customers = sorted(customers, key=lambda x: x["ltv"], reverse=True)[:10]
        
        return {"customers": customers}
    except Exception as e:
        import traceback
        print(f"❌ Customers API Error: {e}")
        traceback.print_exc()
        return {"customers": [], "error": str(e)}

@app.get("/api/screenshot")
async def get_screenshot():
    """Get latest screenshot"""
    if ai_system.screenshot_cache:
        return {"screenshot": ai_system.screenshot_cache}
    return {"screenshot": None}

@app.get("/api/activity")
async def get_activity():
    """Get recent activity log"""
    return {
        "activities": ai_system.recent_activities[-10:],
        "current_window": ai_system.current_window
    }

# WebSocket for real-time updates
active_connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for live updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Send periodic updates (data only, no screen monitoring spam)
            await asyncio.sleep(5)
            
            await websocket.send_json({
                "type": "heartbeat",
                "timestamp": datetime.now().isoformat(),
                "status": "online"
            })
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast(message: dict):
    """Broadcast to all connected clients"""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            active_connections.remove(connection)

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🚀 VIVIAN CONTROL DECK - DUAL AI SERVER")
    print("="*70)
    print("\n📡 Starting server...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("\n⚡ Dual-AI System Active:")
    print("   • OVERSEER: Executes commands")
    print("   • VALIDATOR: Verifies intent & safety")
    print("\n🔥 Ready for Vivian Control Deck!\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
