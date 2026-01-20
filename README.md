# Text-Summarization-Tool
A simple AI-powered text summarization web application built using Flask. The app provides a clean web interface and a REST API to summarize long text into concise summaries.

## 🔗 Live Demo
https://text-summarization-tool-m5as.onrender.com/

Features:
-Web-based UI for text summarization
-REST API endpoint (/api/summarize)
-Input validation and error handling
-CORS enabled (frontend/backend friendly)
-Easy to deploy on cloud platforms like Render

AI-text-summarizer/
│
├── app.py               
├── model.py             
├── templates/
│   └── index.html       
├── requirements.txt     
└── README.md

How It Works
-User enters long text in the web interface or sends JSON to the API
-Flask receives the request
-The text is passed to summarize_text() from model.py
-The summarized output is returned as JSON

Technologies used:
-Backend: Flask (Python)
-AI/NLP: Custom summarization logic (model.py)
-Frontend: HTML
-API: REST + JSON
-Deployment: Render 

