import numpy as np, pyautogui, cv2, time, threading, winsound, os
import customtkinter as ctk, tkinter as tk
from configparser import ConfigParser
from PIL import Image
import sys
import arabic_reshaper
from bidi.algorithm import get_display

def reshape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def only_digits(char):
    return char.isdigit()

# ───────────────────────────────────────────────
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ───────────────────────────────────────────────
config = ConfigParser()
settings_path = resource_path("settings.ini")
if not os.path.exists(settings_path):
    config["settings"] = {
        "default_loops": "10",
        "lang": "",
        "sound_enabled": "yes"
    }
    with open(settings_path, "w") as f:
        config.write(f)
else:
    config.read(settings_path)

# ───────────────────────────────────────────────
def run_main_app():
    global running, loop_counter, total_loops
    running = False
    loop_counter = 0
    total_loops = 0

    lang_cfg = ConfigParser()
    lang_cfg.read(resource_path("lang.ini"), encoding="utf-8")
    raw_lang = lang_cfg[config["settings"]["lang"]]
    lang = {}

    for key, val in raw_lang.items():
      if config["settings"]["lang"] == "arabic":
        lang[key] = reshape_arabic(val)
      else:
        lang[key] = val


    def mse(imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def execute(screenshot, name, threshold, debug=''):
        original = cv2.imread(resource_path(f'data/{name}.png'))
        mask = cv2.imread(resource_path(f'data/{name}_mask.png'), 0)
        if original is None or mask is None:
            return False
        error = mse(cv2.bitwise_and(original, original, mask=mask), cv2.bitwise_and(screenshot, screenshot, mask=mask))
        if debug == 'all' or debug == name:
            print(f'{name} - {error}')
        return error < threshold

    def update_loop_label(label):
        label.configure(text=f"{lang['loop_label']}: {loop_counter}")

    def update_progress(progress_bar):
        if total_loops > 0:
            progress = (total_loops - loop_counter) / total_loops
            progress_bar.set(progress)

    def play_done_sound():
        if sound_var.get():
            try:
                winsound.PlaySound(resource_path("done.wav"), winsound.SND_FILENAME)
            except:
                winsound.Beep(1000, 300)

    def main_loop(refill, debug, loop_label, loop_entry, progress_bar, start_btn):
        global running, loop_counter, total_loops
        try:
            user_loops = int(loop_entry.get())
            if user_loops <= 0:
                raise ValueError
        except ValueError:
            loop_label.configure(text="Invalid loop count")
            running = False
            return

        loop_counter = user_loops
        total_loops = user_loops
        config["settings"]["default_loops"] = str(user_loops)
        config["settings"]["sound_enabled"] = "yes" if sound_var.get() else "no"
        with open(resource_path("settings.ini"), "w") as f:
            config.write(f)

        in_battle = False

        while running and loop_counter > 0:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            if execute(screenshot, 'finish', 500, debug=debug):
                pyautogui.click(x=1180, y=950)
                loop_counter -= 1
                update_loop_label(loop_label)
                update_progress(progress_bar)
                time.sleep(1)
                continue

            if refill:
                if execute(screenshot, 'tb_power', 450, debug=debug):
                    pyautogui.click(x=1180, y=735)
                    in_battle = True
                elif execute(screenshot, 'tb_power2', 100, debug=debug):
                    pyautogui.click(x=1400, y=690)
                    time.sleep(1)
                    pyautogui.click(x=1180, y=800)
                    in_battle = True
                elif execute(screenshot, 'tb_power3', 100, debug=debug):
                    pyautogui.click(x=950, y=950)
                    in_battle = True

            update_loop_label(loop_label)
            update_progress(progress_bar)
            time.sleep(1 / 15)

        running = False
        loop_entry.configure(state="normal")
        debug_entry.configure(state="normal")
        refill_chk.configure(state="normal")
        sound_chk.configure(state="normal")
        start_btn.configure(text=lang["start"])
        play_done_sound()
        loop_label.configure(text="✅ Done!")

    def toggle_automation(button, refill_chk, debug_entry, loop_entry, loop_label, progress_bar):
        global running
        if not running:
            try:
                user_loops = int(loop_entry.get())
                if user_loops <= 0:
                    raise ValueError
            except ValueError:
                loop_label.configure(text="Invalid loop count")
                return

            running = True
            refill_chk.configure(state="disabled")
            debug_entry.configure(state="disabled")
            loop_entry.configure(state="disabled")
            sound_chk.configure(state="disabled")
            button.configure(text=lang["stop"])
            thread = threading.Thread(target=main_loop, args=(
                refill_var.get(), debug_var.get(), loop_label, loop_entry, progress_bar, button))
            thread.start()
        else:
            running = False
            refill_chk.configure(state="normal")
            debug_entry.configure(state="normal")
            loop_entry.configure(state="normal")
            sound_chk.configure(state="normal")
            button.configure(text=lang["start"])

    # GUI
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.iconbitmap(resource_path("app_icon.ico"))
    if config["settings"]["lang"] == "arabic":
        app.title(raw_lang["title"]) 
    else:
        app.title(lang["title"])
    app.resizable(False, False)

    if os.path.exists(resource_path("background.png")):
        bg_img = Image.open(resource_path("background.png"))
        bg_width, bg_height = bg_img.size
        bg_width = int(bg_width * 0.3)
        bg_height = int(bg_height * 0.3)

        app.geometry(f"{bg_width}x{bg_height}")
        bg_image = ctk.CTkImage(bg_img, size=(bg_width, bg_height))
        bg_label = ctk.CTkLabel(app, image=bg_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    container = ctk.CTkFrame(app, fg_color="transparent")
    container.place(relx=0.5, rely=0.05, anchor="n")

    title_label = ctk.CTkLabel(container, text=lang["title"], font=ctk.CTkFont(size=18, weight="bold"))
    title_label.pack(pady=10)

    refill_var = tk.BooleanVar(value=True)
    refill_chk = ctk.CTkSwitch(container, text=lang["refill"], variable=refill_var)
    refill_chk.pack(pady=5)

    sound_var = tk.BooleanVar(value=config["settings"].get("sound_enabled", "yes") == "yes")
    sound_chk = ctk.CTkSwitch(container, text=lang['sound'], variable=sound_var)
    sound_chk.pack(pady=5)

    debug_var = tk.StringVar(value="")
    debug_entry = ctk.CTkEntry(container, placeholder_text=lang["debug_placeholder"], textvariable=debug_var)
   # debug_entry.pack(pady=5) <= uncomment this line to enable debug entry

    vcmd = container.register(only_digits)
    default_loops = config.getint("settings", "default_loops", fallback=10)

    loop_entry = ctk.CTkEntry(
        container,
        placeholder_text="Enter loop count",
        validate="key",
        validatecommand=(vcmd, "%S")
    )
    loop_entry.insert(0, str(default_loops))
    loop_entry.pack(pady=5)

    loop_label = ctk.CTkLabel(container, text=f"{lang['loop_label']}: 0", font=ctk.CTkFont(size=14))
    loop_label.pack(pady=10)

    progress_bar = ctk.CTkProgressBar(container, width=250)
    progress_bar.set(0)
    progress_bar.pack(pady=5)

    start_btn = ctk.CTkButton(container, text=lang["start"], command=lambda: toggle_automation(
        start_btn, refill_chk, debug_entry, loop_entry, loop_label, progress_bar))
    start_btn.pack(pady=15)
    credits_label = ctk.CTkLabel(
    container,
    text="Made by kitfox • Honkai: Star Rail AB\n0.1",
    font=ctk.CTkFont(size=10, weight="normal"),
    text_color="gray"
)
    credits_label.pack(pady=(5, 10))

    app.mainloop()

# ───────────────────────────────────────────────
if config["settings"].get("lang", "") == "":
    def choose_language(language):
        config["settings"]["lang"] = language
        with open(resource_path("settings.ini"), "w") as f:
            config.write(f)
        lang_window.destroy()
        run_main_app()

    lang_window = ctk.CTk()
    lang_window.iconbitmap(resource_path("app_icon.ico"))

    lang_window.title("Select Language - اختر اللغة")
    lang_window.resizable(False, False)
    lang_window.geometry("400x200")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    label = ctk.CTkLabel(lang_window, text="Choose Language\n اللغة اختر", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(pady=20)

    ctk.CTkButton(lang_window, text="English", command=lambda: choose_language("english")).pack(pady=10)
    ctk.CTkButton(lang_window, text="عربي", command=lambda: choose_language("arabic")).pack(pady=10)

    lang_window.mainloop()

else:
    run_main_app()
