"""
Generate PROFESSIONAL photorealistic images using FREE online AI APIs
"""

import requests
from PIL import Image
from io import BytesIO
import time

def generate_cat_image():
    """Generate a PROFESSIONAL photorealistic cat using free AI API"""
    print("🤖 Generating professional photorealistic image with AI...")
    
    try:
        # Use Pollinations.ai - FREE unlimited AI image generation
        prompt = "professional photo of a cute realistic cat drinking milk from a white ceramic saucer, photorealistic, high quality, detailed fur, natural lighting, 8k, masterpiece"
        
        # Pollinations.ai free API - no key needed
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
        
        print("📡 Calling AI image generator...")
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            # Save the image
            image = Image.open(BytesIO(response.content))
            image_path = "cat_drinking_milk.png"
            image.save(image_path)
            print(f"✅ Professional AI image saved: {image_path}")
            return image_path
        else:
            print(f"❌ API returned status {response.status_code}")
            return generate_simple_cat()
            
    except Exception as e:
        print(f"❌ Error with AI generation: {e}")
        print("📝 Falling back to simple drawing...")
        return generate_simple_cat()

def generate_simple_cat():
    """Fallback: Generate simple cat drawing if AI fails"""
    from PIL import Image, ImageDraw
    
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Simple but better looking cat
    # Head
    draw.ellipse([300, 150, 500, 350], outline='black', fill='orange', width=3)
    
    # Ears
    draw.polygon([(330, 180), (300, 100), (360, 160)], fill='orange', outline='black', width=2)
    draw.polygon([(470, 180), (500, 100), (440, 160)], fill='orange', outline='black', width=2)
    
    # Eyes
    draw.ellipse([350, 220, 380, 250], fill='green', outline='black', width=2)
    draw.ellipse([420, 220, 450, 250], fill='green', outline='black', width=2)
    draw.ellipse([360, 230, 370, 240], fill='black')
    draw.ellipse([430, 230, 440, 240], fill='black')
    
    # Nose and mouth
    draw.polygon([(400, 270), (390, 285), (410, 285)], fill='pink')
    draw.arc([370, 280, 430, 310], 0, 180, fill='black', width=2)
    
    # Whiskers
    for y_offset in [-10, 0, 10]:
        draw.line([(320, 260 + y_offset), (250, 255 + y_offset)], fill='black', width=2)
        draw.line([(480, 260 + y_offset), (550, 255 + y_offset)], fill='black', width=2)
    
    # Body
    draw.ellipse([320, 340, 480, 520], fill='orange', outline='black', width=3)
    
    # Saucer with milk
    draw.ellipse([300, 520, 500, 570], fill='white', outline='black', width=3)
    draw.ellipse([320, 530, 480, 560], fill='lightblue', outline='blue', width=2)
    
    image_path = "cat_drinking_milk.png"
    image.save(image_path)
    print(f"✅ Image saved: {image_path}")
    return image_path

def open_image_in_paint(image_path):
    """Open the generated image in Paint"""
    import subprocess
    subprocess.Popen(['mspaint', image_path])
    print(f"✅ Opened {image_path} in Paint")

if __name__ == "__main__":
    print("🎨 Generating cat drinking milk image...")
    image_path = generate_cat_image()
    time.sleep(1)
    print("📂 Opening in Paint...")
    open_image_in_paint(image_path)
