import os
import re
import sys
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont

# Garante que o diretório de trabalho seja SEMPRE a pasta onde este script está salvo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Trata compatibilidade de versão do Pillow (Linux x Windows)
try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_FILTER = Image.LANCZOS

FOLDER_FONT = os.path.join(BASE_DIR, "vox")
DEFAULT_FONT_FILE_NAME = "Vox-Regular.ttf"
FOLDER_RESULTS = os.path.join(BASE_DIR, "results")
FILE_PHOENIX = os.path.join(BASE_DIR, "fenix.png")

config = {
    "font_name": DEFAULT_FONT_FILE_NAME,
    "use_fixed_height": False,
    "phoenix_height_px": 60,
    "scale_factor": 1.0,
    "width_scale": 1.0,
    "space_between": 15,
    "margin": 20,
}


def list_available_fonts():
    if not os.path.exists(FOLDER_FONT):
        os.makedirs(FOLDER_FONT, exist_ok=True)
        return []

    valid_extensions = (".ttf", ".otf")
    files = [
        f for f in os.listdir(FOLDER_FONT) 
        if f.lower().endswith(valid_extensions)
    ]
    return files


def sanitize_file_name(text):
    clean_text = re.sub(r'[\\/*?:"<>|]', "", text)
    return clean_text.strip().replace(" ", "_")[:30]


def cut_os_in_half(image, text, font, pos_x_text, pos_y_text):
    draw = ImageDraw.Draw(image)

    for i, char in enumerate(text):
        left_text = text[:i]
        bbox_left = font.getbbox(left_text) if left_text else (0, 0, 0, 0)
        x_current = pos_x_text + (bbox_left[2] - bbox_left[0] if left_text else 0)

        bbox_char = font.getbbox(char)
        char_width = bbox_char[2] - bbox_char[0]

        if char in ("o", "O"):
            char_height = bbox_char[3] - bbox_char[1]

            x_start_letter = x_current + bbox_char[0]
            x_center = x_start_letter + (char_width / 2)

            cut_width = max(3, int(font.size * 0.12))

            x1 = x_center - (cut_width / 2)
            x2 = x_center + (cut_width / 2)

            y1 = pos_y_text + bbox_char[1]
            y2 = y1 + char_height

            draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 0))


def open_settings_window():
    win = tk.Toplevel(app)
    win.title("Generator Settings")
    win.geometry("400x420")
    win.resizable(False, False)
    
    win.transient(app)
    win.grab_set()

    frame_font = tk.LabelFrame(win, text=" Font ", font=("Arial", 9, "bold"), padx=10, pady=5)
    frame_font.pack(fill="x", padx=15, pady=(10, 5))

    fonts = list_available_fonts()
    
    if config["font_name"] not in fonts and fonts:
        config["font_name"] = fonts[0]

    combo_font = ttk.Combobox(frame_font, values=fonts, state="readonly")
    if fonts:
        combo_font.set(config["font_name"])
    else:
        combo_font.set("No fonts found in /vox")
    combo_font.pack(fill="x", pady=5)

    frame_phoenix = tk.LabelFrame(win, text=" Phoenix & Layout Parameters ", font=("Arial", 9, "bold"), padx=10, pady=5)
    frame_phoenix.pack(fill="x", padx=15, pady=5)

    var_fixed = tk.BooleanVar(value=config["use_fixed_height"])
    chk_fixed = tk.Checkbutton(frame_phoenix, text="Use Fixed Height in Pixels", variable=var_fixed)
    chk_fixed.pack(anchor="w", pady=(5, 5))

    frame_height = tk.Frame(frame_phoenix)
    frame_height.pack(fill="x", pady=2)
    tk.Label(frame_height, text="Fixed Height (px):").pack(side="left")
    ent_height_px = tk.Entry(frame_height, width=8, justify="center")
    ent_height_px.insert(0, str(config["phoenix_height_px"]))
    ent_height_px.pack(side="right")

    frame_scale = tk.Frame(frame_phoenix)
    frame_scale.pack(fill="x", pady=2)
    tk.Label(frame_scale, text="Scale Factor (Vertical):").pack(side="left")
    ent_scale = tk.Entry(frame_scale, width=8, justify="center")
    ent_scale.insert(0, str(config["scale_factor"]))
    ent_scale.pack(side="right")

    frame_width = tk.Frame(frame_phoenix)
    frame_width.pack(fill="x", pady=2)
    tk.Label(frame_width, text="Stretch Aspect Ratio:").pack(side="left")
    ent_width = tk.Entry(frame_width, width=8, justify="center")
    ent_width.insert(0, str(config["width_scale"]))
    ent_width.pack(side="right")

    frame_space = tk.Frame(frame_phoenix)
    frame_space.pack(fill="x", pady=2)
    tk.Label(frame_space, text="Text Spacing (px):").pack(side="left")
    ent_space = tk.Entry(frame_space, width=8, justify="center")
    ent_space.insert(0, str(config["space_between"]))
    ent_space.pack(side="right")

    frame_margin = tk.Frame(frame_phoenix)
    frame_margin.pack(fill="x", pady=2)
    tk.Label(frame_margin, text="Outer Margin (px):").pack(side="left")
    ent_margin = tk.Entry(frame_margin, width=8, justify="center")
    ent_margin.insert(0, str(config["margin"]))
    ent_margin.pack(side="right")

    def save_settings():
        font_selected = combo_font.get()
        if not font_selected or font_selected == "No fonts found in /vox":
            messagebox.showwarning(
                "Font Warning",
                f"No valid font selected.\nPlease place .ttf/.otf files inside the '{FOLDER_FONT}' folder."
            )
            return

        try:
            config["font_name"] = font_selected
            config["use_fixed_height"] = var_fixed.get()
            config["phoenix_height_px"] = int(ent_height_px.get())
            config["scale_factor"] = float(ent_scale.get())
            config["width_scale"] = float(ent_width.get())
            config["space_between"] = int(ent_space.get())
            config["margin"] = int(ent_margin.get())
            win.destroy()
            messagebox.showinfo("Settings", "Parameters saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for the parameters.")

    btn_save = tk.Button(
        win,
        text="Save Settings",
        command=save_settings,
        bg="#1976D2",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5,
    )
    btn_save.pack(pady=15)


