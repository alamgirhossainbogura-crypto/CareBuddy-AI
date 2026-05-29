# app.py
import os
import sys
import requests

# ==========================================
# ১. কনফিগারেশন পার্ট (নিরাপদ আর্কিটেকচার)
# ==========================================
# গিটহাবে পুশ করার জন্য এপিআই কি সরাসরি কোড থেকে সরিয়ে এনভায়রনমেন্ট ভেরিয়েবলে সেট করা হলো
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
MODEL_NAME = "gemini-3.5-flash"  # <--- লেটেস্ট মডেলে আপডেট করা হলো

# ==========================================
# ২. সিস্টেম প্রম্পট
# ==========================================
SYSTEM_PROMPT = """
You are "CareBuddy AI", a specialized medical first-aid and nursing guidance assistant. 
Your goal is to provide helpful, accurate, and safe guidance strictly within these 3 categories:
1. Emergency & First Aid (e.g., cuts, burns, insect bites, initial stroke response).
2. Maternal & Child Care (e.g., newborn jaundice, mild fever, diarrhea, pregnancy nutrition).
3. Chronic Disease Care Management (e.g., how to check blood sugar, managing high blood pressure through lifestyle).

Rules you must follow:
- Respond in the language the user asks (Bengali or English).
- Be polite, empathetic, and professional.
- Do NOT prescribe antibiotics, high-power medicines, or make complex medical diagnoses.
- If a query is outside these 3 categories or seems like a severe emergency, politely tell the user to seek immediate professional medical help.

At the very end of EVERY response, you MUST append the following text exactly as written:

---
⚠️ **NB (সতর্কতা):** এটি একটি AI-চালিত প্রাথমিক স্বাস্থ্যসেবা ও নার্সিং গাইডলাইন অ্যাসিস্ট্যান্ট। এটি কোনো অবস্থাতেই একজন রেজিস্টার্ড ডাক্তারের সরাসরি বিকল্প নয় এবং দীর্ঘমেয়াদী বা জটিল রোগ নিরাময়ের উদ্দেশ্যে তৈরি করা হয়নি। যেকোনো জরুরি পরিস্থিতি বা চূড়ান্ত চিকিৎসার সিদ্ধান্ত নেওয়ার আগে অবশ্যই একজন পেশাদার ডাক্তারের পরামর্শ নিন।
""" #

# ==========================================
# ৩. মেইন ইঞ্জিন
# ==========================================
def generate_carebuddy_response(user_message):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}" #
    
    headers = {
        'Content-Type': 'application/json'
    } #
    
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        }
    } #
    
    try:
        response = requests.post(url, json=payload, headers=headers) #
        
        if response.status_code != 200:
            return f"সার্ভার ত্রুটি (স্ট্যাটাস কোড: {response.status_code})" #
            
        response_data = response.json() #
        
        if 'candidates' in response_data:
            return response_data['candidates'][0]['content']['parts'][0]['text'] #
        elif 'error' in response_data:
            return f"API ত্রুটি: {response_data['error']['message']}" #
        else:
            return "দুঃখিত, কোনো উত্তর পাওয়া যায়নি।" #
    except Exception as e:
        return f"নেটওয়ার্ক সমস্যা: {e}" #

def main():
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print("ভুল: অনুগ্রহ করে আপনার পরিবেশ ভেরিয়েবলে বা কোডে সঠিক API Key সেট করুন!")
        sys.exit(1)
        
    print("==================================================")
    print("   CareBuddy AI - প্রাথমিক চিকিৎসা ও নার্সিং গাইড   ")
    print("==================================================")
    print("বটটি সফলভাবে চালু হয়েছে! (বন্ধ করতে 'exit' লিখুন)\n") #
    
    while True:
        user_input = input("আপনার স্বাস্থ্য সমস্যা বা প্রশ্নটি লিখুন: ") #
        if user_input.strip().lower() == 'exit':
            print("CareBuddy AI ব্যবহার করার জন্য ধন্যবাদ।") #
            break
            
        if not user_input.strip():
            continue
            
        print("\nCareBuddy AI উত্তর তৈরি করছে...") #
        reply = generate_carebuddy_response(user_input) #
        
        print("\n--------------------------------------------------")
        print(reply)
        print("--------------------------------------------------\n") #

if __name__ == "__main__":
    main() #
