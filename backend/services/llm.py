import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import traceback
from prompts import MATH_PROMPT, TECH_PROMPT, STARTUP_PROMPT

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_script_and_storyboard(text: str, category: str):
    """
    Generates a script and storyboard from the input text based on the category.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        base_prompt = TECH_PROMPT
        if category.lower() == "math":
            base_prompt = MATH_PROMPT
        elif category.lower() == "startup":
            base_prompt = STARTUP_PROMPT
            
        prompt = f"""
        {base_prompt}
        
        Topic: {text}
        
        Output Format:
        Return JSON with:
        - 'script': The narration text.
        - 'scenes': A list of objects, each having:
            - 'scene_number': Integer
            - 'description': Detailed visual description of what happens in the scene.
        """
        
        print(f"Sending prompt to LLM (Model: gemini-2.5-pro, Category: {category})...")
        response = model.generate_content(prompt)
        print(f"Received response from LLM.")
        
        try:
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_text)
        except Exception as e:
            print(f"JSON Parse Error: {e}")
            print(f"Raw Response Text: {response.text}")
            return {"error": "Failed to parse JSON", "raw": response.text}
            
    except Exception as e:
        print(f"LLM Error in generate_script_and_storyboard: {e}")
        traceback.print_exc()
        return {"error": str(e)}

def generate_manim_code(storyboard: dict, category: str = "tech"):
    """
    Generates Manim code from the storyboard.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Define category-specific visual guidelines
        visual_style = ""
        if category.lower() == "math":
            visual_style = """
            - **Visual Style**: Mathematical & Academic.
            - **Elements**: Use Axes, FunctionGraph, Tex/MathTex for equations, and geometric shapes.
            - **Layout**: Clean, structured, often using split screens or centered equations.
            """
        elif category.lower() == "startup":
            visual_style = """
            - **Visual Style**: Modern, Clean, Corporate.
            - **Elements**: Use flowcharts, bullet points, bold text, and simple geometric icons to represent concepts.
            - **Layout**: Dynamic, moving from problem to solution.
            """
        else: # Tech / Default
            visual_style = """
            - **Visual Style**: Technical Diagram / Architecture.
            - **Elements**: Use rectangles for services, circles for nodes, arrows for data flow.
            - **Icons**: Create simple geometric representations for User, Database, Server if needed (using built-in shapes).
            """

        prompt = f"""
        Generate Manim (Python) code for the following storyboard:
        {json.dumps(storyboard)}
        
        Ensure the code is complete, runnable, and uses the Manim library correctly.
        
        # DESIGN SYSTEM (PREMIUM LOOK)
        - **Colors**: Use a cohesive palette. 
          - Background: BLACK (default)
          - Primary: BLUE (#3B82F6)
          - Secondary: PURPLE (#8B5CF6)
          - Accent: TEAL (#14B8A6)
          - Text: WHITE or LIGHT_GRAY (#E5E7EB)
        - **Typography**: Use standard fonts but ensure high contrast.
        
        {visual_style}
        
        # CODING RULES
        - **NO External Assets**: Use ONLY built-in shapes (Circle, Square, Rectangle, Line, Arrow, etc.).
        - **NO Hallucinated Methods**: 
          - Do NOT use `arrange_in_a_circle`. Use standard `arrange()`.
          - Do NOT use `set_style` with `color`. Use `set_color()`, `set_fill()`, or `set_stroke()` directly.
        - **Completeness**: You MUST generate code for ALL scenes in the storyboard. Do not skip any.
        - **Transitions**: Use smooth transitions (FadeIn, Create, Transform) between scenes.
        - **Class Name**: The class MUST be named `VideoScene`.
        - **Structure**: 
          - Create a single `construct(self)` method.
          - Use `self.wait(2)` between major scene changes.
          - Clear the screen with `self.clear()` or `self.play(FadeOut(everything))` between distinct scenes if needed, or transition smoothly.
        
        Return ONLY the python code.
        """
        
        print(f"Sending prompt to LLM for Manim code (Model: gemini-2.5-pro)...")
        response = model.generate_content(prompt)
        print(f"Received response from LLM for Manim code.")
        return response.text
        
    except Exception as e:
        print(f"LLM Error in generate_manim_code: {e}")
        traceback.print_exc()
        return ""

def fix_manim_code(code: str, error_log: str):
    """
    Fixes the Manim code based on the error log.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        prompt = f"""
        The following Manim code failed to render:
        
        ```python
        {code}
        ```
        
        Error Log:
        {error_log}
        
        Please FIX the code to resolve the error.
        
        # CODING RULES
        - **NO External Assets**: Use ONLY built-in shapes (Circle, Square, Rectangle, Line, Arrow, etc.).
        - **NO Hallucinated Methods**: 
          - Do NOT use `arrange_in_a_circle`. Use standard `arrange()`.
          - Do NOT use `set_style` with `color`. Use `set_color()`, `set_fill()`, or `set_stroke()` directly.
        - **Completeness**: Ensure the code is complete and runnable.
        - **Class Name**: The class MUST be named `VideoScene`.
        
        Return ONLY the fixed python code.
        """
        
        print(f"Sending prompt to LLM for FIXING Manim code...")
        response = model.generate_content(prompt)
        print(f"Received response from LLM for FIXING Manim code.")
        return response.text
        
    except Exception as e:
        print(f"LLM Error in fix_manim_code: {e}")
        traceback.print_exc()
        return code # Return original code if fix fails
