# 💼 AI-Powered Job Recommendation System

An intelligent web application that helps students and job seekers discover suitable job or internship opportunities by matching their **skills, experience, and preferences** using **LangChain**, **Groq LLaMA3**, and **RAG (Retrieval-Augmented Generation)** techniques.

<img width="1907" height="963" alt="image" src="https://github.com/user-attachments/assets/0e4c0d02-1d7a-479c-9aca-5cf6acc64900" />
<img width="1900" height="969" alt="image" src="https://github.com/user-attachments/assets/22132308-6143-4efb-a58d-d5384950d675" />
<img width="1906" height="955" alt="image" src="https://github.com/user-attachments/assets/dfb03690-55cf-444c-81e6-4a10e92308b8" />
<img width="1910" height="955" alt="image" src="https://github.com/user-attachments/assets/6b54faed-108e-4a5c-9641-830556bcb9b0" />


---

## 📌 Features

- **Manual Input or Resume Upload**  
  Users can enter their job preferences manually or upload a resume (PDF).
  
- **Real-Time or Demo Job Data**  
  Fetch live job postings from APIs (Google Jobs, LinkedIn Jobs via RapidAPI) or load data during intervals and check for the job recommendations.

- **LLM-Powered Recommendations**  
  Uses **LangChain + Groq LLaMA3-70B** for ranking the best-matching jobs.

- **RAG-based Matching**  
  Finds top job matches using vector similarity (FAISS) between job postings and user profile/resume.

- **Polished Streamlit UI**  
  Professional and interactive interface with styled CSS.

---

## 🛠️ Tech Stack

| Component            | Technology                          |
|----------------------|--------------------------------------|
| Programming Language | Python                              |
| LLM Integration      | LangChain + Groq LLaMA3-70B         |
| Vector Store         | FAISS / Chroma                      |
| UI Framework         | Streamlit                           |
| Deployment           | Streamlit Cloud / Local             |
| Resume Parsing       | pdfplumber + Groq LLaMA3            |

---

## 🚀 How It Works

1. **User Input** – Enter skills, experience, and preferences OR upload resume.
2. **Data Retrieval** – Fetches job postings from API or demo dataset.
3. **Data Preprocessing** – Extracts relevant job features before embedding.
4. **Embedding & Retrieval** – Uses vector similarity to shortlist top candidates.
5. **LLM Ranking** – LLaMA3 ranks shortlisted jobs with clear reasoning.
6. **Results Display** – Shows polished recommendations with job links.

![Workflow Diagram](screenshots/workflow.png)  
*System architecture workflow*

---

## 📂 Project Structure

```

├── app.py                # Main Streamlit application
├── requirements.txt      # Dependencies
├── .env                  # API keys and configs (not committed)
├── data/
│   └── jobs\_api.json     # Demo job postings
├── src/
│   ├── fetch\_jobs.py     # Fetch job postings from API
│   ├── embeddings\_store.py # Vector store management
│   ├── rag\_recommender.py  # RAG + LLM recommendation logic
│   ├── resume\_parser.py    # Resume parsing (manual + LLM-based)
│   └── **init**.py
└── styles.css            # Custom UI styling

````

---

## ⚙️ Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/GautamAnandDS/AI-Powered-Job-Recommender.git
cd AI-Powered-Job-Recommender
````

2. **Create Virtual Environment & Install Dependencies**

```bash
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)
pip install -r requirements.txt
```

3. **Set Environment Variables** in `.env`

```env
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=your_rapidapi_host
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-70b-8192
```

4. **Run the App**

```bash
streamlit run app.py
```

---

## 🧪 Sample Input/Output

**Example User Input (manual)**:

```
Role: Data Analyst
Skills: Python, SQL, Machine Learning
Experience: 2 years
Location: Bangalore
Job Type: Full-time
```

**Example Output**:

```
1) Business Analyst - Company X
   Reason: Matches data analysis skills and location preference.
   [Apply Here](https://link-to-job)

2) Data Scientist Intern - Company Y
   Reason: Strong skills match, but internship instead of full-time.
   [Apply Here](https://link-to-job)
```

---

## 📸 Screenshots

| Home Page                                                                                                                          | Job Recommendations                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| <img width="1907" height="963" alt="image" src="https://github.com/user-attachments/assets/0e4c0d02-1d7a-479c-9aca-5cf6acc64900" />| <img width="1900" height="969" alt="image" src="https://github.com/user-attachments/assets/22132308-6143-4efb-a58d-d5384950d675" /> |

---

## 📄 Documentation

📌 **Google Doc** – [Project Documentation Link](https://docs.google.com/)
📌 **Video Walkthrough** – [YouTube Demo Link](https://youtube.com/)

---

## ✨ What I Learned

* Integrating **LangChain** with **Groq LLaMA3** for real-world use cases.
* Optimizing embeddings for performance in RAG workflows.
* Building interactive and professional **Streamlit** apps.
* Using LLMs for structured **resume parsing**.

---

## 📜 License

MIT License © 2025 Gautam Anand

```
