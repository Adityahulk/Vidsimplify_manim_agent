import subprocess
import os

def render_manim_code(code: str, filename: str = "scene.py", quality: str = "-ql") -> tuple[bool, str]:
    """
    Saves the code to a file and runs Manim to render it.
    """
    # Save code to file
    with open(filename, "w") as f:
        f.write(code)
    
    # Run Manim
    # Assuming the class name is 'VideoScene' or similar. 
    # We might need to parse the code to find the class name or enforce a standard name.
    # Run Manim command
    command = f"manim -ql {filename} VideoScene"
    try:
        # Run in the current directory (backend/) where the file was written
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, ""
        else:
            print(f"Error rendering video: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"Exception in renderer: {e}")
        return False, str(e)
