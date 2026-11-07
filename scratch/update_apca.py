with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """    # APCA contrast between top 2 colors
    apca_score = _apca_contrast(dominant_hex, secondary_hex)
    apca_pass = abs(apca_score) >= 60.0"""

replacement = """    # APCA contrast against white copy or top secondary
    apca_score = _apca_contrast("#FFFFFF", dominant_hex) if len(palette) == 1 else _apca_contrast(dominant_hex, secondary_hex)
    apca_pass = abs(apca_score) >= 60.0"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated image APCA contrast in backend/main.py")
else:
    print("Target not found")
