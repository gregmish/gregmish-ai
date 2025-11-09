"""
Social Media Poster
Post content to TikTok, Instagram, YouTube, Twitter/X, Facebook
"""

import os
from pathlib import Path
from colorama import Fore, Style, init
import webbrowser
import time
from urllib.parse import quote
import pyautogui
import pyperclip

init(autoreset=True)


class SocialMediaPoster:
    """Automate posting to social media platforms"""
    
    def __init__(self):
        self.content_dir = Path("social_media_content")
        self.content_dir.mkdir(exist_ok=True)
        
    def post_to_tiktok(self, video_path, caption="", hashtags=None):
        """
        Post video to TikTok via web browser
        Opens TikTok upload page and guides user through posting
        """
        print(f"\n{Fore.CYAN}📱 Posting to TikTok...{Style.RESET_ALL}")
        
        # Prepare caption with hashtags
        if hashtags:
            full_caption = f"{caption} " + " ".join([f"#{tag}" for tag in hashtags])
        else:
            full_caption = caption
            
        # Copy caption to clipboard
        pyperclip.copy(full_caption)
        print(f"{Fore.GREEN}✓ Caption copied to clipboard:{Style.RESET_ALL}")
        print(f"  {full_caption[:100]}...")
        
        # Open TikTok upload page
        tiktok_url = "https://www.tiktok.com/upload"
        print(f"\n{Fore.YELLOW}Opening TikTok upload page...{Style.RESET_ALL}")
        webbrowser.open(tiktok_url)
        
        print(f"\n{Fore.CYAN}📋 Instructions:{Style.RESET_ALL}")
        print(f"  1. Log in to TikTok if needed")
        print(f"  2. Click 'Select file' and choose: {video_path}")
        print(f"  3. Paste the caption (Ctrl+V) - already in your clipboard!")
        print(f"  4. Add any other details (cover, privacy settings)")
        print(f"  5. Click 'Post' when ready")
        
        return {
            'platform': 'TikTok',
            'video': str(video_path),
            'caption': full_caption,
            'status': 'Browser opened - manual upload required'
        }
    
    def post_to_instagram(self, media_path, caption="", hashtags=None, is_reel=False):
        """
        Post to Instagram via web browser
        Note: Instagram web has limited upload capabilities
        """
        print(f"\n{Fore.MAGENTA}📸 Posting to Instagram...{Style.RESET_ALL}")
        
        # Prepare caption with hashtags
        if hashtags:
            full_caption = f"{caption}\n\n" + " ".join([f"#{tag}" for tag in hashtags])
        else:
            full_caption = caption
            
        # Copy caption to clipboard
        pyperclip.copy(full_caption)
        print(f"{Fore.GREEN}✓ Caption copied to clipboard:{Style.RESET_ALL}")
        print(f"  {full_caption[:100]}...")
        
        # Open Instagram
        if is_reel:
            print(f"\n{Fore.YELLOW}Opening Instagram (Reels)...{Style.RESET_ALL}")
            print(f"\n{Fore.RED}⚠️  Instagram Reels require mobile app{Style.RESET_ALL}")
            print(f"  Options:")
            print(f"  1. Transfer {media_path} to your phone")
            print(f"  2. Open Instagram app > Create > Reel")
            print(f"  3. Upload the video and paste caption")
        else:
            webbrowser.open("https://www.instagram.com/")
            print(f"\n{Fore.CYAN}📋 Instructions:{Style.RESET_ALL}")
            print(f"  1. Log in to Instagram")
            print(f"  2. Click + (Create) > Post")
            print(f"  3. Select file: {media_path}")
            print(f"  4. Paste caption (Ctrl+V)")
            print(f"  5. Click 'Share'")
        
        return {
            'platform': 'Instagram' + (' Reels' if is_reel else ''),
            'media': str(media_path),
            'caption': full_caption,
            'status': 'Ready to upload'
        }
    
    def post_to_youtube_shorts(self, video_path, title, description="", hashtags=None):
        """
        Post to YouTube Shorts
        """
        print(f"\n{Fore.RED}▶️  Posting to YouTube Shorts...{Style.RESET_ALL}")
        
        # Prepare description with hashtags
        if hashtags:
            full_description = f"{description}\n\n" + " ".join([f"#{tag}" for tag in hashtags])
        else:
            full_description = description
            
        # Add #Shorts tag if not present
        if "#Shorts" not in full_description and "#shorts" not in full_description:
            full_description += " #Shorts"
        
        # Copy title to clipboard
        pyperclip.copy(title)
        print(f"{Fore.GREEN}✓ Title copied to clipboard:{Style.RESET_ALL} {title}")
        
        # Open YouTube Studio upload
        youtube_url = "https://studio.youtube.com/channel/UC/videos/upload"
        print(f"\n{Fore.YELLOW}Opening YouTube Studio...{Style.RESET_ALL}")
        webbrowser.open(youtube_url)
        
        print(f"\n{Fore.CYAN}📋 Instructions:{Style.RESET_ALL}")
        print(f"  1. Log in to YouTube if needed")
        print(f"  2. Click 'CREATE' > Upload videos")
        print(f"  3. Select file: {video_path}")
        print(f"  4. Paste title (Ctrl+V)")
        print(f"  5. Add description: {full_description[:50]}...")
        print(f"  6. Make sure video is vertical (9:16) for Shorts")
        print(f"  7. Set visibility and publish")
        
        return {
            'platform': 'YouTube Shorts',
            'video': str(video_path),
            'title': title,
            'description': full_description,
            'status': 'Browser opened - upload in progress'
        }
    
    def post_to_twitter(self, text, media_path=None, hashtags=None):
        """
        Post to Twitter/X
        """
        print(f"\n{Fore.BLUE}🐦 Posting to Twitter/X...{Style.RESET_ALL}")
        
        # Prepare tweet with hashtags
        if hashtags:
            full_text = f"{text}\n\n" + " ".join([f"#{tag}" for tag in hashtags])
        else:
            full_text = text
        
        # Copy to clipboard
        pyperclip.copy(full_text)
        print(f"{Fore.GREEN}✓ Tweet copied to clipboard:{Style.RESET_ALL}")
        print(f"  {full_text[:100]}...")
        
        # Open Twitter compose
        webbrowser.open("https://twitter.com/compose/tweet")
        
        print(f"\n{Fore.CYAN}📋 Instructions:{Style.RESET_ALL}")
        print(f"  1. Log in to Twitter/X if needed")
        print(f"  2. Paste tweet (Ctrl+V)")
        if media_path:
            print(f"  3. Click image/video icon and upload: {media_path}")
            print(f"  4. Click 'Post'")
        else:
            print(f"  3. Click 'Post'")
        
        return {
            'platform': 'Twitter/X',
            'text': full_text,
            'media': str(media_path) if media_path else None,
            'status': 'Browser opened'
        }
    
    def post_to_facebook(self, text, media_path=None, hashtags=None):
        """
        Post to Facebook
        """
        print(f"\n{Fore.BLUE}📘 Posting to Facebook...{Style.RESET_ALL}")
        
        # Prepare post with hashtags
        if hashtags:
            full_text = f"{text}\n\n" + " ".join([f"#{tag}" for tag in hashtags])
        else:
            full_text = text
        
        # Copy to clipboard
        pyperclip.copy(full_text)
        print(f"{Fore.GREEN}✓ Post copied to clipboard:{Style.RESET_ALL}")
        print(f"  {full_text[:100]}...")
        
        # Open Facebook
        webbrowser.open("https://www.facebook.com/")
        
        print(f"\n{Fore.CYAN}📋 Instructions:{Style.RESET_ALL}")
        print(f"  1. Log in to Facebook if needed")
        print(f"  2. Click 'What's on your mind?'")
        print(f"  3. Paste post (Ctrl+V)")
        if media_path:
            print(f"  4. Click Photo/Video and upload: {media_path}")
            print(f"  5. Click 'Post'")
        else:
            print(f"  4. Click 'Post'")
        
        return {
            'platform': 'Facebook',
            'text': full_text,
            'media': str(media_path) if media_path else None,
            'status': 'Browser opened'
        }
    
    def schedule_post(self, platform, content, post_time):
        """
        Schedule a post for later (requires platform-specific scheduling tools)
        """
        print(f"\n{Fore.YELLOW}⏰ Scheduling post for {post_time}...{Style.RESET_ALL}")
        print(f"{Fore.RED}Note: Most platforms require native apps or third-party tools for scheduling{Style.RESET_ALL}")
        print(f"\nRecommended scheduling tools:")
        print(f"  - Buffer (buffer.com)")
        print(f"  - Hootsuite (hootsuite.com)")
        print(f"  - Later (later.com)")
        print(f"  - Meta Business Suite (for Instagram/Facebook)")
        
        return {
            'platform': platform,
            'content': content,
            'scheduled_time': post_time,
            'status': 'Manual scheduling required'
        }
    
    def post_everywhere(self, video_path=None, image_path=None, caption="", title="", hashtags=None):
        """
        Post content to all major platforms at once
        """
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚀 POSTING TO ALL PLATFORMS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        results = []
        
        if video_path:
            # Post video to video platforms
            results.append(self.post_to_tiktok(video_path, caption, hashtags))
            time.sleep(2)
            results.append(self.post_to_instagram(video_path, caption, hashtags, is_reel=True))
            time.sleep(2)
            results.append(self.post_to_youtube_shorts(video_path, title or caption, caption, hashtags))
            time.sleep(2)
            results.append(self.post_to_twitter(caption, video_path, hashtags))
            time.sleep(2)
            results.append(self.post_to_facebook(caption, video_path, hashtags))
            
        elif image_path:
            # Post image to all platforms
            results.append(self.post_to_instagram(image_path, caption, hashtags))
            time.sleep(2)
            results.append(self.post_to_twitter(caption, image_path, hashtags))
            time.sleep(2)
            results.append(self.post_to_facebook(caption, image_path, hashtags))
        
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ All platforms ready! Follow the browser instructions.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        
        return results


# Demo usage
if __name__ == "__main__":
    poster = SocialMediaPoster()
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🌐 SOCIAL MEDIA POSTER DEMO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    # Example 1: Post TikTok video
    print(f"\n{Fore.YELLOW}Example 1: Posting TikTok video{Style.RESET_ALL}")
    video_file = "social_media_content/tiktok_text_video.mp4"
    
    if Path(video_file).exists():
        result = poster.post_to_tiktok(
            video_path=video_file,
            caption="Never give up on your dreams! 💪",
            hashtags=["motivation", "mindset", "success", "inspiration"]
        )
        print(f"\n{Fore.GREEN}✓ Result: {result['status']}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Video not found. Run tiktok_creator.py first!{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Want to post everywhere at once? Uncomment the code below:{Style.RESET_ALL}")
    print(f"\n# Post to ALL platforms:")
    print(f"# poster.post_everywhere(")
    print(f"#     video_path='social_media_content/tiktok_text_video.mp4',")
    print(f"#     caption='Check out my AI-generated content!',")
    print(f"#     title='AI-Generated Motivational Video',")
    print(f"#     hashtags=['AI', 'automation', 'content']")
    print(f"# )")
