import sys
import os
import json
import time
import datetime
import logging
import sqlite3
import yaml
import google.generativeai as genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import get_db_connection

QUESTIONS = [
    "1. Why do users struggle to discover new music?",
    "2. What are the most common frustrations with recommendations?",
    "3. What listening behaviors are users trying to achieve?",
    "4. What causes users to repeatedly listen to the same content?",
    "5. Which user segments experience different discovery challenges?",
    "6. What unmet needs emerge consistently across reviews?"
]

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_data_summary(cursor):
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE tagged_at IS NOT NULL")
    total_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT theme, COUNT(*) as c FROM reviews WHERE tagged_at IS NOT NULL GROUP BY theme ORDER BY c DESC")
    themes = {row['theme']: row['c'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT pain_severity, COUNT(*) as c FROM reviews WHERE tagged_at IS NOT NULL GROUP BY pain_severity ORDER BY c DESC")
    severities = {row['pain_severity']: row['c'] for row in cursor.fetchall()}
    
    # Grab top 30 most severe reviews (or randomized if we have many) to use as quotes
    cursor.execute("""
        SELECT source, date, pain_severity, text 
        FROM reviews 
        WHERE tagged_at IS NOT NULL AND pain_severity >= 3 AND theme != 'other'
        ORDER BY pain_severity DESC, date DESC LIMIT 40
    """)
    quotes_rows = cursor.fetchall()
    
    # fallback if not enough high severity
    if len(quotes_rows) < 10:
        cursor.execute("""
            SELECT source, date, pain_severity, text 
            FROM reviews 
            WHERE tagged_at IS NOT NULL AND theme != 'other'
            ORDER BY RANDOM() LIMIT 30
        """)
        quotes_rows = cursor.fetchall()
        
    formatted_quotes = []
    for r in quotes_rows:
        text = r['text']
        if text and len(text) > 200:
            text = text[:200] + "..."
        formatted_quotes.append(f"[{r['source']} | {r['date']} | Sev: {r['pain_severity']}] \"{text}\"")
        
    return {
        "count": total_count,
        "themes": json.dumps(themes),
        "severities": json.dumps(severities),
        "quotes": "\n".join(formatted_quotes),
        "raw_quotes_list": [dict(r) for r in quotes_rows]
    }

def run():
    print("Starting Synthesizer...")
    config = load_config()
    api_key = config.get('gemini', {}).get('api_key')
    
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY':
        print("Gemini API key missing in config.yaml.")
        return
        
    genai.configure(api_key=api_key)
    # Switched to Flash because the free tier daily quota for Pro was exhausted
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    data_summary = get_data_summary(cursor)
    
    if data_summary['count'] == 0:
        print("No tagged reviews found. Run tagger first.")
        return
        
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prompts', 'synth_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        synth_prompt_tpl = f.read()
        
    final_prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prompts', 'synth_final_prompt.txt')
    with open(final_prompt_path, 'r', encoding='utf-8') as f:
        final_prompt_tpl = f.read()
        
    report_sections = []
    
    for i, q in enumerate(QUESTIONS):
        print(f"Synthesizing answer for Q{i+1}: {q}")
        
        prompt = synth_prompt_tpl.replace('{question}', q)
        prompt = prompt.replace('{count}', str(data_summary['count']))
        prompt = prompt.replace('{themes}', data_summary['themes'])
        prompt = prompt.replace('{severities}', data_summary['severities'])
        prompt = prompt.replace('{quotes}', data_summary['quotes'])
        
        success = False
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                answer = response.text
                report_sections.append(f"## {q}\n\n{answer}\n")
                success = True
                break
            except Exception as e:
                print(f"  -> Attempt {attempt+1} failed for Q{i+1}: {e}")
                if "429" in str(e) or "quota" in str(e).lower():
                    print("  -> Hit Gemini Pro Rate Limit. Sleeping for 65 seconds...")
                    time.sleep(65)
                else:
                    time.sleep(10)
                    
        if not success:
            report_sections.append(f"## {q}\n\n*Error generating insights for this question due to API failure.*")
            
        time.sleep(15) # avoid rate limits on Pro model
        
    print("Generating Final Executive Summary and Unmet Needs...")
    combined_report = "\n---\n".join(report_sections)
    final_prompt = final_prompt_tpl.replace('{report_text}', combined_report)
    
    success = False
    for attempt in range(3):
        try:
            final_response = model.generate_content(final_prompt)
            final_section = final_response.text
            success = True
            break
        except Exception as e:
            print(f"  -> Attempt {attempt+1} failed for Final Section: {e}")
            if "429" in str(e) or "quota" in str(e).lower():
                print("  -> Hit Gemini Pro Rate Limit. Sleeping for 65 seconds...")
                time.sleep(65)
            else:
                time.sleep(10)
                
    if not success:
        final_section = "*Error generating executive summary.*"
        
    # Compile full markdown
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    full_markdown = f"# Spotify Discovery Insights Report\n*Generated on {today}*\n\n{final_section}\n\n---\n\n{combined_report}"
    
    os.makedirs('reports', exist_ok=True)
    report_filename = f"reports/insight_report_{today}.md"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(full_markdown)
        
    # Save JSON snapshot
    snapshot_data = {
        "date": today,
        "total_analyzed": data_summary['count'],
        "themes": json.loads(data_summary['themes']),
        "severities": json.loads(data_summary['severities']),
        "quotes_used": data_summary['raw_quotes_list']
    }
    
    with open(f"reports/data_snapshot_{today}.json", 'w', encoding='utf-8') as f:
        json.dump(snapshot_data, f, indent=2)
        
    print(f"\nSynthesis Complete! Report saved to {report_filename}")

if __name__ == '__main__':
    run()
