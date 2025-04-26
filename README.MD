# Multi-Agent AI/GenAI Use-Case Generator

An end-to-end, modular pipeline that automates discovery of AI and Generative AI opportunities for any public company. The system uses lightweight “agents” to research industry data, generate tailored use cases, collect prototype-ready datasets, and compile a polished proposal.

## 📁 Repository Structure
```text
market_research_agent/
├── agents.py           # Agent classes implementing each pipeline step
├── browser_tool.py     # Utility for Wikipedia API and HTML scraping
├── main.py             # CLI orchestrator
├── gradio_app.py       # Gradio-based interactive interface
├── requirements.txt    # Python dependencies
├── resources.md        # Generated dataset resource links
├── Final_Proposal.md   # Generated AI/GenAI use-case proposal
└── README.md           # This README
```

## 🛠 Prerequisites
- Python 3.8+
- Internet connection
- *(Optional)* Kaggle API for richer dataset links:
  1. Install the `kaggle` package.
  2. Place your `kaggle.json` in `~/.kaggle/` **or** set environment variables:
     ```bash
     export KAGGLE_USERNAME=your_username
     export KAGGLE_KEY=your_key
     ```

## 🚀 Installation
```bash
git clone https://github.com/KaushikML/Industry_Gen_Ai_Generator
cd Industry_Gen_Ai_Generator
pip install -r requirements.txt
```

## ▶️ How to Run

### 1. CLI Mode
Run the full workflow and generate output files:
```bash
python main.py
```
- **Outputs**:
  - `resources.md` – Dataset and model links for each use case
  - `Final_Proposal.md` – Full proposal with use cases and GenAI solutions

### 2. Interactive Gradio UI
Launch a web-based interface:
```bash
python gradio_app.py
```
- Open the displayed URL in your browser.
- Enter a **Company Name** (e.g., `Tesla, Inc.`).
- Click **Generate** to view:
  - Company overview
  - Use-case table
  - GenAI solution table

## ⚙️ Configuration
- **Target Company**: Edit the `company` variable in `main.py` or input via Gradio.
- **Trend Sources**: Update the URL list in `main.py` and `gradio_app.py` under `MarketStandardsAgent`.
- **Extend Agents**: Add new classes in `agents.py` and hook them into `main.py` / `gradio_app.py`.

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request for enhancements, bug fixes, or new use-case ideas.

## 📄 License
This project is licensed under the MIT License.

