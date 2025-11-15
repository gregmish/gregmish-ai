"""
Web Dashboard - Actually works now
Uses the real agent_core that actually DOES things
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import json
from pathlib import Path
from core.agent_core import get_agent

app = FastAPI(title="GregMish AI Dashboard")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    """Serve the dashboard"""
    return FileResponse("vivian_ui.html")


@app.get("/api/status")
async def status():
    """System status"""
    return {
        "status": "online",
        "agent": "ready",
        "tools": ["browser", "gumroad", "social"]
    }


@app.get("/api/dashboard")
async def get_dashboard():
    """Get dashboard data from REAL scraped Gumroad"""
    try:
        # Load actual scraped data
        sales_file = Path("minions/commerce_core/data/sales.json")
        
        if not sales_file.exists():
            return {
                "revenue": {"last_30d": 0, "total_sales": 0},
                "customers": {"total": 0},
                "products": {"count": 0},
                "message": "Run 'python greg_agent.py --test \"check gumroad\"' first"
            }
        
        with open(sales_file, 'r') as f:
            products = json.load(f)
        
        # Calculate real stats
        total_revenue = sum(p['revenue'] for p in products)
        total_sales = sum(p['sales'] for p in products)
        total_products = len(products)
        
        # Products with sales
        products_with_sales = [p for p in products if p['sales'] > 0]
        
        return {
            "revenue": {
                "last_30d": round(total_revenue, 2),
                "total_sales": total_sales,
                "avg_order_value": round(total_revenue / total_sales, 2) if total_sales > 0 else 0
            },
            "customers": {
                "total": total_sales,  # Each sale is a customer
                "vip": len([p for p in products if p['sales'] > 5])
            },
            "products": {
                "count": total_products,
                "active": len(products_with_sales),
                "top_sellers": sorted(products_with_sales, key=lambda x: x['revenue'], reverse=True)[:3]
            },
            "insights": [
                f"You have {total_products} products",
                f"Total revenue: £{total_revenue:.2f}",
                f"{len(products_with_sales)} products have made sales"
            ]
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint - actually DOES things via agent_core"""
    try:
        agent = get_agent()
        
        # Execute the command through the real agent
        result = agent.execute_command(request.message)
        
        # Format response
        if result['status'] == 'completed':
            # Get the actual result
            if result['results']:
                last_result = result['results'][-1]
                data = last_result.get('data', {})
                
                # Format based on what was done
                if 'products' in data:
                    response = f"✅ Found {data['product_count']} products with total revenue of £{data['total_revenue']}"
                elif 'response' in data:
                    response = data['response']
                else:
                    response = f"✅ Done! {last_result.get('summary', '')}"
            else:
                response = "✅ Done!"
        else:
            # Partial completion - show what failed
            response = "⚠️ Partially completed. "
            for i, r in enumerate(result['results']):
                if r['status'] == 'error':
                    response += f"Step {i+1} failed: {r.get('error', 'Unknown error')}. "
        
        return {
            "response": response,
            "full_result": result
        }
    
    except Exception as e:
        import traceback
        return JSONResponse(
            status_code=500,
            content={
                "response": f"❌ Error: {str(e)}",
                "traceback": traceback.format_exc()
            }
        )


@app.post("/api/execute")
async def execute_command(request: ChatRequest):
    """Execute a command and return structured result"""
    try:
        agent = get_agent()
        result = agent.execute_command(request.message)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    print("\n🌐 Starting dashboard on http://localhost:8000")
    print("📊 Dashboard: http://localhost:8000")
    print("🤖 Chat: POST to http://localhost:8000/api/chat")
    print("\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
