# RAG-ChatBot 🤖

A production-ready Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, Streamlit, and LangChain. This intelligent chatbot retrieves relevant information from your documents and generates contextual responses using Google's Gemini AI.

## ✨ Features

- **🔍 Intelligent Document Retrieval**: Uses FAISS vector database for efficient similarity search
- **💬 Context-Aware Responses**: Maintains conversation history for coherent multi-turn dialogues
- **👤 User Management**: Built-in authentication and per-user chat history
- **🎨 Modern UI**: Clean and intuitive Streamlit interface
- **⚡ Fast API Backend**: RESTful API powered by FastAPI
- **📚 Multi-Format Support**: Processes both PDF and TXT documents
- **🔐 Persistent Storage**: PostgreSQL database for user data and chat history

## 🏗️ Architecture

```
RAG-ChatBot/
├── backend/               # FastAPI backend services
│   ├── main.py           # Main API server
│   ├── models.py         # Pydantic data models
│   ├── create_index.py   # FAISS index generation
│   ├── create_tables.py  # Database initialization
│   └── requirements.txt  # Python dependencies
├── frontend/             # Streamlit UI
│   └── app.py           # Chat interface
├── knowledge_base/       # Document storage
│   └── webscraping.txt  # Sample documents
└── faiss_index/         # Vector embeddings
    └── index.faiss      # FAISS index file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Google API key (for Gemini AI)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd RAG-ChatBot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Initialize the database**
   ```bash
   python backend/create_tables.py
   ```

6. **Create FAISS index**
   
   Place your documents (PDF/TXT) in the `knowledge_base/` folder, then:
   ```bash
   python backend/create_index.py
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

2. **Launch the frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py
   ```
   The UI will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Login**: Enter a username to create an account or login
2. **Chat**: Ask questions about the documents in your knowledge base
3. **View History**: Your conversation history is automatically saved
4. **Logout**: Click logout to end your session

### Example Queries

- "What is web scraping?"
- "Explain OOPs in Java"
- "Tell me about the main concepts in the documents"

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/get_or_create_user` | POST | User login/signup |
| `/get_history` | POST | Retrieve chat history |
| `/query` | POST | Send a query and get AI response |

View full API documentation at `http://localhost:8000/docs`

## 🛠️ Technology Stack

**Backend:**
- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for LLM applications
- **FAISS**: Vector similarity search
- **PostgreSQL**: Relational database
- **Google Gemini 2.5 Flash**: Large language model

**Frontend:**
- **Streamlit**: Interactive web interface

**ML/AI:**
- **HuggingFace Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **RAG Pipeline**: Retrieval-Augmented Generation

## ⚙️ Configuration

### Customizing the RAG Pipeline

Edit the following parameters in [backend/main.py](backend/main.py):

- **Retrieval**: Change `search_kwargs={"k":3}` to retrieve more/fewer documents
- **Temperature**: Adjust `temperature=0.7` for response creativity (0.0-1.0)
- **Chunk Size**: Modify in [backend/create_index.py](backend/create_index.py) - `chunk_size=1000`
- **Model**: Change `model="gemini-2.5-flash"` to use different Gemini models

### Adding Documents

1. Place PDF or TXT files in `knowledge_base/`
2. Run: `python backend/create_index.py`
3. Restart the backend server

## 🗄️ Database Schema

**users table:**
```sql
id SERIAL PRIMARY KEY
username TEXT UNIQUE NOT NULL
```

**chat_history table:**
```sql
id SERIAL PRIMARY KEY
user_id INTEGER REFERENCES users(id)
prompt TEXT
answer TEXT
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

**Issue: "Database connection failed"**
- Verify your `DATABASE_URL` in the `.env` file
- Ensure PostgreSQL is running

**Issue: "FAISS index not found"**
- Run `python backend/create_index.py` to create the index
- Ensure documents exist in `knowledge_base/`

**Issue: "Google API key error"**
- Check your `GOOGLE_API_KEY` in the `.env` file
- Verify the key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using LangChain, FastAPI, and Streamlit**