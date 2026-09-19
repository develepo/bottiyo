# 🐼 Bottiyo
# AI Generated Text Below
**A tiny desktop AI companion for local tools, browser automation, and agent experiments.**

Bottiyo is an experimental desktop agent interface built around a small animated panda. It provides a lightweight way to interact with local tools and browser automation through a persistent desktop companion.

The project started as part of experiments around AI-powered automation and eventually became a standalone exploration of what a desktop-native AI agent could look like.

> **Bottiyo is experimental software. It is intentionally small, hackable, and evolving.**

---

## ✨ What Bottiyo Does

Bottiyo currently provides a foundation for:

- 🐼 Animated desktop companion
- 💬 Natural command input
- 🧠 Local agent execution
- 🌐 Browser automation through Chrome CDP
- 🧰 Local tool execution
- ⚡ Background agent execution without blocking the UI
- 📡 Event-based communication between the agent and desktop UI
- 🔌 Extensible command/tool architecture

The goal isn't to build another chatbot window.

The goal is to explore a **physical-feeling interface for AI agents** that lives on the desktop and can interact with the environment around it.

---

## 🏗️ Architecture

At a high level:

```text
┌──────────────────────┐
│       Bottiyo        │
│    Desktop Panda     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Local Agent      │
│                      │
│  Command → Action    │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐ ┌─────────────┐
│  Local  │ │   Browser   │
│  Tools  │ │    CDP      │
└─────────┘ └─────────────┘
```

The desktop interface communicates with a background agent running in its own Qt thread.

Browser interaction is handled through **Chrome DevTools Protocol (CDP)** using Playwright.

---

## 📁 Project Structure

```text
Bottiyo/
│
├── app.py
│
└── desk/
    │
    ├── __init__.py
    ├── pet.py
    ├── animation.py
    │
    ├── agent/
    │   ├── __init__.py
    │   ├── router.py
    │   ├── executor.py
    │   ├── protocol.py
    │   ├── events.py
    │   └── local_agent.py
    │
    ├── tools/
    │   ├── __init__.py
    │   └── browser.py
    │
    └── assets/
        └── panda/
            ├── idle.svg
            ├── blink.svg
            ├── thinking.svg
            ├── working.svg
            └── happy.svg
```

---

## 🛠️ Tech Stack

- **Python**
- **PySide6**
- **Playwright**
- **Chrome DevTools Protocol**
- **Qt signals / slots**
- **Local process execution**

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- Google Chrome
- Windows
- Playwright
- PySide6

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright's browser dependencies if required:

```bash
playwright install
```

Run Bottiyo:

```bash
python app.py
```

---

## 🌐 Browser Automation

Bottiyo can connect to a dedicated Chrome instance through CDP.

The browser uses an isolated profile so Bottiyo's automation environment is separated from the normal browser profile.

Default CDP endpoint:

```text
http://127.0.0.1:9222
```

The browser integration is designed around:

```text
Bottiyo
   ↓
BrowserTool
   ↓
Playwright
   ↓
Chrome CDP
   ↓
Browser
```

---

## 🧠 Agent System

Bottiyo's current agent is deliberately lightweight.

Commands are routed into deterministic intents and then executed by the corresponding local tool.

For example:

```text
"open chrome"
       ↓
CommandRouter
       ↓
chrome_cdp
       ↓
ActionExecutor
       ↓
BrowserTool
```

The architecture is intentionally simple so that different agent approaches can be experimented with later.

---

## 🎨 Desktop Companion

Bottiyo isn't just a terminal wrapped in a GUI.

The panda has different states representing what the agent is doing:

```text
idle
blink
thinking
working
happy
```

Agent events are passed back to the UI through a Qt event bus.

This allows the interface to react while work is happening in the background.

---

## 🧪 Why Bottiyo Exists

Most AI agents are presented as:

```text
Chat box
    ↓
AI
    ↓
Answer
```

Bottiyo explores a different interaction model:

```text
Desktop environment
        ↓
      Agent
        ↓
   Tools / Browser
        ↓
   Visible companion
```

The long-term question is:

> **What should an AI agent feel like when it actually lives on your computer?**

Bottiyo is an exploration of that idea.

---

## 🚧 Status

**Experimental / early-stage.**

The current implementation is primarily an agent interface and browser-control foundation.

It is **not yet a fully autonomous general-purpose computer agent**.

Expect APIs, architecture, and behavior to change.

---

## 🗺️ Possible Future Directions

Some areas being explored include:

- Local LLM integration
- More capable planning
- Tool discovery
- Browser observation
- Visual computer interaction
- Persistent agent memory
- Better task execution
- Agent permissions and safety boundaries
- More expressive desktop behavior
- Multi-step workflows

Nothing in this list is a commitment to a particular implementation.

---

## 🔐 Safety

Bottiyo is intended for authorized local and browser automation.

It should not be used to bypass:

- Authentication
- CAPTCHAs
- Rate limits
- Access controls
- Paywalls
- Robots restrictions
- Other platform security mechanisms

Use automation responsibly and respect the policies of services you interact with.

---

## 🤝 Contributing

Bottiyo is an experimental project and contributions, ideas, experiments, and architectural discussions are welcome.

If you're interested in:

- AI agents
- desktop AI interfaces
- browser automation
- local models
- human-agent interaction

feel free to explore the code and open an issue or pull request.

---

## 📜 License

Use however u want idc
---

<p align="center">
  🐼 <strong>Bottiyo</strong><br>
  <sub>Small companion. Big experiments.</sub>
</p>
