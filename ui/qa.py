import os
import sqlite3
import yaml
import google.generativeai as genai

def load_api_key():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('gemini', {}).get('api_key')
    except:
        return None

def get_context(query):
    # Simplistic BM25-ish / keyword matching using LIKE.
    # In a real enterprise app, we'd use vector embeddings.
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    
    # Just grab 30 random tagged reviews for now to act as context,
    # or try to match words from the query
    words = [w for w in query.split() if len(w) > 3]
    
    if words:
        escaped_words = [w.replace("'", "''") for w in words]
        like_clauses = " OR ".join([f"text LIKE '%{w}%'" for w in escaped_words])
        sql = f"""
            SELECT source, pain_severity, text 
            FROM reviews 
            WHERE tagged_at IS NOT NULL AND ({like_clauses})
            LIMIT 30
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
    else:
        rows = []
        
    # fallback
    if len(rows) < 10:
        cursor.execute("""
            SELECT source, pain_severity, text 
            FROM reviews 
            WHERE tagged_at IS NOT NULL
            ORDER BY RANDOM() LIMIT 30
        """)
        rows = cursor.fetchall()
        
    conn.close()
    
    context_str = ""
    for r in rows:
        context_str += f"- [{r[0]} | Sev: {r[1]}] {r[2][:300]}\n"
        
    return context_str, len(rows)

def stream_answer(question):
    api_key = load_api_key()
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY':
        yield "Gemini API key is missing. Please configure it."
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash') # Use Flash for chat to save latency/tokens
    
    context, num_reviews = get_context(question)
    
    prompt = f"""
You are an AI assistant for a Spotify Product Manager. You answer questions strictly based on the provided user review data.
If the question is unrelated to the data (e.g. "what is the weather"), politely decline.
Do not hallucinate features. Cite your sources.

USER QUESTION: {question}

CONTEXT REVIEWS ({num_reviews} reviews retrieved):
{context}

ANSWER:
"""
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        yield f"An error occurred: {str(e)}"
