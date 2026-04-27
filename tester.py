from ml_engine import EyeHealthModel

def getPrediction():
    model = EyeHealthModel()
    print('====================================')
    print('   Eye Health Diagnostics Console   ')
    print('====================================')
    
    try:
        sleep = float(input('Enter sleep hours (e.g. 7.5): '))
        vitamin = float(input('Enter Vitamin A intake (e.g. 900): '))
        
        prediction = model.predict(sleep, vitamin)
        status, color, message = model.get_insights(prediction)
        
        print(f'\n[RESULT]')
        print(f'Prediction Score: {prediction:.2f}')
        print(f'Status: {status}')
        print(f'Insight: {message}')
        print('====================================')
    except ValueError:
        print("Invalid input. Please enter numbers.")

if __name__ == "__main__":
    getPrediction()
