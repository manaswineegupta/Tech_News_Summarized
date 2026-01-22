# Tech News Summarizer

A simple web application that fetches the hottest technology news from **Hacker News** and generates concise summaries using gpt-4o-mini.

This project demonstrates an end-to-end pipeline combining external APIs, AI-powered summarization, caching, and a lightweight web service.


## Features

- Fetches the **top 5 tech stories** from Hacker News  
- Generates **3-bullet summaries** for each article using gpt-4o-mini
- **Daily caching** to reduce repeated API and LLM calls  
- REST API built with FastAPI  
- Frontend-ready with CORS enabled  


## Tech Stack

### Backend
- Python
- FastAPI
- Requests
- OpenAI Python SDK

### Frontend
- React (Vite)

### AI
- OpenAI gpt-4o-mini model for summarization


## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/manaswineegupta/Tech_News_Summarized.git
cd tech-news/backend
```

### 2. Set environment variables
Create a .env file in backend/ and add the following code:
```bash
OPENAI_API_KEY=your_openai_api_key
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the backend
```bash
uvicorn main:app --reload
```
The API will be available at:
```bash
http://localhost:8000/news
```

### 5. Run the frontend
```bash
cd ../frontend
npm install
npm run dev
```
The frontend runs at:
```bash
http://localhost:5173
```

## API Endpoint

### `GET /news`

Returns summarized tech news.

**Example response:**
```json
{
  "source": "Hacker News",
  "cached": false,
  "articles": [
    {
      "title": "Example Title",
      "summary": [
        "Bullet point 1",
        "Bullet point 2",
        "Bullet point 3"
      ],
      "url": "https://example.com"
    }
  ]
}
```

## Caching Strategy

- News summaries are cached **once per day**
- Cache is stored locally as a JSON file

### On the first request of the day:
1. News is fetched from Hacker News  
2. LLM is called to generate summaries  
3. Results are cached (old cached results are deleted to save space) 

### On subsequent requests:
- Data is served directly from cache  

This approach minimizes LLM usage while keeping the system simple and cost-effective.


## LLM Usage

- Each article is summarized independently i.e. 1 LLM call per article (total 5 articles per day)
- Summaries are generated using gpt-4o-mini 
- Batching of LLM calls is not implemented to prioritize correctness and simplicity, but can be easily added in the future
- LLM is asked to also read the full article at the given url because often times the content retured by Hacker News API is incomplete or insufficient


## Tradeoffs

- Hacker News provides limited article content. For simplicity I am only pulling tech news from one source. This can be expanded to multiple sources in the future
- File-based caching is used instead of Redis for simplicity   
- LLM calls are sequential rather than batched i.e. 1 LLM call per article (in this project we summarize the top 5 articles). This can easily be convereted to a batched call where we ask the LLM to summarize all articles in 1 call  


## Future Improvements

- Add multiple news sources (TechCrunch, The Verge, NewsAPI)  
- Batch LLM calls to reduce latency and cost
- Improve the frontend 
