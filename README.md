# Text Summarization — Dialogue Summarizer

A dialogue summarization system built by fine-tuning [Pegasus](https://huggingface.co/google/pegasus-cnn_dailymail) on the [SAMSum](https://huggingface.co/datasets/samsum) dataset, wrapped in a modular, config-driven ML pipeline and deployed as a live web app.

**Live demo:** [text-summarization.streamlit.app](https://text-summarization-d6kobtue2ha8nw7fwy3dv9.streamlit.app/)

## Overview

This project takes a multi-turn chat-style conversation and generates a concise, human-readable summary. It started as a news-summarization model (`google/pegasus-cnn_dailymail`) and was fine-tuned to instead summarize casual dialogue — a meaningful domain shift from formal news text to informal, multi-speaker conversation.

Example:

**Input**
```
Amanda: I baked cookies. Do you want some?
Jerry: Sure!
Amanda: I'll bring you tomorrow :-)
```

**Output**
```
Amanda baked cookies and will bring them to Jerry tomorrow.
```

## Architecture

The project follows a modular, config-driven ML pipeline, with each stage separated into its own component:

```
Data Ingestion → Data Validation → Data Transformation → Model Training → Model Evaluation → Prediction
```

- **Data Ingestion** — downloads and extracts the SAMSum dataset
- **Data Validation** — verifies all expected files are present before proceeding
- **Data Transformation** — tokenizes dialogue/summary pairs for the Pegasus tokenizer
- **Model Trainer** — fine-tunes `google/pegasus-cnn_dailymail` on the transformed dataset (trained on Google Colab's free GPU)
- **Model Evaluation** — scores the fine-tuned model against the test set using ROUGE
- **Prediction Pipeline** — loads the fine-tuned model and generates summaries for new input text

Each stage is driven by `config/config.yaml` and `params.yaml`, with dedicated entity classes and a `ConfigurationManager` tying configuration to each component. `main.py` runs the full pipeline end-to-end, with each stage skipping automatically if its output already exists.

## Results

After fine-tuning for 1 epoch on SAMSum:

| Metric | Score |
|---|---|
| ROUGE-1 | 0.398 |
| ROUGE-2 | 0.177 |
| ROUGE-L | 0.289 |
| ROUGE-Lsum | 0.287 |

## Tech Stack

- **Modeling:** Hugging Face `transformers` (Pegasus, `AutoModelForSeq2SeqLM`), `datasets`, `evaluate`, PyTorch
- **Data:** SAMSum dialogue-summary dataset
- **Pipeline:** Custom modular pipeline (`ConfigurationManager` + entity configs + components), PyYAML
- **API:** FastAPI + Uvicorn, with a custom HTML/CSS/JS frontend
- **Alternate UI:** Streamlit
- **Training infra:** Google Colab (free GPU)
- **Model hosting:** [Hugging Face Hub](https://huggingface.co/anuroy007/pegasus-samsum-summarizer) — the fine-tuned model and tokenizer are hosted here and loaded at inference time via `from_pretrained`, keeping the model out of this repo
- **Deployment:** Streamlit Community Cloud (free tier)

## Project Structure

```
├── config/                # config.yaml, params.yaml
├── src/textSummarizer/
│   ├── components/        # DataIngestion, DataValidation, DataTransformation, ModelTrainer, ModelEvaluation
│   ├── config/             # ConfigurationManager
│   ├── entity/             # Config dataclasses per stage
│   ├── pipeline/           # Stage pipelines + PredictionPipeline
│   └── logging/
├── templates/              # index.html (custom frontend)
├── static/                 # style.css, script.js
├── main.py                 # Runs the full training pipeline
├── app.py                  # FastAPI app (main branch) / Streamlit app (streamlit-deploy branch)
├── Dockerfile
└── requirements.txt
```

## Branches

- **`main`** — full version: FastAPI backend, custom HTML/CSS/JS frontend, Dockerfile (for deployment on platforms supporting Docker, e.g. Hugging Face Spaces on a paid plan)
- **`streamlit-deploy`** — Streamlit-based version, deployed live and free on Streamlit Community Cloud

## Running Locally

```bash
git clone https://github.com/anuroy15052005/Text-Summarization.git
cd Text-Summarization
pip install -r requirements.txt
```

**Run the full training pipeline:**
```bash
python main.py
```

**Run the app (FastAPI, `main` branch):**
```bash
python app.py
# visit http://localhost:8080
```

**Run the app (Streamlit, `streamlit-deploy` branch):**
```bash
streamlit run app.py
```

The prediction pipeline loads the fine-tuned model directly from [Hugging Face Hub](https://huggingface.co/anuroy007/pegasus-samsum-summarizer), so no local model download or training is required to just run inference.

## Model

The fine-tuned model and tokenizer are publicly available at:
**[huggingface.co/anuroy007/pegasus-samsum-summarizer](https://huggingface.co/anuroy007/pegasus-samsum-summarizer)**