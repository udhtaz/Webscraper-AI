# FastAPI Web Scraper & AI-Based Content Processing ⚡

A **FastAPI backend** that automates the process of:
- Scraping event details from the web 🕵️‍♂️
- Processing and structuring scraped event data using LLM 🏗️
- Generating **brief, engaging event descriptions** using multiple **LLMs** 🤖
- **Supported LLMs:** GPT-4o, Deepseek R1, Llama3.3, Qwen2.5, Gemma2, Mixtral8x7b ⚡
- Storing processed event details into a **PostgreSQL database** 🗄️

---

## **🚀 Features**
✅ **Automated Event Scraping** – Extract event details dynamically  
✅ **LLM-Powered Summarization** – Generate brief event descriptions  
✅ **Multiple AI Models** – Switch between LLMs based on preference  
✅ **Full CRUD Operations** – Manage events in a PostgreSQL database  
✅ **FastAPI & Async Processing** – High-performance API  

---

## **📦 Installation & Setup**

### **🔹 1. Clone the Repository**
```bash
git clone https://github.com/udhtaz/Webscraper-AI.git
cd Webscraper-AI
```

### **🔹 2. Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **🔹 3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **🔹 4. Configure Environment Variables**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
```

### **🔹 5. Run Database Migrations**
```bash
alembic upgrade head
```

### **🔹 6. Start the FastAPI Server**
```bash
uvicorn app:app --reload
```
Server will be running at **http://127.0.0.1:8000**

---

## **🛠️ API Endpoints**

### **🔹 Generate & Save Events**
**POST** `/scraper/generate-events/`  
_Request Body:_
```json
{
  "country": "ghana",
  "city": "accra",
  "model": "gpt-4o",
  "is_db": true
}
```

### **🔹 Get All Events**
**GET** `/crud/events/`

### **🔹 Get a Specific Event**
**GET** `/crud/events/{event_id}`

### **🔹 Update an Event**
**PUT** `/crud/events/{event_id}`  
_Request Body (Partial Updates Supported):_
```json
{
  "venue": "New Venue Name"
}
```

### **🔹 Delete an Event**
**DELETE** `/crud/events/{event_id}`

📌 **Full API docs available at** `http://127.0.0.1:8000/api/{version}/docs/`

---

## **🛠️ Tech Stack**
- **FastAPI** – High-performance backend framework ⚡
- **SQLModel & Async SQLAlchemy** – Database ORM 🗄️
- **BeautifulSoup** – Web scraping for event extraction 🕵️‍♂️
- **OpenAI API & Groq API** – AI-powered event summarization 🤖
- **Uvicorn** – ASGI server for FastAPI ⚡
- **Alembic** – Database migrations 🗄️

---

## **📜 Contributing**
🚀 Contributions are welcome!  

1. **Fork the repo**  
2. **Create a feature branch** (`git checkout -b feature-name`)  
3. **Commit changes** (`git commit -m "feat: add new feature"`)  
4. **Push to GitHub** (`git push origin feature-name`)  
5. **Create a pull request** 🎉  

---

## **📄 License**
Apache License. See `LICENSE` for more details.

---

### ** Ready to automate webscraping and content processing with AI? Get started today!**

