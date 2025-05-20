# zonkai-rail-star-auto-battle
auto battle app for lazy fellas 

A simple, GUI-based automation tool to assist with grinding in **Honkai: Star Rail**. This app automates repetitive gameplay tasks such as looping battles and refilling power using screen recognition and user-configured options.

---

## ✨ Features

- Automates loop-based grinding using screen detection
- Uses masked image comparison (MSE) for precise UI detection
- Configurable number of loops
- Optional sound alert when all loops are done
- Multi-language support (English and Arabic)

---

## 📸 Preview

![hsr auto battle](https://i.ibb.co/VY8Yqh7Q/image.png "hsr auto battle")

---

## ⚙️ Requirements

- Python 3.8+
- Windows OS (due to `winsound` and `pyautogui` usage)
- The following Python libraries:

Install required dependencies using:

```bash
pip install numpy opencv-python pyautogui Pillow customtkinter arabic-reshaper python-bidi
Or via a requirements.txt (optional):

bash
Copy
Edit
pip install -r requirements.txt
🚀 Getting Started
Clone the repository:

bash
Copy
Edit
git clone https://github.com/kitfox5525/zonkai-rail-star-auto-battle.git
cd zonkai-rail-star-auto-battle
Run the script:

bash
Copy
Edit
python main.py
Choose your language on first launch (English or Arabic).

Set options:

Number of loops to run

Refill toggle

Sound notification toggle

Start automation – the tool will recognize screen elements and simulate clicks automatically.

📁 Project Structure
bash
Copy
Edit
📁 data/
  ├─ finish.png
  ├─ finish_mask.png
  ├─ tb_power.png
  ├─ tb_power_mask.png
  └─ ...
📄 main.py           # Main automation script
📄 settings.ini      # Auto-generated on first run
📄 lang.ini          # Language localization file
📄 done.wav          # sound when complete
📄 background.png    # GUI background
📄 app_icon.ico      # Application icon
🧠 How It Works
Captures the current screen

Compares it against predefined templates using masked Mean Squared Error (MSE)

Executes appropriate clicks based on UI state (e.g., "Finish", "Refill", "Battle")

Uses threading to keep GUI responsive

📝 Notes

Requires template images (and corresponding mask images) placed in the data/ folder.

Works best at specific resolutions matching the templates.

🪪 License
MIT License

🙌 Credits
Made by kitfox
the app is based on github.com/genesisdumallay/hsrAutoContinueBattle by genesisdumallay
