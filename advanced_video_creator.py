"""
Advanced Video Creator - Like CapCut
Create professional TikTok/Reels videos with animations, transitions, effects
Uses AI voice, music, motion graphics, and advanced editing
"""

from moviepy import *
from moviepy import vfx
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
from pathlib import Path
from colorama import Fore, Style, init
import random
import textwrap

init(autoreset=True)


class AdvancedVideoCreator:
    """
    Professional video creator with CapCut-like features:
    - Smooth transitions (fade, zoom, slide)
    - Animated text (typewriter, bounce, glow)
    - Background music
    - Motion graphics
    - Filters and effects
    - Multiple text styles
    """
    
    def __init__(self):
        self.output_dir = Path("social_media_content")
        self.output_dir.mkdir(exist_ok=True)
        
        # Video settings
        self.width = 1080
        self.height = 1920
        self.fps = 30
        
        print(f"{Fore.GREEN}✓ Advanced Video Creator initialized{Style.RESET_ALL}")
    
    def create_zoom_animation(self, image_path, duration, zoom_factor=1.3):
        """Create a Ken Burns zoom effect on an image"""
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            h, w = frame.shape[:2]
            
            # Calculate zoom
            progress = t / duration
            current_zoom = 1 + (zoom_factor - 1) * progress
            
            # Zoom in
            new_h, new_w = int(h * current_zoom), int(w * current_zoom)
            
            # Resize
            from PIL import Image as PILImage
            pil_frame = PILImage.fromarray(frame)
            zoomed = pil_frame.resize((new_w, new_h), PILImage.Resampling.LANCZOS)
            
            # Crop to center
            left = (new_w - w) // 2
            top = (new_h - h) // 2
            cropped = zoomed.crop((left, top, left + w, top + h))
            
            return np.array(cropped)
        
        clip = ImageClip(str(image_path)).with_duration(duration)
        return clip.transform(zoom_effect)
    
    def create_text_clip_animated(self, text, duration, position='center', 
                                  font_size=80, color='white', bg_color=None,
                                  animation='fade'):
        """
        Create animated text with various effects
        
        Animations:
        - fade: Fade in/out
        - slide_up: Slide from bottom
        - slide_down: Slide from top
        - zoom: Zoom in effect
        - bounce: Bouncing text
        - glow: Glowing effect
        """
        
        # Create text image
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0) if not bg_color else bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to load a bold font
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Wrap text
        max_width = self.width - 100
        wrapped_lines = []
        for line in text.split('\n'):
            words = line.split()
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        wrapped_lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                wrapped_lines.append(' '.join(current_line))
        
        # Calculate text position
        y_offset = self.height // 2 - (len(wrapped_lines) * font_size) // 2
        
        # Draw each line centered
        for i, line in enumerate(wrapped_lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            y = y_offset + i * (font_size + 20)
            
            # Add shadow/outline for readability
            shadow_offset = 3
            draw.text((x + shadow_offset, y + shadow_offset), line, font=font, fill='black')
            draw.text((x, y), line, font=font, fill=color)
        
        # Save temporary image
        temp_path = self.output_dir / f"temp_text_{random.randint(1000,9999)}.png"
        img.save(temp_path)
        
        # Create clip
        clip = ImageClip(str(temp_path)).with_duration(duration)
        
        # Apply animation
        if animation == 'fade':
            # Fade in/out effect using opacity
            clip = clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
        elif animation == 'slide_up':
            clip = clip.with_position(lambda t: ('center', self.height - int((self.height * 0.8) * min(t * 2, 1))))
        elif animation == 'zoom':
            clip = clip.resized(lambda t: 0.5 + 0.5 * min(t * 2, 1))
        elif animation == 'bounce':
            def bounce_pos(t):
                if t < 0.3:
                    y = self.height - int(self.height * 0.5 * (t / 0.3))
                else:
                    y = self.height * 0.5
                return ('center', y)
            clip = clip.with_position(bounce_pos)
        
        # Clean up temp file later
        # temp_path.unlink(missing_ok=True)
        
        return clip
    
    def create_professional_video(self, scenes, output_filename="professional_video.mp4",
                                 bg_music=None, transition='fade'):
        """
        Create a professional video from multiple scenes
        
        Args:
            scenes: List of dicts with {'text': str, 'duration': float, 'bg_color': str, 'animation': str}
            output_filename: Output file name
            bg_music: Path to background music (optional)
            transition: Type of transition between scenes
        """
        
        print(f"\n{Fore.CYAN}🎬 Creating professional video with {len(scenes)} scenes...{Style.RESET_ALL}")
        
        clips = []
        
        for i, scene in enumerate(scenes):
            print(f"  Creating scene {i+1}/{len(scenes)}: {scene['text'][:30]}...")
            
            # Create background
            bg_color = scene.get('bg_color', '#000000')
            if bg_color.startswith('#'):
                # Convert hex to RGB
                bg_color = tuple(int(bg_color[j:j+2], 16) for j in (1, 3, 5))
            
            bg = ColorClip(size=(self.width, self.height), color=bg_color, 
                          duration=scene.get('duration', 3))
            
            # Create animated text
            text_clip = self.create_text_clip_animated(
                text=scene['text'],
                duration=scene.get('duration', 3),
                font_size=scene.get('font_size', 80),
                color=scene.get('text_color', 'white'),
                animation=scene.get('animation', 'fade')
            )
            
            # Composite
            scene_clip = CompositeVideoClip([bg, text_clip])
            
            # Add transition
            if transition == 'fade' and i > 0:
                scene_clip = scene_clip.with_effects([vfx.FadeIn(0.5)])
            
            clips.append(scene_clip)
        
        print(f"\n{Fore.YELLOW}Combining scenes...{Style.RESET_ALL}")
        
        # Concatenate with transitions
        if transition == 'fade':
            final_video = concatenate_videoclips(clips, method="compose", padding=-0.5)
        else:
            final_video = concatenate_videoclips(clips, method="compose")
        
        # Write video
        output_path = self.output_dir / output_filename
        print(f"\n{Fore.YELLOW}Rendering video... This may take a minute...{Style.RESET_ALL}")
        
        final_video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio=False,
            logger=None
        )
        
        print(f"\n{Fore.GREEN}✓ Professional video created: {output_path}{Style.RESET_ALL}")
        return str(output_path)
    
    def create_product_promo(self, product_name, features, price, 
                           call_to_action="Link in bio!",
                           output_filename="product_promo.mp4"):
        """
        Create a professional product promotional video
        """
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🎥 CREATING PRODUCT PROMO: {product_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        scenes = []
        
        # Scene 1: Hook/Attention grabber
        scenes.append({
            'text': '🔥 NEW DROP 🔥',
            'duration': 2,
            'bg_color': '#FF0000',
            'text_color': 'white',
            'font_size': 100,
            'animation': 'zoom'
        })
        
        # Scene 2: Product name
        scenes.append({
            'text': product_name,
            'duration': 3,
            'bg_color': '#000000',
            'text_color': '#FFD700',
            'font_size': 70,
            'animation': 'fade'
        })
        
        # Scene 3-N: Features (one per scene)
        colors = ['#FF1493', '#00CED1', '#FF4500', '#32CD32', '#8B00FF']
        for i, feature in enumerate(features[:5]):
            scenes.append({
                'text': f'✓ {feature}',
                'duration': 2.5,
                'bg_color': colors[i % len(colors)],
                'text_color': 'white',
                'font_size': 65,
                'animation': 'slide_up'
            })
        
        # Scene: Price
        scenes.append({
            'text': f'Only {price}!',
            'duration': 2,
            'bg_color': '#FFD700',
            'text_color': '#000000',
            'font_size': 90,
            'animation': 'bounce'
        })
        
        # Scene: Call to action
        scenes.append({
            'text': call_to_action,
            'duration': 2.5,
            'bg_color': '#00FF00',
            'text_color': '#000000',
            'font_size': 80,
            'animation': 'zoom'
        })
        
        return self.create_professional_video(scenes, output_filename, transition='fade')


# Demo
if __name__ == "__main__":
    creator = AdvancedVideoCreator()
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🎬 ADVANCED VIDEO CREATOR - LIKE CAPCUT{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Example: Creating professional product promo{Style.RESET_ALL}")
    
    video = creator.create_product_promo(
        product_name="50 Romantic Recipes",
        features=[
            "10 Countries",
            "World-Class Dinners",
            "Easy Instructions",
            "Beautiful Photos",
            "Instant Download"
        ],
        price="£1.99",
        call_to_action="Get it NOW!\nLink in bio! 👇",
        output_filename="gumroad_romantic_recipes.mp4"
    )
    
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ VIDEO READY!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}Your professional video is ready to upload to TikTok!{Style.RESET_ALL}")
