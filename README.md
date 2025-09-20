# 🧪 CORD-19 Assignment

This project is a small data exploration and visualization app built with **Streamlit**.  
It uses the [CORD-19 dataset](https://www.semanticscholar.org/cord19) to load, clean, and visualize COVID-19 research metadata.

---

## 📂 Project Structure

CORD19_Assignment/
├── app/
│ └── streamlit_app.py # Streamlit app entry point
├── data/
│ └── metadata.csv # Dataset (ignored in repo for size)
├── notebooks/
│ └── 01_load_and_explore.ipynb # Data exploration notebook
├── requirements.txt # Production dependencies
└── README.md # This file


---

---

## 🚀 Setup & Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/thuodev/CORD_19-Assignment.git
cd CORD_19-Assignment
---
2️⃣ Create Virtual Environment & Install Requirements


python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Mac/Linux

pip install -r requirements.txt
data/metadata.csv
streamlit run app/streamlit_app.py

