# Natural Language Processing (NLP) in Finance

NLP involves extracting signals from unstructured text data like news, social media, SEC filings, and earnings transcripts. It's a critical component of modern multi-strategy and event-driven funds.

---

## 1. Sentiment Analysis

The most common application: determining if a news headline or tweet is bullish or bearish for a specific stock.

### Lexicon-Based (Old School)
Uses pre-defined dictionaries of "positive" and "negative" words.
- **Loughran-McDonald (2011):** Specifically designed for financial text (e.g., "liability" is negative in finance but neutral elsewhere).

### Deep Learning & Transformers
Modern NLP uses models like BERT, which understand context and long-range dependencies.

#### FinBERT
A BERT model pre-trained on a large corpus of financial text (TRC2-financial, earnings reports).
- Significantly outperforms vanilla BERT on financial sentiment tasks.
- Available via Hugging Face: `ProsusAI/finbert`.

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def get_finbert_sentiment(text):
    """
    Predict sentiment using FinBERT.
    Returns: Positive, Negative, or Neutral probabilities.
    """
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)

    # Sentiment labels: 0=positive, 1=negative, 2=neutral
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probs.detach().numpy()[0]

# Example
text = "NVIDIA's revenue beat expectations as AI chip demand remains robust."
# Output: [0.95, 0.02, 0.03] -> Strongly Positive
```

---

## 2. SEC Filing Parsing (EDGAR)

Publicly traded companies must file periodic reports with the SEC (10-K, 10-Q, 8-K).

### Key Signals in Filings
| Signal | Description |
|--------|-------------|
| **MD&A Section** | Management's Discussion & Analysis of future risks. |
| **Sentiment Shift** | Changes in word choice between consecutive filings. |
| **Complexity** | More complex text (Fog Index) often hides bad news. |
| **Footnotes** | Identifying hidden liabilities or aggressive accounting. |

```python
import requests
from bs4 import BeautifulSoup

def get_sec_filing(ticker, accession_number):
    """
    Fetch a filing from SEC EDGAR.
    Note: Real-world implementations require User-Agent and CIK lookups.
    """
    url = f"https://www.sec.gov/Archives/edgar/data/.../{accession_number}.txt"
    headers = {'User-Agent': 'YourName (email@example.com)'}
    response = requests.get(url, headers=headers)
    return response.text
```

---

## 3. Earnings Call Analysis

Analyzing the live Q&A between management and analysts.

### Advanced Features
- **Speaker Diarization:** Distinguishing between CEO, CFO, and different analysts.
- **Vocal Tone Analysis:** Detecting stress or hesitation in the CEO's voice (requires audio data).
- **QA-to-Script Ratio:** High QA length vs script length suggests analyst skepticism.
- **Evasive Answers:** Detecting when management avoids direct questions.

---

## 4. Large Language Models (LLMs) & RAG

Large models like GPT-4 or Claude-3 are being used for complex financial reasoning.

### Retrieval-Augmented Generation (RAG)
1. **Index:** Convert thousands of financial documents into vector embeddings.
2. **Retrieve:** When a user asks "What is Apple's exposure to supply chain issues in China?", retrieve the most relevant sections.
3. **Augment:** Pass these sections to the LLM to summarize the answer.

---

## NLP Pipeline Architecture

1. **Ingestion:** Scrapers for news (Reuters, Bloomberg) and APIs for social media.
2. **Preprocessing:** Tokenization, stop-word removal, entity recognition (NER).
3. **Modeling:** FinBERT, LLM, or topic modeling (LDA).
4. **Signal Generation:** Aggregate sentiment scores into an alpha factor.
5. **Backtest:** Evaluate the signal using [[Walk-Forward Analysis]].

---

## Related Notes
- [[ML and AI MOC]] — Parent section
- [[Sentiment-Based Strategies]] — Trading on NLP signals
- [[Alpha Research]] — Signal construction
- [[Alternative Data]] — Text as a non-traditional data source
- [[Unsupervised Learning]] — Topic modeling (LDA)
- [[Resources MOC]] — Link to FinBERT paper