def generate_png_image():
    text = entry_text.get().strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    try:
        font_size = int(entry_size.get())
    except ValueError:
        messagebox.showerror("Error", "Font size must be an integer.")
        return

    font_path = os.path.join(FOLDER_FONT, config["font_name"])

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        messagebox.showerror(
            "Font Error",
            f"Could not find the font file at:\n{font_path}\n\n"
            f"Make sure '{config['font_name']}' is in the '{FOLDER_FONT}' folder or change the font in Settings (⚙).",
        )
        return

    if not os.path.exists(FILE_PHOENIX):
        messagebox.showerror(
            "Image Error",
            f"Could not find the image '{FILE_PHOENIX}'.\nExpected path:\n{FILE_PHOENIX}",
        )
        return

    try:
        img_phoenix = Image.open(FILE_PHOENIX).convert("RGBA")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the phoenix image:\n{e}")
        return

    os.makedirs(FOLDER_RESULTS, exist_ok=True)

    suggested_name = sanitize_file_name(text) or "image"
    file_name = f"{suggested_name}.png"
    save_path = os.path.join(FOLDER_RESULTS, file_name)

    counter = 1
    final_path = save_path
    while os.path.exists(final_path):
        final_path = os.path.join(FOLDER_RESULTS, f"{suggested_name}_{counter}.png")
        counter += 1

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    orig_width, orig_height = img_phoenix.size

    if config["use_fixed_height"]:
        base_height = config["phoenix_height_px"]
    else:
        base_height = text_height

    new_height = int(base_height * config["scale_factor"])
    width_ratio = new_height / float(orig_height)
    new_width = int(orig_width * width_ratio * config["width_scale"])

    if new_width > 0 and new_height > 0:
        img_phoenix = img_phoenix.resize((new_width, new_height), RESAMPLE_FILTER)

    margin = config["margin"]
    space = config["space_between"]

    img_width = new_width + space + text_width + (margin * 2)
    max_content_height = max(text_height, new_height)
    img_height = max_content_height + (margin * 2)

    image = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    center_y = margin + (max_content_height / 2)

    pos_x_phoenix = margin
    pos_y_phoenix = int(center_y - (new_height / 2))

    pos_x_text = margin + new_width + space - bbox[0]
    pos_y_text = int(center_y - (text_height / 2) - bbox[1])

    image.paste(img_phoenix, (pos_x_phoenix, pos_y_phoenix), mask=img_phoenix)

    draw.text((pos_x_text, pos_y_text), text, font=font, fill=(0, 0, 0, 255))

    cut_os_in_half(image, text, font, pos_x_text, pos_y_text)

    image.save(final_path)
    messagebox.showinfo("Success", f"Image successfully saved to:\n{final_path}")


app = tk.Tk()
app.title("PNG Generator - Vox Font")
app.geometry("400x260")
app.resizable(False, False)

btn_config = tk.Button(
    app,
    text="⚙ Config",
    command=open_settings_window,
    font=("Arial", 9, "bold"),
    bg="#e0e0e0",
    relief="groove",
)
btn_config.place(x=315, y=10, width=75, height=28)

lbl_text = tk.Label(app, text="Enter your text:", font=("Arial", 10, "bold"))
lbl_text.pack(pady=(25, 5))

entry_text = tk.Entry(app, width=40, font=("Arial", 11))
entry_text.pack(pady=5)
entry_text.focus()

lbl_size = tk.Label(app, text="Font size (px):")
lbl_size.pack(pady=(10, 2))

entry_size = tk.Entry(app, width=10, justify="center")
entry_size.insert(0, "48")
entry_size.pack(pady=5)

btn_generate = tk.Button(
    app,
    text="Generate PNG",
    command=generate_png_image,
    bg="#2e7d32",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
)
btn_generate.pack(pady=20)

app.mainloop()