import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

class EyeHealthModel:
    def __init__(self, data_path='eyes.csv', model_path='eye_model.joblib'):
        self.data_path = data_path
        self.model_path = model_path
        self.model = None
        self.features = ['Sleep_Hours', 'Vitamin_A_Intake']
        self.target = 'Eye_Health'
        
        # Load or train
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.train()

    def load_data(self):
        if not os.path.exists(self.data_path):
            # Fallback to local directory if full path fails
            path = os.path.join(os.path.dirname(__file__), 'eyes.csv')
            if not os.path.exists(path):
                # Try bestfit.csv if eyes.csv is missing
                path = os.path.join(os.path.dirname(__file__), 'bestfit.csv')
            return pd.read_csv(path, skipinitialspace=True)
        return pd.read_csv(self.data_path, skipinitialspace=True)

    def train(self):
        try:
            df = self.load_data()
            df.dropna(subset=self.features + [self.target], inplace=True)
            
            X = df[self.features]
            y = df[self.target]
            
            self.model = LinearRegression()
            self.model.fit(X, y)
            
            joblib.dump(self.model, self.model_path)
            return True
        except Exception as e:
            print(f"Training failed: {e}")
            return False

    def predict(self, sleep_hours, vitamin_a, screen_time=6.8, luminance=450):
        # Implement the mandatory mathematical constraint formula:
        # Eye Health = (Sleep * 8) - (ScreenTime * 3) + (Vitamin A * 0.05)
        raw_score = (sleep_hours * 8) - (screen_time * 3) + (vitamin_a * 0.05)
        
        # Keep it bounded between 0 and 100
        return max(0, min(100, raw_score))

    def get_insights(self, score):
        if score > 85:
            return "OPTIMAL", "#4edea3", "Your vision metrics are in the top 5th percentile."
        elif score > 50:
            return "NORMAL", "#4edea3", "All biocentric markers are within standard physiological ranges."
        else:
            return "AT RISK", "#ff7886", "Significant neural-visual strain detected."

    def get_realtime_metrics(self, luminance, sleep):
        # Simulated real-time metrics based on inputs
        ocular_drift = max(0.01, min(0.05, (12 - sleep) * 0.005))
        tear_stability = "Stable" if luminance < 1000 and sleep > 6 else "Unstable"
        return f"{ocular_drift:.2f}%", tear_stability

    def generate_patients(self):
        import random
        patients = []
        for i in range(15):
            sleep = round(random.uniform(4.0, 10.0), 1)
            screen = round(random.uniform(2.0, 15.0), 1)
            vitamin = random.randint(400, 1500)
            health = round((sleep * 8) - (screen * 3) + (vitamin * 0.05))
            health = max(0, min(100, health))
            
            inf = "NORMAL"
            inf_class = "status-normal"
            if health > 85:
                inf, inf_class = "OPTIMAL", "status-optimal"
            elif health <= 50:
                inf, inf_class = "AT RISK", "status-risk"
                
            patients.append({
                "patient_id": f"#VS-{random.randint(8000, 9999)}",
                "sleep": sleep,
                "screen": screen,
                "health": health,
                "inf": inf,
                "class": inf_class
            })
        return pd.DataFrame(patients)
