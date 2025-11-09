"""
TikTok Video Creator
Create short-form videos for TikTok, Instagram Reels, YouTube Shorts
"""

try:
    # MoviePy 2.x import structure
    from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
except ImportError:
    # Fallback for MoviePy 1.x
    from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
from colorama import Fore, Style, init
import cv2

init(autoreset=True)


class TikTokVideoCreator:
    """Create TikTok-style videos"""
    
    def __init__(self, output_dir: str = "./social_media_content"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # TikTok dimensions (9:16 aspect ratio)
        self.width = 1080
        self.height = 1920
        self.size = (self.width, self.height)
    
    def create_text_video(self,
                         texts: list,
                         duration_per_text: float = 3.0,
                         bg_color: str = "#000000",
                         text_color: str = "#FFFFFF",
                         output_filename: str = "tiktok_text_video.mp4") -> str:
        """
        Create a video with text slides
        Perfect for motivational quotes, tips, facts, etc.
        """
        
        print(f"{Fore.CYAN}Creating text video...{Style.RESET_ALL}")
        
        clips = []
        
        for i, text in enumerate(texts):
            print(f"  Creating slide {i+1}/{len(texts)}: {text[:30]}...")
            
            # Create image with text
            img = Image.new('RGB', self.size, bg_color)
            draw = ImageDraw.Draw(img)
            
            # Load font
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 80)
            except:
                font = ImageFont.load_default()
            
            # Word wrap
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] > self.width - 100:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text centered
            line_height = 100
            total_height = len(lines) * line_height
            y = (self.height - total_height) // 2
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (self.width - text_width) // 2
                draw.text((x, y), line, fill=text_color, font=font)
                y += line_height
            
            # Convert to numpy array
            frame = np.array(img)
            
            # Create video clip
            clip = ImageClip(frame, duration=duration_per_text)
            clips.append(clip)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Write video
        output_path = self.output_dir / output_filename
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio=False,
            
            logger=None
        )
        
        print(f"{Fore.GREEN}✓ Video created: {output_path}{Style.RESET_ALL}")
        return str(output_path)
    
    def create_slideshow_video(self,
                              image_paths: list,
                              duration_per_image: float = 2.0,
                              transition: str = "fade",
                              output_filename: str = "tiktok_slideshow.mp4") -> str:
        """
        Create a slideshow video from images
        Great for product showcases, before/after, tutorials
        """
        
        print(f"{Fore.CYAN}Creating slideshow video...{Style.RESET_ALL}")
        
        clips = []
        
        for i, img_path in enumerate(image_paths):
            print(f"  Processing image {i+1}/{len(image_paths)}...")
            
            # Load and resize image
            img = Image.open(img_path)
            
            # Resize to fit TikTok dimensions
            img_ratio = img.width / img.height
            target_ratio = self.width / self.height
            
            if img_ratio > target_ratio:
                # Image is wider, fit by height
                new_height = self.height
                new_width = int(new_height * img_ratio)
            else:
                # Image is taller, fit by width
                new_width = self.width
                new_height = int(new_width / img_ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop to exact size
            left = (new_width - self.width) // 2
            top = (new_height - self.height) // 2
            img = img.crop((left, top, left + self.width, top + self.height))
            
            # Convert to clip
            frame = np.array(img)
            clip = ImageClip(frame, duration=duration_per_image)
            
            if transition == "fade" and i > 0:
                clip = clip.crossfadein(0.5)
            
            clips.append(clip)
        
        # Concatenate
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Write video
        output_path = self.output_dir / output_filename
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio=False,
            
            logger=None
        )
        
        print(f"{Fore.GREEN}✓ Slideshow created: {output_path}{Style.RESET_ALL}")
        return str(output_path)
    
    def create_countdown_video(self,
                              title: str,
                              items: list,
                              duration_per_item: float = 3.0,
                              bg_color: str = "#1a1a2e",
                              output_filename: str = "tiktok_countdown.mp4") -> str:
        """
        Create a countdown/list video
        Perfect for "Top 5 Tips", "3 Secrets", etc.
        """
        
        print(f"{Fore.CYAN}Creating countdown video...{Style.RESET_ALL}")
        
        clips = []
        
        # Title slide
        print(f"  Creating title slide...")
        title_img = self._create_text_frame(title, bg_color, "#FFD700", 100)
        title_clip = ImageClip(title_img, duration=2.0)
        clips.append(title_clip)
        
        # Countdown items
        for i, item in enumerate(items):
            number = len(items) - i
            print(f"  Creating slide #{number}...")
            
            text = f"#{number}\n\n{item}"
            frame = self._create_text_frame(text, bg_color, "#FFFFFF", 70)
            clip = ImageClip(frame, duration=duration_per_item)
            clips.append(clip)
        
        # Concatenate
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Write video
        output_path = self.output_dir / output_filename
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio=False,
            
            logger=None
        )
        
        print(f"{Fore.GREEN}✓ Countdown video created: {output_path}{Style.RESET_ALL}")
        return str(output_path)
    
    def create_animated_text_video(self,
                                  text: str,
                                  duration: float = 5.0,
                                  bg_color: str = "#667eea",
                                  output_filename: str = "tiktok_animated.mp4") -> str:
        """
        Create a simple animated text video
        Text zooms in for emphasis
        """
        
        print(f"{Fore.CYAN}Creating animated text video...{Style.RESET_ALL}")
        
        # Create base frame
        base_img = self._create_text_frame(text, bg_color, "#FFFFFF", 90)
        
        # Create clip with zoom effect
        clip = ImageClip(base_img, duration=duration)
        
        # Add zoom animation
        clip = clip.resize(lambda t: 1 + 0.3 * (t / duration))
        clip = clip.set_position('center')
        
        # Create background
        bg = ColorClip(size=self.size, color=self._hex_to_rgb(bg_color), duration=duration)
        
        # Composite
        final_video = CompositeVideoClip([bg, clip], size=self.size)
        
        # Write video
        output_path = self.output_dir / output_filename
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio=False,
            
            logger=None
        )
        
        print(f"{Fore.GREEN}✓ Animated video created: {output_path}{Style.RESET_ALL}")
        return str(output_path)
    
    def _create_text_frame(self, text: str, bg_color: str, text_color: str, font_size: int) -> np.ndarray:
        """Helper to create a frame with text"""
        
        img = Image.new('RGB', self.size, bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Word wrap
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] > self.width - 100:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw text
        line_height = font_size + 20
        total_height = len(lines) * line_height
        y = (self.height - total_height) // 2
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            
            # Add shadow for better readability
            draw.text((x + 3, y + 3), line, fill="#000000", font=font)
            draw.text((x, y), line, fill=text_color, font=font)
            y += line_height
        
        return np.array(img)
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# Demo
if __name__ == "__main__":
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🎬 TIKTOK VIDEO CREATOR 🎬{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    creator = TikTokVideoCreator()
    
    # Example 1: Motivational quotes video
    print(f"{Fore.YELLOW}Example 1: Creating motivational quotes video{Style.RESET_ALL}\n")
    quotes = [
        "NEVER GIVE UP",
        "SUCCESS IS A JOURNEY",
        "DREAM BIG",
        "WORK HARD",
        "STAY POSITIVE"
    ]
    video1 = creator.create_text_video(quotes, duration_per_text=2.5, bg_color="#000000", text_color="#00FF00")
    
    # Example 2: Top 3 tips video
    print(f"\n{Fore.YELLOW}Example 2: Creating countdown/tips video{Style.RESET_ALL}\n")
    tips = [
        "Start with a strong hook",
        "Keep it under 60 seconds",
        "Add trending music"
    ]
    video2 = creator.create_countdown_video(
        "TOP 3 TIKTOK TIPS",
        tips,
        duration_per_item=3.0,
        bg_color="#FF6B6B"
    )
    
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ TikTok videos ready!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Videos saved in:{Style.RESET_ALL} {creator.output_dir}")
    print(f"\n{Fore.CYAN}Upload to TikTok, Instagram Reels, or YouTube Shorts!{Style.RESET_ALL}\n")
