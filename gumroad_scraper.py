"""
Gumroad Product Scraper
Goes to your Gumroad account and lists all your products
"""

import webbrowser
import time
from screen_vision import ScreenVision
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import pyautogui

init(autoreset=True)


def scrape_gumroad_products(username):
    """
    Scrape products from a Gumroad profile
    
    Args:
        username: Your Gumroad username or profile URL
    """
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📦 GUMROAD PRODUCT SCRAPER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    # Build the URL
    if username.startswith('http'):
        url = username
    else:
        url = f"https://{username}.gumroad.com"
    
    print(f"\n{Fore.YELLOW}Opening your Gumroad: {url}{Style.RESET_ALL}")
    
    try:
        # Method 1: Try to scrape the public page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print(f"{Fore.GREEN}✓ Successfully loaded Gumroad page!{Style.RESET_ALL}")
            
            # Try to find products - Gumroad uses different structures
            products = []
            
            # Look for product containers
            product_elements = soup.find_all(['a', 'div'], class_=lambda x: x and ('product' in x.lower() or 'item' in x.lower()))
            
            # Also search for product titles in the page
            titles = soup.find_all(['h1', 'h2', 'h3', 'h4'], class_=lambda x: x and 'title' in str(x).lower())
            
            # Extract product information
            for element in product_elements[:10]:  # First 10 products
                title = element.get_text(strip=True)
                link = element.get('href', '')
                
                if title and len(title) > 5 and len(title) < 200:  # Filter out junk
                    products.append({
                        'title': title,
                        'link': link if link.startswith('http') else f"https://gumroad.com{link}"
                    })
            
            # Display products
            if products:
                print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}📦 FOUND {len(products)} PRODUCTS ON YOUR GUMROAD:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
                
                for i, product in enumerate(products, 1):
                    print(f"{Fore.CYAN}{i}. {product['title']}{Style.RESET_ALL}")
                    if product['link']:
                        print(f"   {Fore.YELLOW}Link: {product['link']}{Style.RESET_ALL}")
                    print()
                
                return products
            else:
                print(f"\n{Fore.YELLOW}⚠️ Couldn't find products with automatic scraping{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Let me try the visual method...{Style.RESET_ALL}")
                
        else:
            print(f"{Fore.YELLOW}⚠️ Couldn't access page (status {response.status_code}){Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.YELLOW}⚠️ Scraping error: {e}{Style.RESET_ALL}")
    
    # Method 2: Open browser and use screen vision
    print(f"\n{Fore.CYAN}Using visual method - opening browser...{Style.RESET_ALL}")
    webbrowser.open(url)
    
    print(f"{Fore.YELLOW}Waiting for page to load...{Style.RESET_ALL}")
    time.sleep(3)
    
    # Take screenshot and analyze
    vision = ScreenVision()
    print(f"\n{Fore.CYAN}Taking screenshot of your Gumroad...{Style.RESET_ALL}")
    analysis = vision.describe_screen()
    
    # Try to extract product names from OCR
    if analysis['text'] and '[OCR' not in analysis['text']:
        print(f"\n{Fore.GREEN}✓ I can see your screen!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Text visible on your Gumroad page:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{analysis['text'][:1000]}{Style.RESET_ALL}")
        
        # Save the full text for analysis
        with open('gumroad_content.txt', 'w', encoding='utf-8') as f:
            f.write(analysis['text'])
        
        print(f"\n{Fore.GREEN}✓ Saved full page content to: gumroad_content.txt{Style.RESET_ALL}")
        
        return analysis['text']
    else:
        print(f"\n{Fore.YELLOW}⚠️ OCR not available. Install Tesseract for text reading.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ But I took a screenshot - check screenshots folder!{Style.RESET_ALL}")
        
        return None


# Interactive mode
if __name__ == "__main__":
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🎯 GUMROAD PRODUCT LISTER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    # Ask for Gumroad username
    print(f"\n{Fore.YELLOW}Enter your Gumroad username or profile URL:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Examples:{Style.RESET_ALL}")
    print(f"  - username (if your profile is username.gumroad.com)")
    print(f"  - https://yourname.gumroad.com")
    print(f"  - https://gumroad.com/yourname")
    
    username = input(f"\n{Fore.GREEN}Your Gumroad: {Style.RESET_ALL}").strip()
    
    if username:
        products = scrape_gumroad_products(username)
        
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ DONE! Check the results above.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}No username provided.{Style.RESET_ALL}")
