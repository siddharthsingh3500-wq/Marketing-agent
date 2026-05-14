from flask import Flask, render_template, request, jsonify
from groq import Groq
import requests
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def scrape_website(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        text = ' '.join(text.split())
        return text[:3000]
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    company_name = data.get('company_name')
    industry = data.get('industry')
    budget = data.get('budget')
    goal = data.get('goal')
    location = data.get('location')
    employees = data.get('employees')
    challenge = data.get('challenge')
    target_age = data.get('target_age')
    marketing_channels = data.get('marketing_channels')
    business_type = data.get('business_type')
    website_url = data.get('website_url')

    website_context = ""
    if website_url:
        scraped = scrape_website(website_url)
        if scraped:
            website_context = f"""

IMPORTANT - Website Analysis:
The following content was extracted directly from the company website.
Use this to make strategies highly specific and personalized:
{scraped}
"""

    prompt = f"""
You are an expert marketing strategist. Analyze this company profile and generate exactly 3 distinct marketing strategies.

Company Profile:
- Company Name: {company_name}
- Industry: {industry}
- Business Type: {business_type}
- Budget: {budget}
- Primary Goal: {goal}
- Location: {location}
- Number of Employees: {employees}
- Target Age Group: {target_age}
- Current Marketing Channels: {marketing_channels}
- Biggest Challenge: {challenge}
{website_context}

Output format — follow this EXACTLY for each strategy. Each item must be on its own NEW LINE:

Strategy 1
Strategy Name: [name here]
Why It Fits:
- [reason 1]
- [reason 2]
Key Channels:
- [channel 1 with one line explanation]
- [channel 2 with one line explanation]
- [channel 3 with one line explanation]
Timeline:
- [timeline details]
Expected ROI:
- [High / Medium / Low with one line reason]

Strategy 2
Strategy Name: [name here]
Why It Fits:
- [reason 1]
- [reason 2]
Key Channels:
- [channel 1 with one line explanation]
- [channel 2 with one line explanation]
- [channel 3 with one line explanation]
Timeline:
- [timeline details]
Expected ROI:
- [High / Medium / Low with one line reason]

Strategy 3
Strategy Name: [name here]
Why It Fits:
- [reason 1]
- [reason 2]
Key Channels:
- [channel 1 with one line explanation]
- [channel 2 with one line explanation]
- [channel 3 with one line explanation]
Timeline:
- [timeline details]
Expected ROI:
- [High / Medium / Low with one line reason]

STRICT RULES:
- Every bullet point MUST be on its own separate line
- Never put multiple bullet points on the same line
- Never use ## or ** or any markdown
- Never write in paragraph form
- Each section title ends with a colon
{"- Use specific details from the website data to make strategies personalized" if website_context else ""}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    result = response.choices[0].message.content
    return jsonify({"strategy": result})

@app.route('/refine', methods=['POST'])
def refine():
    data = request.json
    original_strategy = data.get('original_strategy')
    user_choice = data.get('user_choice')
    refinement = data.get('refinement')
    company_profile = data.get('company_profile')

    prompt = f"""
You are an expert marketing strategist.

Company Profile: {company_profile}
Chosen Strategy: {user_choice}
Additional Requirements: {refinement}

Generate a detailed marketing strategy report. Follow this EXACT format.
Every bullet point on its own NEW LINE. Never use ## or **. Never write paragraphs.

EXECUTIVE SUMMARY
- [point 1]
- [point 2]
- [point 3]

TARGET AUDIENCE
- [point 1]
- [point 2]
- [point 3]

MARKETING CHANNELS
- [channel]: [one line explanation]
- [channel]: [one line explanation]
- [channel]: [one line explanation]

BUDGET ALLOCATION
- [category]: [percentage and amount]
- [category]: [percentage and amount]
- [category]: [percentage and amount]

90-DAY ACTION PLAN
Day 1-30:
- [action 1]
- [action 2]
- [action 3]
Day 31-60:
- [action 1]
- [action 2]
- [action 3]
Day 61-90:
- [action 1]
- [action 2]
- [action 3]

KEY PERFORMANCE INDICATORS
- [KPI 1]
- [KPI 2]
- [KPI 3]

EXPECTED RESULTS
- [result 1]
- [result 2]
- [result 3]

STRICT RULES:
- Every bullet on its own line
- Never combine multiple bullets on one line
- No markdown, no ## or **
- No paragraphs
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    result = response.choices[0].message.content
    return jsonify({"report": result})

if __name__ == '__main__':
    app.run(debug=True)
