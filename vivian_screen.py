"""
VIVIAN - Simple Screen Control Agent
Uses TWO AIs: One to plan, one to validate
No more bullshit parsing errors
"""

import pyautogui
import requests
import json
import time
import sys

class VivianScreenAgent:
    def __init__(self):
        self.model = "qwen2.5:latest"
        self.ollama_url = "http://localhost:11434/api/generate"
        self.history = []
        
    def ask_ai(self, prompt: str) -> str:
        """Ask Ollama AI a question"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            return response.json()['response'].strip()
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return ""
    
    def plan_task(self, task: str) -> list:
        """AI plans the steps needed"""
        prompt = f"""Break down this task into simple steps:
TASK: {task}

Available actions:
- OPEN: paint
- TYPE: hello world
- PRESS: enter
- DRAW: cat drinking milk (for images)
- VIDEO: cat drinking milk and going to bed (for videos)
- DONE

Example for "open notepad and type hello":
OPEN: notepad
TYPE: hello
DONE

Example for "make a video of a cat":
VIDEO: cat drinking milk and going to bed
DONE

Now plan for: {task}
"""
        response = self.ask_ai(prompt)
        print(f"\n📋 AI PLANNER says:\n{response}\n")
        
        steps = []
        for line in response.split('\n'):
            line = line.strip()
            if ':' in line and line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    action = parts[0].strip().upper()
                    param = parts[1].strip()
                    if action in ['OPEN', 'TYPE', 'PRESS', 'DRAW', 'VIDEO', 'DONE']:
                        steps.append((action, param))
        
        return steps
    
    def validate_step(self, action: str, param: str, step_num: int) -> bool:
        """SECOND AI validates if the step is correct"""
        history_text = "\n".join([f"{i+1}. {a}: {p}" for i, (a, p) in enumerate(self.history)])
        
        prompt = f"""You are a VALIDATOR AI checking if an action should be executed.

Steps completed so far:
{history_text if history_text else "None - starting fresh"}

Next proposed action:
{action}: {param}

