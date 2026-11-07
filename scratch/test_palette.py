import sys
import os
sys.path.insert(0, r"C:\Users\swast\OneDrive\Desktop\vercel\backend")
from main import _extract_palette_from_b64

indigo_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAiSURBVFhH7c4xEQAgAMPAh5+M4V3Y4Zfsgq0zM/txrQYGBgYGBp5N6W8D1wT6eG0AAAAASUVORK5CYII="
try:
    p = _extract_palette_from_b64(indigo_b64)
    print("Palette:", p)
except Exception as e:
    import traceback
    traceback.print_exc()
