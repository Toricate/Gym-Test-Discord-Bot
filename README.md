# Gym Compass Discord Bot 🏋️‍♂️🧪

A psychometric testing bot for Discord that evaluates a user's lifting philosophy and biochemical status across a custom 2D grid. Built with `discord.py` and `Pillow`, this bot runs completely free and handles private user assessments natively.

---

## 📊 The Axes & Ranks

The bot tracks user answers across a 30-question test to map them onto a two-axis grid:
* **X-Axis:** Natural vs. Chemical (Biochemical Purity)
* **Y-Axis:** Form vs. Ego (Training Philosophy)

### Core Archetypes
Depending on where the red dot lands, users are assigned one of the following legendary statuses:
* **The Tren-Titan** (Far Chemical / Far Ego)
* **The Zen Master** (Far Natural / Far Form)
* **The Bio-Hacker** (Far Chemical / Far Form)
* **The Raw Chaos** (Far Natural / Far Ego)
* **The Casual Lifter** (Dead Center Neutral)

---

## ⚙️ Features

* **Dynamic Channel Creation:** Automatically spins up a private channel for each user inside a designated category to keep responses confidential.
* **Interactive Button UI:** Uses Discord's modern UI buttons (`Strongly Agree` to `Strongly Disagree`) rather than messy text commands.
* **Precise Visual Plotting:** Uses `Pillow` to dynamically draw a red coordinate dot directly onto a template grid, automatically clamped to stay inside the margins.
* **Self-Cleaning:** Automatically deletes the testing channel 60 seconds after completion to prevent server clutter.

---

## 🛠️ Prerequisites & Installation

### 1. File Structure
Ensure your host (e.g., FPS.ms or local environment) has the following files in the main directory:
```text
├── app.py                  # The main bot script
├── Gym Compass.png         # Your custom background grid template
└── requirements.txt        # Python dependencies

```

### 2. Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt

```

### 3. Discord Developer Portal Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a New Application.
2. Under the **Bot** tab, toggle **ON** the following Privileged Gateway Intents:
* **Presence Intent**
* **Server Members Intent**
* **Message Content Intent**


3. Reset and copy your Bot Token. Paste it into the `TOKEN` variable inside `app.py`.

### 4. Bot Invite Permissions

Generate an invite link using the **OAuth2 URL Generator** with the following settings:

* **Scopes:** `bot`
* **Bot Permissions:** * Manage Channels (Crucial for private sessions)
* Send Messages
* Attach Files (Crucial for sending the plotted image)
* Read Message History



---

## 🚀 How to Run

1. Create a category in your Discord Server named exactly **`Chemical Test`** (case-sensitive).
2. Start the script on your host:
```bash
python app.py

```


3. Type **`!start`** in any public chat channel. The bot will delete your command, open your private text room under the `Chemical Test` category, and begin the exam.

---

## 📝 License

Distributed under the "Do Whatever You Want" License. Feel free to copy, tweak, share, or completely rewrite the code. Go wild.

```

```
