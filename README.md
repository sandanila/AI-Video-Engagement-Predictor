📺 YouTube Video Engagement Predictor

An AI-based machine learning application that predicts the potential view count of a YouTube video based on its metadata before it is published.

🚀 Overview
This project uses a Random Forest Regressor model to analyze various factors that influence video reach. It helps content creators understand how their video might perform based on scheduling and title optimization.

📊 Key Features
Engagement Prediction: Estimates views based on Category, Time, and Title length.

Data-Driven Insights: Uses historical YouTube trending data for training.

Interactive Visualization: Includes analysis of trends like "Views vs Likes" and "Average views per Category."

🛠️ Technologies Used
Language: Python

Libraries: Pandas, Scikit-learn, Matplotlib, Seaborn, Joblib

Model: Random Forest Regressor

Framework: Django (Frontend/Backend Integration)

📈 Model Performance
R-squared Score: ~0.33 (Current version)

Features used: category_id, publish_hour, publish_day, title_length, tag_count

📂 Project Structure
AI-Video-Engagement-Predictor.ipynb - Data analysis and model training code.

video_model.pkl - The trained AI model file.

youtube_project/ - Django web application folder.

👷 How to Run
Clone the repository.

Install dependencies: pip install pandas scikit-learn django joblib

Run the Django server: python manage.py runserver
