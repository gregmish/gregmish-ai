"""
Media Creation Tools - Images & Videos for Social Media
Create graphics, edit images, make videos for Instagram, TikTok, YouTube, etc.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import os


class MediaCreator:
    """Tools for creating social media content"""
    
    def __init__(self, output_dir: str = "./social_media_content"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Social media dimensions
        self.sizes = {
            "instagram_post": (1080, 1080),
            "instagram_story": (1080, 1920),
            "youtube_thumbnail": (1280, 720),
            "tiktok": (1080, 1920),
            "twitter_post": (1200, 675),
            "facebook_post": (1200, 630),
        }
    
    def create_text_image(self, 
                         text: str,
                         platform: str = "instagram_post",
                         bg_color: str = "#1a1a2e",
                         text_color: str = "#eaeaea",
                         font_size: int = 80,
                         filename: Optional[str] = None) -> str:
        """Create an image with text for social media"""
        
        size = self.sizes.get(platform, (1080, 1080))
        
        # Create image
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default
        try:
            # Common Windows fonts
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
                "C:/Windows/Fonts/segoeui.ttf",
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Word wrap text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] > size[0] - 100:  # Leave margin
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total height and starting position
        line_height = font_size + 20
        total_height = len(lines) * line_height
        y = (size[1] - total_height) // 2
        
        # Draw text centered
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (size[0] - text_width) // 2
            draw.text((x, y), line, fill=text_color, font=font)
            y += line_height
        
        # Save
        if not filename:
            filename = f"{platform}_{text[:20].replace(' ', '_')}.png"
        
        output_path = self.output_dir / filename
        img.save(output_path)
        
        return str(output_path)
    
    def create_gradient_background(self,
                                   platform: str = "instagram_post",
                                   color1: Tuple[int, int, int] = (255, 0, 150),
                                   color2: Tuple[int, int, int] = (0, 200, 255),
                                   filename: Optional[str] = None) -> str:
        """Create a gradient background image"""
        
        size = self.sizes.get(platform, (1080, 1080))
        
        # Create gradient
        gradient = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        
        for i in range(size[1]):
            ratio = i / size[1]
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            gradient[i, :] = [b, g, r]  # OpenCV uses BGR
        
        # Convert to PIL and save
        img = Image.fromarray(cv2.cvtColor(gradient, cv2.COLOR_BGR2RGB))
        
        if not filename:
            filename = f"{platform}_gradient.png"
        
        output_path = self.output_dir / filename
        img.save(output_path)
        
        return str(output_path)
    
    def add_text_to_image(self,
                         image_path: str,
                         text: str,
                         position: str = "bottom",
                         text_color: str = "white",
                         bg_opacity: float = 0.7,
                         output_filename: Optional[str] = None) -> str:
        """Add text overlay to an existing image"""
        
        img = Image.open(image_path)
        
        # Create overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Load font
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        padding = 40
        if position == "bottom":
            x = (img.width - text_width) // 2
            y = img.height - text_height - padding * 2
        elif position == "top":
            x = (img.width - text_width) // 2
            y = padding
        else:  # center
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
        
        # Draw background rectangle
        bg_alpha = int(255 * bg_opacity)
        draw.rectangle(
            [(x - padding, y - padding), 
             (x + text_width + padding, y + text_height + padding)],
            fill=(0, 0, 0, bg_alpha)
        )
        
        # Draw text
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Composite
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        # Save
        if not output_filename:
            output_filename = f"text_overlay_{Path(image_path).stem}.png"
        
        output_path = self.output_dir / output_filename
        img.save(output_path)
        
        return str(output_path)
    
    def create_video_from_images(self,
                                image_paths: list,
                                duration_per_image: float = 3.0,
                                output_filename: Optional[str] = None,
                                fps: int = 30) -> str:
        """Create a video slideshow from images"""
        
        if not output_filename:
            output_filename = "slideshow_video.mp4"
        
        output_path = self.output_dir / output_filename
        
        # Load first image to get dimensions
        first_img = cv2.imread(image_paths[0])
        height, width = first_img.shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Add each image for specified duration
        frames_per_image = int(fps * duration_per_image)
        
        for img_path in image_paths:
            img = cv2.imread(img_path)
            if img is None:
                continue
            
            # Resize if needed
            if img.shape[:2] != (height, width):
                img = cv2.resize(img, (width, height))
            
            # Write frames
            for _ in range(frames_per_image):
                out.write(img)
        
        out.release()
        
        return str(output_path)
    
    def apply_filter(self,
                    image_path: str,
                    filter_type: str = "blur",
                    output_filename: Optional[str] = None) -> str:
        """Apply Instagram-style filters to images"""
        
        img = Image.open(image_path)
        
        if filter_type == "blur":
            img = img.filter(ImageFilter.GaussianBlur(radius=2))
        
        elif filter_type == "sharpen":
            img = img.filter(ImageFilter.SHARPEN)
        
        elif filter_type == "vintage":
            # Sepia tone
            img = img.convert('RGB')
            pixels = img.load()
            for i in range(img.width):
                for j in range(img.height):
                    r, g, b = pixels[i, j]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    pixels[i, j] = (min(tr, 255), min(tg, 255), min(tb, 255))
        
        elif filter_type == "bright":
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.3)
        
        elif filter_type == "contrast":
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
        
        elif filter_type == "bw":
            img = img.convert('L').convert('RGB')
        
        # Save
        if not output_filename:
            output_filename = f"{filter_type}_{Path(image_path).stem}.png"
        
        output_path = self.output_dir / output_filename
        img.save(output_path)
        
        return str(output_path)
    
    def create_thumbnail(self,
                        text: str,
                        subtitle: str = "",
                        bg_color: str = "#FF6B6B",
                        filename: Optional[str] = None) -> str:
        """Create a YouTube thumbnail"""
        
        size = self.sizes["youtube_thumbnail"]
        
        # Create gradient background
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 100)
            subtitle_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 50)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Draw title
        bbox = draw.textbbox((0, 0), text, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2
        y = size[1] // 3
        
        # Add shadow
        draw.text((x + 5, y + 5), text, fill="black", font=title_font)
        draw.text((x, y), text, fill="white", font=title_font)
        
        # Draw subtitle
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            text_width = bbox[2] - bbox[0]
            x = (size[0] - text_width) // 2
            y = size[1] * 2 // 3
            
            draw.text((x + 3, y + 3), subtitle, fill="black", font=subtitle_font)
            draw.text((x, y), subtitle, fill="yellow", font=subtitle_font)
        
        # Save
        if not filename:
            filename = f"thumbnail_{text[:20].replace(' ', '_')}.png"
        
        output_path = self.output_dir / filename
        img.save(output_path)
        
        return str(output_path)


# Simple command-line interface for testing
if __name__ == "__main__":
    from colorama import Fore, Style, init
    init(autoreset=True)
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🎨 MEDIA CREATOR - Social Media Content Tools 🎨{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    creator = MediaCreator()
    
    # Demo: Create various content
    print(f"{Fore.YELLOW}Creating sample content...{Style.RESET_ALL}\n")
    
    # Instagram post
    img1 = creator.create_text_image(
        "Follow Your Dreams",
        platform="instagram_post",
        bg_color="#667eea",
        text_color="#ffffff"
    )
    print(f"{Fore.GREEN}✓ Created Instagram post:{Style.RESET_ALL} {img1}")
    
    # YouTube thumbnail
    img2 = creator.create_thumbnail(
        "AMAZING AI",
        subtitle="You Won't Believe This!",
        bg_color="#FF0000"
    )
    print(f"{Fore.GREEN}✓ Created YouTube thumbnail:{Style.RESET_ALL} {img2}")
    
    # Gradient background
    img3 = creator.create_gradient_background(
        platform="instagram_story",
        color1=(255, 107, 107),
        color2=(78, 205, 196)
    )
    print(f"{Fore.GREEN}✓ Created gradient background:{Style.RESET_ALL} {img3}")
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}All files saved to:{Style.RESET_ALL} {creator.output_dir}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
