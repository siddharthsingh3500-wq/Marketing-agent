from flask import Flask, render_template, request, jsonify
from groq import Groq
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

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

    prompt = f"""
    You are an expert marketing strategist. Analyze this company profile and generate 3 distinct marketing strategies.
    
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
    
    For each strategy provide ONLY in bullet points:
    • Strategy Name (one line)
    • Why it fits this company (2 bullets)
    • Key Channels to use (2-3 bullets)
    • Timeline (1 bullet)
    • Expected ROI: High / Medium / Low (1 bullet)
    
    Keep each strategy concise and scannable. No long paragraphs.
    Use Strategy 1, Strategy 2, Strategy 3 as headers.
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
    
    Generate a detailed marketing strategy report in bullet points only. Use this structure:
    
    EXECUTIVE SUMMARY
    • 3 bullet points max
    
    TARGET AUDIENCE
    • 3 bullet points max
    
    MARKETING CHANNELS
    • One bullet per channel with brief explanation
    
    BUDGET ALLOCATION
    • One bullet per category with percentage
    
    90-DAY ACTION PLAN
    • Day 1-30: 3 bullets
    • Day 31-60: 3 bullets
    • Day 61-90: 3 bullets
    
    KEY PERFORMANCE INDICATORS
    • One bullet per KPI
    
    EXPECTED RESULTS
    • 3 bullets max
    
    Keep everything scannable. No long paragraphs. Be specific and actionable.
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