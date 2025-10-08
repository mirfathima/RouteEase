from flask import Flask, request, render_template
import joblib
import datetime

app = Flask(__name__)

# Load your trained model
model = joblib.load('best_model.pkl')

# Mapping days of the week to integers
days_map = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract and convert form data
        time_str = request.form['Time']
        date_str = request.form['Date']
        day_of_week_str = request.form['DayOfWeek']

        # Convert time to an integer representing the hour (0-23)
        time_obj = datetime.datetime.strptime(time_str, '%H:%M')
        time_int = time_obj.hour

        # Convert date to an integer representing the day of the year
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        date_int = date_obj.timetuple().tm_yday

        # Convert day of the week to an integer using the mapping
        day_of_week_int = days_map[day_of_week_str]

        # Feature list for the prediction model
        features = [time_int, date_int, day_of_week_int]

        # Make prediction
        prediction = model.predict([features])[0]

        # Assuming prediction is a list with car, bike, bus, truck, and total counts
        car_count = prediction[0]
        bike_count = prediction[1]
        bus_count = prediction[2]
        truck_count = prediction[3]
        total_count = prediction[4]

        # Determine traffic situation based on total count
        traffic_situation = "High" if total_count > 100 else "Moderate" if total_count > 50 else "Low"

        # Render result template with prediction data
        return render_template('result.html', 
                               car_count=car_count, 
                               bike_count=bike_count,
                               bus_count=bus_count, 
                               truck_count=truck_count, 
                               total_count=total_count,
                               traffic_situation=traffic_situation)
    except Exception as e:
        # Handle errors gracefully
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
