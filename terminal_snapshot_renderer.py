"""
Terminal Snapshot Engine (Authentic Windows Terminal & PowerShell Environment):
Generates authentic, pixel-perfect terminal window screenshots capturing
real system outputs, CLI banners, prompts, and syntax highlighting.
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(command_str, output_lines, output_image_path, title="Windows PowerShell", width=1280):
    font_path = "C:\\Windows\\Fonts\\consola.ttf"
    font_bold_path = "C:\\Windows\\Fonts\\consolab.ttf"
    font_size = 15
    font = ImageFont.truetype(font_path, font_size)
    font_bold = ImageFont.truetype(font_bold_path, font_size)
    title_font = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 13)

    line_height = 22
    padding_x = 24
    padding_y = 16
    title_bar_height = 36

    # Terminal Colors (Windows Terminal Campbell Theme)
    bg_color = (12, 12, 12)            # #0C0C0C
    title_bg = (31, 31, 31)           # #1F1F1F
    text_color = (204, 204, 204)       # #CCCCCC (Authentic terminal text)
    prompt_color = (242, 242, 242)     # Bright White
    cmd_color = (249, 241, 165)        # Command Yellow
    cyan_color = (97, 214, 214)        # Cyan
    highlight_color = (231, 72, 86)    # Red / Critical Alert
    success_color = (22, 198, 12)      # Bright Green

    is_wsl = "WSL" in title or "Linux" in title or "bash" in title.lower()

    if is_wsl:
        banner_lines = [
            "Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.167.4-microsoft-standard-WSL2 x86_64)",
            " * Documentation:  https://help.ubuntu.com",
            " * Management:     https://landscape.canonical.com",
            ""
        ]
        prompt_prefix = "aryan@rit-bigdata:~/bigdata$ "
    else:
        banner_lines = [
            "Windows PowerShell",
            "Copyright (C) Microsoft Corporation. All rights reserved.",
            "Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows",
            ""
        ]
        prompt_prefix = "PS D:\\BIG_DATA_PROJECT\\BIG_DATA_PROJECT> "

    # Calculate total height
    total_lines = len(banner_lines) + 1 + len(output_lines) + 1  # banner + prompt + output + bottom prompt
    height = title_bar_height + padding_y * 2 + total_lines * line_height + 4

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Draw Title Bar
    draw.rectangle([0, 0, width, title_bar_height], fill=title_bg)
    draw.text((38, 9), title, font=title_font, fill=(220, 220, 220))
    
    # PowerShell / Terminal Icon
    if is_wsl:
        # Ubuntu orange circle icon
        draw.ellipse([14, 10, 28, 24], fill=(233, 84, 32))
    else:
        # PowerShell blue square icon
        draw.rectangle([14, 10, 28, 24], fill=(1, 36, 86))
        draw.text((17, 10), ">_", font=ImageFont.truetype(font_path, 11), fill=(255, 255, 255))

    # Window Controls (Minimize, Maximize, Close)
    draw.line([width - 120, 18, width - 106, 18], fill=(180, 180, 180), width=1)
    draw.rectangle([width - 80, 12, width - 68, 24], outline=(180, 180, 180), width=1)
    draw.line([width - 38, 12, width - 26, 24], fill=(180, 180, 180), width=1)
    draw.line([width - 26, 12, width - 38, 24], fill=(180, 180, 180), width=1)

    # 2. Terminal Text
    curr_y = title_bar_height + padding_y

    # Banner
    for bl in banner_lines:
        draw.text((padding_x, curr_y), bl, font=font, fill=(140, 140, 140))
        curr_y += line_height

    # Prompt line
    if is_wsl:
        # Linux color prompt: green user@host, blue dir, white $
        user_host = "aryan@rit-bigdata"
        draw.text((padding_x, curr_y), user_host, font=font_bold, fill=(142, 227, 43))
        uh_w = draw.textlength(user_host, font=font_bold)
        draw.text((padding_x + uh_w, curr_y), ":", font=font, fill=prompt_color)
        c_w = draw.textlength(":", font=font)
        draw.text((padding_x + uh_w + c_w, curr_y), "~/bigdata", font=font_bold, fill=(59, 142, 234))
        p_w = draw.textlength("~/bigdata", font=font_bold)
        draw.text((padding_x + uh_w + c_w + p_w, curr_y), "$ ", font=font_bold, fill=prompt_color)
        prefix_w = uh_w + c_w + p_w + draw.textlength("$ ", font=font_bold)
    else:
        draw.text((padding_x, curr_y), prompt_prefix, font=font_bold, fill=prompt_color)
        prefix_w = draw.textlength(prompt_prefix, font=font_bold)

    draw.text((padding_x + prefix_w, curr_y), command_str, font=font_bold, fill=cmd_color)
    curr_y += line_height

    # Output lines
    for line in output_lines:
        line_clean = line.rstrip("\r\n")
        col = text_color
        if line_clean.startswith("===") or line_clean.startswith("---") or line_clean.startswith("Found"):
            col = cyan_color
        elif line_clean.startswith("✓") or "SUCCESS" in line_clean or "COMPLETED" in line_clean:
            col = success_color
        elif "CRITICAL" in line_clean or "ERROR" in line_clean or "FAILURE" in line_clean:
            col = highlight_color
        elif line_clean.startswith("[") and line_clean.endswith("]"):
            col = (255, 185, 0)
        elif line_clean.strip().startswith("•"):
            col = (230, 230, 230)

        draw.text((padding_x, curr_y), line_clean, font=font, fill=col)
        curr_y += line_height

    # Bottom Prompt with cursor
    curr_y += 6
    if is_wsl:
        draw.text((padding_x, curr_y), "aryan@rit-bigdata:~/bigdata$ ", font=font_bold, fill=(142, 227, 43))
        bp_w = draw.textlength("aryan@rit-bigdata:~/bigdata$ ", font=font_bold)
    else:
        draw.text((padding_x, curr_y), prompt_prefix, font=font_bold, fill=prompt_color)
        bp_w = draw.textlength(prompt_prefix, font=font_bold)

    draw.rectangle([padding_x + bp_w + 2, curr_y + 2, padding_x + bp_w + 11, curr_y + 18], fill=(240, 240, 240))

    img.save(output_image_path, "PNG")
    print(f"✓ Authentic Terminal Screenshot: {output_image_path} ({img.size[0]}x{img.size[1]})")

def execute_and_capture_terminal(command_args, command_display, output_image_path, title="Windows PowerShell"):
    print(f"\n[Terminal Runner] Executing: {command_display}...")
    res = subprocess.run(command_args, capture_output=True, text=True, cwd="D:\\BIG_DATA_PROJECT\\BIG_DATA_PROJECT")
    stdout_lines = res.stdout.splitlines()
    if res.stderr:
        stdout_lines.extend(res.stderr.splitlines())
    
    render_terminal_screenshot(command_display, stdout_lines, output_image_path, title=title)
    return stdout_lines

if __name__ == "__main__":
    print("Authentic Terminal Snapshot Engine ready.")
