# 🤖 Automated AI News Poster

**An end-to-end local AI pipeline that scrapes trending AI news, analyzes visual styles, and generates professional social media posters using Llama 3.2 Vision and Flux.1 [dev].**

## 🚀 Overview

This project is an **autonomous content creation agent** designed to automate the daily workflow of a social media manager. Instead of relying on expensive cloud APIs, this pipeline runs entirely **locally** on high-end hardware (NVIDIA A6000), demonstrating a privacy-first, zero-cost architecture for enterprise content generation.

It performs four key cognitive tasks:

1. **Sensing:** Polls RSS feeds (Hacker News, The Verge, NYT) for the latest AI breakthroughs.
2. **Decision Making:** Uses a local VLM (Llama 3.2 Vision) to analyze headlines and select the most "viral" or impactful story.
3. **Visual Perception:** Analyzes a user-provided `reference.png` to extract artistic style, lighting, and typography preferences.
4. **Creation:** Generates a high-fidelity 8K poster with embedded typography using the **Flux.1 [dev]** model.

## ⚡ Tech Stack & Architecture

* **Language:** Python 3.12+
* **Local LLM / VLM:** [Ollama](https://ollama.com) running `llama3.2-vision` (7B)
* **Image Generation:** [Flux.1 [dev]](https://huggingface.co/black-forest-labs/FLUX.1-dev) via HuggingFace Diffusers
* **Data Ingestion:** `feedparser` (RSS)
* **Orchestration:** Custom Python modular pipeline
* **Hardware Requirement:** NVIDIA GPU (24GB+ VRAM recommended for Flux Dev, tested on RTX A6000)

## 📂 Project Structure

```text
ai-news-poster/
├── config/
│   └── settings.py       # Centralized configuration (Models, Paths, URLs)
├── src/
│   ├── scraper.py        # RSS polling and data normalization
│   ├── processor.py      # Llama 3.2 logic for selection & style extraction
│   ├── generator.py      # Flux.1 pipeline for image rendering
│   └── publisher.py      # (In Progress) LinkedIn API integration
├── main.py               # Main pipeline orchestrator
├── reference.png         # The "Style Reference" input image
└── requirements.txt      # Python dependencies

```

## 🛠️ Installation

### 1. Prerequisites

* **Python 3.10+** installed.
* **Ollama** installed and running.
* **NVIDIA Drivers** and CUDA Toolkit installed.

### 2. Setup Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-news-poster.git
cd ai-news-poster

# Create Virtual Environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install Dependencies
pip install -r requirements.txt

```

### 3. Configure Local Models

**Pull the Text/Vision Model:**

```bash
ollama pull llama3.2-vision

```

**Authenticate for Flux:**
Flux.1 [dev] is a gated model. You must accept the license on HuggingFace and login locally.

```bash
huggingface-cli login
# Paste your User Access Token

```

## ⚙️ Configuration

The pipeline is controlled via `config/settings.py`. You can adjust model paths, GPU devices, and news sources without touching the core code.

```python
# config/settings.py
DEVICE = "cuda"
LLM_MODEL = "llama3.2-vision"
IMAGE_MODEL_PATH = "black-forest-labs/FLUX.1-dev"

```

## 🏃 Usage

1. **Place a Style Reference:** Drop any image you like (cyberpunk, minimalist, corporate) into the root folder and name it `reference.png` (or .jpg).
2. **Start Ollama Server:**
```bash
ollama serve

```


3. **Run the Pipeline:**
```bash
python main.py

```



**Output:**
The script will output logs detailing the selection process and save the final image as `local_render_{timestamp}.jpg`.

## 🔮 Future Roadmap

* [ ] **LinkedIn Integration:** Complete the `publisher.py` module to auto-post via API.
* [ ] **Feedback Loop:** Implement a "Human-in-the-loop" review step (Y/N) before generation.
* [ ] **Multi-Modal Output:** Generate a caption/article summary alongside the image.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## 📜 License

This project uses **Flux.1 [dev]**, which falls under the [FLUX.1-dev Non-Commercial License](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md). Ensure you comply with usage terms.
