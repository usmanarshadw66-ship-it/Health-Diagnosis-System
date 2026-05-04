

import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Expanded Language Dictionary
LANG_DATA = {
    "urdu": {"name": "نام", "desc": "تفصیل", "cause": "وجوہات", "treat": "علاج", "advice": "مشورہ", "msg": "آپ کو ڈاکٹر سے رجوع کرنا چاہیے۔"},
    "punjabi": {"name": "ناں", "desc": "تفصیل", "cause": "وجہ", "treat": "علاج", "advice": "مشورہ", "msg": "تہانوں ڈاکٹر کول جانا چاہیدا اے۔"},
    "english": {"name": "Disease", "desc": "Description", "cause": "Causes", "treat": "Treatment", "advice": "Advice", "msg": "You should consult a doctor."},
    "saraiki": {"name": "ناں", "desc": "تفصیل", "cause": "وجہ", "treat": "علاج", "advice": "مشورہ", "msg": "تہاکوں ڈاکٹر کول ونجنا چاہیدا ہے۔"},
    "sindhi": {"name": "نالو", "desc": "تفصيل", "cause": "سبب", "treat": "علاج", "advice": "مشورو", "msg": "توهان کي ڊاڪٽر سان ملڻ گهرجي."},
    "pashto": {"name": "نوم", "desc": "تفصیل", "cause": "وجوہات", "treat": "علاج", "advice": "مشورہ", "msg": "تاسو باید ډاکټر ته لاړ شئ."},
    "balochi": {"name": "نام", "desc": "تفصیل", "cause": "وجوہات", "treat": "علاج", "advice": "سوج", "msg": "شما را ڈاکٹرءِ کرّا روگ لوٹ ایت."},
    "hindi": {"name": "نام", "desc": "विवरण", "cause": "कारण", "treat": "उपचार", "advice": "सलाह", "msg": "आपको डॉक्टर से मिलना चाहिए।"},
    "bangali": {"name": "রোগ", "desc": "বিবরণ", "cause": "কারণ", "treat": "চিকিৎসা", "advice": "পরামর্শ", "msg": "আপনার ডাক্তারের সাথে পরামর্শ করা উচিত।"},
    "spanish": {"name": "Enfermedad", "desc": "Descripción", "cause": "Causas", "treat": "Tratamiento", "advice": "Consejo", "msg": "Debe consultar a un médico."}
}

DISEASES = {
    "flu": {
        "urdu": {"n": "نزلا زکام (Flu)", "d": "یہ ایک وائرل انفیکشن ہے۔", "c": "وائرس اور کمزور قوت مدافعت۔", "t": "آرام کریں اور گرم قہوہ پیئیں۔"},
        "english": {"n": "Influenza (Flu)", "d": "Viral infection of respiratory system.", "c": "Viruses.", "t": "Rest and fluids."},
        "punjabi": {"n": "زکام", "d": "اے اک وائرل بیماری اے۔", "c": "وائرس دی وجہ توں۔", "t": "ارام کرو تے گرم چاء پیو۔"}
    },
    "fever": {
        "urdu": {"n": "بخار (Fever)", "d": "جسم کا درجہ حرارت بڑھ جانا۔", "c": "انفیکشن یا تھکن۔", "t": "پیراسیٹامول لیں اور پٹیاں کریں۔"},
        "english": {"n": "Fever", "d": "High body temperature.", "c": "Infection or fatigue.", "t": "Paracetamol and rest."},
        "punjabi": {"n": "تھاویں بخار", "d": "جسم دا درجہ حرارت ودھ جانا۔", "c": "تھکن یا انفیکشن۔", "t": "ارام کرو تے دوائی لو۔"}
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Get user input
    symptoms = request.form.get('symptoms', '').lower()
    
    try:
        age = int(request.form.get('age', 0))
    except ValueError:
        age = 0
    
    # 2. Detect Language (Default is Urdu)
    selected_lang = "urdu"
    for lang in LANG_DATA.keys():
        if lang in symptoms:
            selected_lang = lang
            break

    # 3. Disease Matching Logic
    found_disease = "fever" # Default
    # Flu keywords detection
    flu_keywords = ["cough", "khansi", "کھانسی", "zakam", "flu", "zukaam", "nazla"]
    if any(word in symptoms for word in flu_keywords):
        found_disease = "flu"

    # 4. Fetch the specific data
    disease_info = DISEASES.get(found_disease, DISEASES['fever'])
    
    # Get content in selected language, fallback to English if not found
    lang_content = disease_info.get(selected_lang, disease_info.get('english'))
    labels = LANG_DATA[selected_lang]

    # 5. Age advice logic
    if age < 12: 
        age_msg = "بچوں کے لیے خاص احتیاط کی ضرورت ہے۔" if selected_lang=="urdu" else "Special care for kids."
    elif age > 60: 
        age_msg = "بزرگوں کے لیے فوری چیک اپ ضروری ہے۔" if selected_lang=="urdu" else "Immediate checkup for elderly."
    else: 
        age_msg = "مناسب آرام اور غذا لیں۔" if selected_lang=="urdu" else "Take proper rest."

    # 6. Generate random ID for report
    diag_id = random.randint(1000, 9999)

    # 7. Rendering the template with variables
    # Maine 'res' ko use kiya hai, isliye result.html mein bhi 'res' hona chahiye
    return render_template('result.html', 
                         res=lang_content, 
                         labels=labels, 
                         age_msg=age_msg, 
                         diag_id=diag_id,
                         severity="high" if age > 60 else "normal")

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
