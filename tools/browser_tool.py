"""
Browser Tool - Actually DOES things in the browser
This is what WORKS - the core that actually scrapes and posts
"""

from playwright.sync_api import sync_playwright
import time
import subprocess
from typing import Dict, Any


class BrowserTool:
    """
    Browser automation that actually works
    - Uses Edge with user's auto-login
    - Actually scrapes data
    - Actually fills forms
    """
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
    
    def start(self):
        """Start Edge with user's profile"""
        print("🚀 Starting Edge browser...")
        
        # Close any existing Edge
        subprocess.run(['taskkill', '/F', '/IM', 'msedge.exe'], 
                     capture_output=True, shell=True)
        time.sleep(2)
        
        # Start Edge with remote debugging
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        user_data_dir = r"C:\Users\gregr\AppData\Local\Microsoft\Edge\User Data"
        
        subprocess.Popen([
            edge_path,
            f'--user-data-dir={user_data_dir}',
            '--remote-debugging-port=9222',
            '--profile-directory=Default',
            'about:blank'
        ])
        
        time.sleep(4)
        
        # Connect via Playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.connect_over_cdp("http://localhost:9222")
        
        if self.browser.contexts and self.browser.contexts[0].pages:
            self.page = self.browser.contexts[0].pages[0]
        else:
            self.page = self.browser.contexts[0].new_page()
        
        print("✅ Browser ready!")
    
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def check_gumroad_sales(self) -> Dict[str, Any]:
        """Actually scrape Gumroad - THIS WORKS"""
        print("📊 Scraping Gumroad...")
        
        try:
            if not self.page:
                self.start()
            
            self.page.goto("https://gumroad.com/products", wait_until="networkidle")
            time.sleep(3)
            
            products = []
            total_revenue = 0
            
            rows = self.page.locator('tbody tr').all()
            print(f"Found {len(rows)} products")
            
            for row in rows:
                try:
                    cells = row.locator('td').all()
                    if len(cells) < 5:
                        continue
                    
                    name = cells[1].inner_text().strip().split('\n')[0]
                    sales = cells[2].inner_text().strip()
                    revenue = cells[3].inner_text().strip()
                    price = cells[4].inner_text().strip()
                    
                    import re
                    revenue_num = float(re.search(r'[\d.]+', revenue).group()) if re.search(r'[\d.]+', revenue) else 0
                    price_num = float(re.search(r'[\d.]+', price).group()) if re.search(r'[\d.]+', price) else 0
                    sales_num = int(re.search(r'\d+', sales).group()) if re.search(r'\d+', sales) else 0
                    
                    total_revenue += revenue_num
                    
                    products.append({
                        "name": name,
                        "sales": sales_num,
                        "revenue": revenue_num,
                        "price": price_num
                    })
                    
                    print(f"  ✅ {name}: {sales_num} sales, £{revenue_num}")
                except:
                    continue
            
            # Save to file
            import json
            import os
            from pathlib import Path
            
            data_file = Path('minions/commerce_core/data/sales.json')
            data_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(data_file, 'w') as f:
                json.dump(products, f, indent=2)
            
            print(f"\n💰 Total Revenue: £{total_revenue}")
            print(f"📦 Saved {len(products)} products")
            
            return {
                "status": "success",
                "total_revenue": total_revenue,
                "products": products,
                "product_count": len(products)
            }
        
        except Exception as e:
            import traceback
            print(f"❌ Error: {e}")
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }
