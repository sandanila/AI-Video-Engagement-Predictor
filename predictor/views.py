from django.shortcuts import render
import joblib
import os
from django.conf import settings
import random

model_path = os.path.join(settings.BASE_DIR, 'predictor', 'video_model.pkl')
try:
    model = joblib.load(model_path)
except Exception as e:
    model = None

def home(request):
    prediction = None
    result_color = "#28a745"
    analysis = None
    recommendations = []
    suggested_titles = []
    selected_lang = request.POST.get('language', 'en')

    chart_labels = ["12am", "4am", "8am", "12pm", "4pm", "8pm", "11pm"]
    chart_data = [120000, 80000, 450000, 900000, 1500000, 2800000, 1800000]

    texts = {
        'en': {
            'title': 'Video Engagement Predictor',
            'cat_label': 'Category ID',
            'hour_label': 'Upload Hour (0-23)',
            'day_label': 'Day of Week (0-6)',
            'len_label': 'Title Length',
            'tag_label': 'Tag Count',
            'btn': 'Predict Engagement',
            'advice_head': '💡 Optimization Tips:',
            'result_label': 'Predicted Views'
        },
        'si': {
            'title': 'වීඩියෝ ප්‍රතිචාර අනුමානකය',
            'cat_label': 'වර්ගීකරණ අංකය (Category ID)',
            'hour_label': 'පළ කරන වේලාව (0-23)',
            'day_label': 'සතියේ දිනය (0-6)',
            'len_label': 'මාතෘකාවේ දිග',
            'tag_label': 'ටැග් ගණන',
            'btn': 'අනුමාන කරන්න',
            'advice_head': '💡 වැඩි දියුණු කිරීමට උපදෙස්:',
            'result_label': 'අනුමානිත දර්ශන වාර'
        }
    }

    content = texts.get(selected_lang)

    if request.method == 'POST':
        try:
            cat_id = int(request.POST.get('category', 0))
            hour = int(request.POST.get('hour', 0))
            day = int(request.POST.get('day', 0))
            title_len = int(request.POST.get('title_len', 0))
            tag_count = int(request.POST.get('tag_count', 0))

            if model:
                input_data = [[cat_id, hour, day, title_len, tag_count]]
                result = model.predict(input_data)
                prediction_value = int(result[0])
                prediction = f"{prediction_value:,}"
                result_color = "#28a745" if prediction_value > 1000000 else "#dc3545"

                analysis = {
                    'best_time': '18:00 - 21:00 (Evening)',
                    'best_days': 'Friday, Saturday'
                }

                # 3. Optimization Recommendations
                if selected_lang == 'si':
                    if title_len < 30: recommendations.append("මාතෘකාව (Title) කෙටි වැඩියි. තව ටිකක් විස්තර එක් කරන්න.")
                    if tag_count < 10: recommendations.append("ටැග් (Tags) 10කට වඩා එක් කිරීමෙන් වැඩි පිරිසක් අතරට යා හැක.")
                else:
                    if title_len < 30: recommendations.append("Your title is too short. Try adding descriptive keywords.")
                    if tag_count < 10: recommendations.append("Using more than 10 tags helps increase reach.")

                # 4. Title Suggestions Logic
                title_templates = {
                    'si': [
                        "අනිවාර්යයෙන්ම බලන්න! {cat} ගැන ඔබ නොදත් රහස්",
                        "2026 වසරේ {cat} නවතම පෙරළිය",
                        "විනාඩි 10 කින් {cat} ගැන ඉගෙන ගනිමු",
                        "ඔබේ {cat} වීඩියෝ එක Viral කරගන්න රහස්"
                    ],
                    'en': [
                        "Don't Miss This! Secret Tips for {cat}",
                        "The Future of {cat} in 2026",
                        "Mastering {cat} in 10 Minutes",
                        "How to make your {cat} video go Viral"
                    ]
                }

                category_names = {10: "Music", 24: "Entertainment", 20: "Gaming", 28: "Tech"}
                current_cat_name = category_names.get(cat_id, "this category")

                suggested_titles = random.sample(title_templates[selected_lang], 2)
                suggested_titles = [t.format(cat=current_cat_name) for t in suggested_titles]

        except Exception as e:
            prediction = f"Error: {e}"

    context = {
        'prediction': prediction,
        'result_color': result_color,
        'analysis': analysis,
        'recommendations': recommendations,
        'suggested_titles': suggested_titles,
        'selected_lang': selected_lang,
        'content': content,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    return render(request, 'predictor/home.html', context)