Rules:
- If we did "OPEN: notepad", next should be "TYPE: something" (that's CORRECT)
- Only block if we're trying to OPEN the SAME app twice
- Typing after opening is CORRECT
- Pressing keys after typing is CORRECT
- Only say NO if we're repeating the EXACT same action

Should we execute "{action}: {param}" now?

Answer ONLY:
YES - if this is the correct next step
NO - only if this repeats something we JUST did

Your answer:"""
        
        response = self.ask_ai(prompt)
        is_valid = 'YES' in response.upper()
        
        if is_valid:
            print(f"   ✅ VALIDATOR AI: Approved")
        else:
            print(f"   ❌ VALIDATOR AI: Rejected - {response}")
        
        return is_valid
    
    def _create_video(self, description: str):
        """Generate AI video"""
        print("   🎬 Generating AI video...")
        
        from generate_video import generate_cat_video, open_video
        video_path = generate_cat_video()
        if video_path:
            time.sleep(1)
            open_video(video_path)
    
    def _draw_shape(self, description: str):
        """Generate and display actual images instead of manual drawing"""
        import subprocess
        import os
        
        print("   🎨 Generating actual image with PIL...")
        
        # Generate actual image instead of manual drawing
        if "cat" in description.lower():
            # Close Paint first
            pyautogui.hotkey('alt', 'f4')
            time.sleep(0.5)
            
            # Generate the image properly
            from generate_image import generate_cat_image, open_image_in_paint
            image_path = generate_cat_image()
            time.sleep(1)
            open_image_in_paint(image_path)
            return
            # Draw cat head (circle) - use canvas center coordinates
            center_x = canvas_center_x
            center_y = canvas_center_y - 50
            radius = 100
            
            # Draw circle properly - hold mouse down entire time
            pyautogui.moveTo(center_x + radius, center_y)
            pyautogui.mouseDown()
            
            # Draw complete circle
            for angle in range(0, 361, 2):
                x = center_x + radius * math.cos(math.radians(angle))
                y = center_y + radius * math.sin(math.radians(angle))
                pyautogui.moveTo(x, y)
            
            pyautogui.mouseUp()
            time.sleep(0.5)
            
            print("   👂 Drawing ears...")
            # Draw ears (triangles) - relative to head
            # Left ear
            left_ear_x = center_x - 60
            left_ear_y = center_y - 70
            pyautogui.moveTo(left_ear_x, left_ear_y)
            pyautogui.mouseDown()
            pyautogui.moveTo(left_ear_x - 30, left_ear_y - 50, duration=0.15)
            pyautogui.moveTo(left_ear_x + 20, left_ear_y - 20, duration=0.15)
            pyautogui.moveTo(left_ear_x, left_ear_y, duration=0.15)
            pyautogui.mouseUp()
            
            time.sleep(0.2)
            
            # Right ear
            right_ear_x = center_x + 60
            right_ear_y = center_y - 70
            pyautogui.moveTo(right_ear_x, right_ear_y)
            pyautogui.mouseDown()
            pyautogui.moveTo(right_ear_x + 30, right_ear_y - 50, duration=0.15)
            pyautogui.moveTo(right_ear_x - 20, right_ear_y - 20, duration=0.15)
            pyautogui.moveTo(right_ear_x, right_ear_y, duration=0.15)
            pyautogui.mouseUp()
            
            time.sleep(0.3)
            
            print("   🐾 Drawing body...")
            # Draw body (oval below head)
            body_center_x = center_x
            body_center_y = center_y + 150
            body_width = 80
            body_height = 110
            
            # Start at rightmost point of oval
            pyautogui.moveTo(body_center_x + body_width, body_center_y)
            pyautogui.mouseDown()
            
            # Draw complete oval
            for angle in range(0, 361, 2):
                x = body_center_x + body_width * math.cos(math.radians(angle))
                y = body_center_y + body_height * math.sin(math.radians(angle))
                pyautogui.moveTo(x, y)
            
            pyautogui.mouseUp()
            time.sleep(0.5)
            
            print("   🥛 Drawing milk saucer...")
            # Draw saucer - flat oval at bottom
            saucer_center_x = center_x  
            saucer_center_y = body_center_y + 140
            saucer_width = 120
            
            # Draw simple horizontal oval (saucer shape)
            pyautogui.moveTo(saucer_center_x - saucer_width, saucer_center_y)
            pyautogui.mouseDown()
            
            # Top curve of saucer
            for x in range(-saucer_width, saucer_width + 1, 5):
                y_offset = int(20 * math.sqrt(1 - (x/saucer_width)**2)) if abs(x) <= saucer_width else 0
                pyautogui.moveTo(saucer_center_x + x, saucer_center_y - y_offset)
            
            # Bottom line back
            pyautogui.moveTo(saucer_center_x - saucer_width, saucer_center_y)
            pyautogui.mouseUp()
            time.sleep(0.3)
            
            print("   ✨ Adding details...")
            # Add eyes - relative to head center
            eye_y = center_y - 10
            pyautogui.click(center_x - 30, eye_y)  # Left eye
            time.sleep(0.1)
            pyautogui.click(center_x + 30, eye_y)  # Right eye
            
            time.sleep(0.2)
            
            # Add whiskers - relative to head
            whisker_y_top = center_y + 10
            whisker_y_bottom = center_y + 25
            
            # Left whiskers
            pyautogui.moveTo(center_x - 80, whisker_y_top)
            pyautogui.mouseDown()
            pyautogui.moveTo(center_x - 130, whisker_y_top - 10, duration=0.1)
            pyautogui.mouseUp()
            
            pyautogui.moveTo(center_x - 80, whisker_y_bottom)
            pyautogui.mouseDown()
            pyautogui.moveTo(center_x - 130, whisker_y_bottom + 10, duration=0.1)
            pyautogui.mouseUp()
            
            # Right whiskers
            pyautogui.moveTo(center_x + 80, whisker_y_top)
            pyautogui.mouseDown()
            pyautogui.moveTo(center_x + 130, whisker_y_top - 10, duration=0.1)
            pyautogui.mouseUp()
            
            pyautogui.moveTo(center_x + 80, whisker_y_bottom)
            pyautogui.mouseDown()
            pyautogui.moveTo(center_x + 130, whisker_y_bottom + 10, duration=0.1)
            pyautogui.mouseUp()
    
    def execute_step(self, action: str, param: str):
        """Execute one step on the screen"""
        
        if action == "OPEN":
            print(f"   📂 Opening: {param}")
            pyautogui.press('win')
            time.sleep(1)
            pyautogui.write(param, interval=0.1)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(2)
            print(f"   ✅ Done")
            
        elif action == "TYPE":
            print(f"   ⌨️  Typing: {param}")
            pyautogui.write(param, interval=0.05)
            time.sleep(0.3)
            print(f"   ✅ Done")
            
        elif action == "PRESS":
            print(f"   🔘 Pressing: {param}")
            pyautogui.press(param)
            time.sleep(0.3)
            print(f"   ✅ Done")
            
        elif action == "DRAW":
            print(f"   🎨 Drawing: {param}")
            self._draw_shape(param)
            print(f"   ✅ Done")
            
        elif action == "VIDEO":
            print(f"   🎬 Creating video: {param}")
            self._create_video(param)
            print(f"   ✅ Done")
            
        elif action == "DONE":
            print(f"   ✅ Task Complete")
            return True
        
        return False
    
    def run(self, task: str):
        """Execute task with TWO AIs: Planner + Validator"""
        print(f"\n{'='*70}")
        print(f"🎯 TASK: {task}")
        print(f"{'='*70}")
        
        # AI #1: Plan the steps
        print("\n🤖 AI #1 (Planner): Breaking down task...")
        steps = self.plan_task(task)
        
        if not steps:
            print("❌ Planner AI couldn't create a plan")
            return
        
        print(f"\n📝 Plan created: {len(steps)} steps")
        print("\n⚠️  Starting in 3 seconds...")
        print("⚠️  Move mouse to TOP-LEFT corner to emergency stop\n")
        time.sleep(3)
        
        # Execute each step with validation
        for i, (action, param) in enumerate(steps, 1):
            print(f"\n--- Step {i}/{len(steps)}: {action}: {param} ---")
            
            # AI #2: Validate before executing
            print(f"   🤖 AI #2 (Validator): Checking if this is correct...")
            if not self.validate_step(action, param, i):
                print(f"   ⏭️  Skipping this step")
                continue
            
            # Execute the action
            done = self.execute_step(action, param)
            self.history.append((action, param))
            
            if done:
                break
            
            time.sleep(0.5)
        
        print(f"\n{'='*70}")
        print("✅ ALL DONE")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    print("\n🤖 VIVIAN - Screen Control Agent")
    print("Dual AI System: Planner + Validator")
    print("Powered by Ollama Qwen 2.5\n")
    
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        agent = VivianScreenAgent()
        agent.run(task)
    else:
        print("Usage: python vivian_screen.py <task>")
        print("\nExamples:")
        print('  python vivian_screen.py "open notepad and type hello world"')
        print('  python vivian_screen.py "open calculator"')
        print('  python vivian_screen.py "open word and write essay"')
