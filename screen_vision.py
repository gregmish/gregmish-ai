"""
Screen Vision Tool
Allow AI to see and analyze what's on your screen
"""

import pyautogui
from PIL import Image
import pytesseract
from pathlib import Path
from colorama import Fore, Style, init
import cv2
import numpy as np
from datetime import datetime

init(autoreset=True)


class ScreenVision:
    """Give AI the ability to see your screen"""
    
    def __init__(self):
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Try to find Tesseract OCR (for reading text from images)
        # Common installation paths
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(Path.home().name)
        ]
        
        for path in tesseract_paths:
            if Path(path).exists():
                pytesseract.pytesseract.tesseract_cmd = path
                break
    
    def take_screenshot(self, region=None, save=True):
        """
        Take a screenshot of the entire screen or a specific region
        
        Args:
            region: Tuple of (x, y, width, height) for specific area, or None for full screen
            save: Whether to save the screenshot to disk
            
        Returns:
            PIL Image object
        """
        print(f"\n{Fore.CYAN}📸 Taking screenshot...{Style.RESET_ALL}")
        
        if region:
            screenshot = pyautogui.screenshot(region=region)
            print(f"{Fore.GREEN}✓ Captured region: {region}{Style.RESET_ALL}")
        else:
            screenshot = pyautogui.screenshot()
            screen_size = pyautogui.size()
            print(f"{Fore.GREEN}✓ Captured full screen: {screen_size.width}x{screen_size.height}{Style.RESET_ALL}")
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = self.screenshots_dir / filename
            screenshot.save(filepath)
            print(f"{Fore.GREEN}✓ Saved to: {filepath}{Style.RESET_ALL}")
        
        return screenshot
    
    def read_text_from_screen(self, region=None):
        """
        Use OCR to read text from screen
        
        Args:
            region: Tuple of (x, y, width, height) or None for full screen
            
        Returns:
            Extracted text as string
        """
        print(f"\n{Fore.CYAN}👁️ Reading text from screen...{Style.RESET_ALL}")
        
        screenshot = self.take_screenshot(region=region, save=False)
        
        try:
            # Use Tesseract OCR to extract text
            text = pytesseract.image_to_string(screenshot)
            
            if text.strip():
                print(f"{Fore.GREEN}✓ Found text ({len(text)} characters){Style.RESET_ALL}")
                return text
            else:
                print(f"{Fore.YELLOW}⚠️ No text detected{Style.RESET_ALL}")
                return ""
                
        except Exception as e:
            print(f"{Fore.RED}✗ OCR error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Tip: Install Tesseract OCR from: https://github.com/tesseract-ocr/tesseract{Style.RESET_ALL}")
            return f"[OCR not available: {e}]"
    
    def find_on_screen(self, image_path, confidence=0.8):
        """
        Find an image on the screen (useful for finding buttons, icons, etc.)
        
        Args:
            image_path: Path to the image to find
            confidence: How closely it needs to match (0.0 to 1.0)
            
        Returns:
            (x, y, width, height) of found image, or None
        """
        print(f"\n{Fore.CYAN}🔍 Searching for image on screen...{Style.RESET_ALL}")
        
        try:
            location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
            
            if location:
                print(f"{Fore.GREEN}✓ Found at: {location}{Style.RESET_ALL}")
                return location
            else:
                print(f"{Fore.YELLOW}⚠️ Image not found on screen{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}✗ Search error: {e}{Style.RESET_ALL}")
            return None
    
    def get_mouse_position(self):
        """Get current mouse position"""
        x, y = pyautogui.position()
        return (x, y)
    
    def get_screen_info(self):
        """Get information about the screen"""
        size = pyautogui.size()
        mouse_pos = self.get_mouse_position()
        
        info = {
            'screen_width': size.width,
            'screen_height': size.height,
            'mouse_x': mouse_pos[0],
            'mouse_y': mouse_pos[1]
        }
        
        return info
    
    def analyze_screen_colors(self, region=None):
        """
        Analyze dominant colors on screen
        
        Args:
            region: Tuple of (x, y, width, height) or None for full screen
            
        Returns:
            List of dominant colors
        """
        print(f"\n{Fore.CYAN}🎨 Analyzing screen colors...{Style.RESET_ALL}")
        
        screenshot = self.take_screenshot(region=region, save=False)
        
        # Convert PIL image to numpy array
        img_array = np.array(screenshot)
        
        # Convert RGB to BGR for OpenCV
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Reshape to list of pixels
        pixels = img_bgr.reshape(-1, 3)
        
        # Use k-means to find dominant colors
        from sklearn.cluster import KMeans
        
        n_colors = 5
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the dominant colors
        colors = kmeans.cluster_centers_.astype(int)
        
        # Convert BGR back to RGB
        colors_rgb = [[int(c[2]), int(c[1]), int(c[0])] for c in colors]
        
        print(f"{Fore.GREEN}✓ Found {n_colors} dominant colors{Style.RESET_ALL}")
        for i, color in enumerate(colors_rgb, 1):
            print(f"  Color {i}: RGB{tuple(color)} - #{color[0]:02x}{color[1]:02x}{color[2]:02x}")
        
        return colors_rgb
    
    def describe_screen(self):
        """
        Get a complete description of what's on screen
        Combines screenshot, OCR, and analysis
        """
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}👁️ AI VISION: Analyzing your screen...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Take screenshot
        screenshot = self.take_screenshot()
        
        # Get screen info
        info = self.get_screen_info()
        print(f"\n{Fore.YELLOW}Screen Resolution:{Style.RESET_ALL} {info['screen_width']}x{info['screen_height']}")
        print(f"{Fore.YELLOW}Mouse Position:{Style.RESET_ALL} ({info['mouse_x']}, {info['mouse_y']})")
        
        # Read text
        text = self.read_text_from_screen()
        
        if text and "[OCR not available" not in text:
            print(f"\n{Fore.YELLOW}Text found on screen:{Style.RESET_ALL}")
            # Show first 500 characters
            preview = text[:500] + "..." if len(text) > 500 else text
            print(f"{Fore.WHITE}{preview}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Screen analysis complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        
        return {
            'screenshot': screenshot,
            'screen_info': info,
            'text': text
        }
    
    def monitor_screen_changes(self, interval=1, duration=10):
        """
        Monitor screen for changes over time
        
        Args:
            interval: Seconds between screenshots
            duration: Total seconds to monitor
        """
        print(f"\n{Fore.CYAN}📹 Monitoring screen for {duration} seconds...{Style.RESET_ALL}")
        
        import time
        screenshots = []
        
        end_time = time.time() + duration
        count = 0
        
        while time.time() < end_time:
            screenshot = self.take_screenshot(save=False)
            screenshots.append(screenshot)
            count += 1
            print(f"{Fore.GREEN}✓ Captured frame {count}{Style.RESET_ALL}")
            time.sleep(interval)
        
        print(f"\n{Fore.GREEN}✓ Captured {count} screenshots{Style.RESET_ALL}")
        return screenshots


# Demo usage
if __name__ == "__main__":
    vision = ScreenVision()
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  👁️ SCREEN VISION DEMO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Example 1: Taking a screenshot{Style.RESET_ALL}")
    screenshot = vision.take_screenshot()
    
    print(f"\n{Fore.YELLOW}Example 2: Getting screen info{Style.RESET_ALL}")
    info = vision.get_screen_info()
    print(f"  Screen: {info['screen_width']}x{info['screen_height']}")
    print(f"  Mouse: ({info['mouse_x']}, {info['mouse_y']})")
    
    print(f"\n{Fore.YELLOW}Example 3: Reading text from screen (OCR){Style.RESET_ALL}")
    text = vision.read_text_from_screen()
    if text and not text.startswith("[OCR"):
        print(f"  Found {len(text)} characters of text")
        print(f"  Preview: {text[:100]}...")
    
    print(f"\n{Fore.YELLOW}Example 4: Complete screen analysis{Style.RESET_ALL}")
    analysis = vision.describe_screen()
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ AI can now see your screen!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 Your AI can now:{Style.RESET_ALL}")
    print(f"  ✓ Take screenshots of your screen")
    print(f"  ✓ Read text from any window (OCR)")
    print(f"  ✓ See what's in your browser")
    print(f"  ✓ Monitor screen changes")
    print(f"  ✓ Find images/buttons on screen")
    print(f"  ✓ Get mouse position")
