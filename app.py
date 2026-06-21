from flask import Flask, request, render_template_string, url_for
import os
import pickle
import numpy as np

app = Flask(__name__)

# Ensure the required model artifacts are available during deployment
required_artifacts = ['model.pkl', 'scaler.pkl', 'features.pkl']
missing_artifacts = [path for path in required_artifacts if not os.path.exists(path)]
if missing_artifacts:
    raise FileNotFoundError(
        'Missing required deployment artifacts: ' + ', '.join(missing_artifacts) +
        '.\nEnsure model.pkl, scaler.pkl, and features.pkl are present in the repository or uploaded to the deployment environment.'
    )

# Load the optimized 7-feature model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('features.pkl', 'rb') as f:
    features_list = pickle.load(f)

# Faded background placeholders
example_placeholders = {
    'flow_duration': '4521.0', 
    'total_forward_packets': '4.0', 
    'total_backward_packets': '3.0',
    'forward_iat_mean': '120.0',
    'backward_iat_mean': '95.0',
    'flow_packets_per_seconds': '1547.0',
    'flow_bytes_per_seconds': '109200.0'
}

# Simple, short definitions for the UI
feature_descriptions = {
    'flow_duration': 'Total time the connection remained active (in microseconds).',
    'total_forward_packets': 'Total number of packets sent to the destination.',
    'total_backward_packets': 'Total number of packets received back from the destination.',
    'forward_iat_mean': 'Average time delay between sending consecutive packets.',
    'backward_iat_mean': 'Average time delay between receiving consecutive packets.',
    'flow_packets_per_seconds': 'Speed of the connection measured in packets per second.',
    'flow_bytes_per_seconds': 'Data volume speed measured in bytes per second.'
}

html_layout = """
<!DOCTYPE html>
<html>
<head>
    <title>NIDS Stream Analytics</title>
    <style>
        /* 1. Set the uploaded image as the fixed, full-screen background */
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0;
            padding: 40px; 
            min-height: 100vh;
            background-image: url("{{ url_for('static', filename='sc.jpeg') }}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        /* 2. The Glassmorphism Card: Semi-transparent dark background with a blur filter */
        .card { 
            background: rgba(15, 23, 42, 0.85); /* Dark blue/slate tint */
            backdrop-filter: blur(12px);        /* The frosted glass blur effect */
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.15); /* Thin glowing edge */
            padding: 35px; 
            border-radius: 16px; 
            width: 100%;
            max-width: 650px; 
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6); 
        }

        h2 { text-align: center; color: #ffffff; margin-bottom: 5px; text-shadow: 0 2px 10px rgba(0,255,255,0.3); }
        .sub { text-align: center; color: #cbd5e1; font-size: 14px; margin-bottom: 30px; letter-spacing: 1px;}
        
        .input-group { 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 1px solid rgba(255, 255, 255, 0.1); 
            padding-bottom: 15px;
        }
        
        .label-container { width: 55%; }
        label { color: #f8fafc; font-weight: 600; font-size: 15px; text-transform: capitalize; display: block; margin-bottom: 4px;}
        .desc { color: #94a3b8; font-size: 12px; line-height: 1.4; }
        
        /* 3. The Input Boxes: Slightly transparent with bright cyan borders on click */
        input[type="number"] { 
            width: 40%; 
            padding: 10px; 
            background: rgba(255, 255, 255, 0.05); /* Ghost background */
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2); 
            border-radius: 6px; 
            font-size: 15px; 
            box-sizing: border-box;
            transition: all 0.3s ease;
        }
        
        input[type="number"]:focus { 
            border-color: #06b6d4; /* Cyan glow matching your background image */
            background: rgba(255, 255, 255, 0.1);
            outline: none; 
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.5);
        }
        
        ::placeholder { color: rgba(255, 255, 255, 0.3); font-style: italic; }
        
        /* 4. The Submit Button: Vibrant gradient */
        button { 
            background: linear-gradient(135deg, #0ea5e9, #2563eb); 
            color: white; 
            border: none; 
            padding: 14px; 
            font-size: 16px; 
            font-weight: 700; 
            cursor: pointer; 
            border-radius: 8px; 
            width: 100%; 
            margin-top: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.4); 
        }
        
        /* 5. The Output Alerts (Adapted for dark mode) */
        .output-box { margin-top: 25px; padding: 15px; border-radius: 8px; text-align: center; font-size: 18px; font-weight: bold; backdrop-filter: blur(5px); }
        .danger-alert { background: rgba(153, 27, 27, 0.7); color: #fca5a5; border: 1px solid #f87171; }
        .safe-alert { background: rgba(22, 101, 52, 0.7); color: #86efac; border: 1px solid #4ade80; }
        .error-alert { background: rgba(154, 52, 18, 0.7); color: #fdba74; border: 1px solid #fb923c; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🛡️ Network Intrusion Diagnostics</h2>
        <div class="sub">AI-Powered Anomaly Detection Engine</div>
        
        <form method="POST" action="/">
            {% for feature in features %}
                <div class="input-group">
                    <div class="label-container">
                        <label>{{ feature.replace('_', ' ') }}</label>
                        <div class="desc">{{ descriptions[feature] }}</div>
                    </div>
                    <input type="number" step="any" name="{{ feature }}" placeholder="Example: {{ placeholders.get(feature, '0.0') }}" required>
                </div>
            {% endfor %}
            
            <button type="submit">Execute Traffic Scan</button>
        </form>
        
        {% if report_text %}
            <div class="output-box {{ alert_class }}">
                {{ report_text }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    report_text = ""
    alert_class = ""

    if request.method == 'POST':
        try:
            input_values = []
            for feature in features_list:
                val = float(request.form[feature])
                input_values.append(val)
            
            feature_matrix = np.array(input_values).reshape(1, -1)
            scaled_features = scaler.transform(feature_matrix)
            prediction = model.predict(scaled_features)
            
            if prediction[0] == 1:
                report_text = "🚨 THREAT DETECTED: DrDoS Attack Signature"
                alert_class = "danger-alert"
            else:
                report_text = "✅ SYSTEM SECURE: Normal Traffic Flow"
                alert_class = "safe-alert"
                
        except Exception as error:
            report_text = f"Error: Please fill all fields with valid numbers. System log: {error}"
            alert_class = "error-alert"

    return render_template_string(
        html_layout, 
        features=features_list, 
        placeholders=example_placeholders,
        descriptions=feature_descriptions,
        report_text=report_text, 
        alert_class=alert_class
    )

if __name__ == '__main__':
    app.run(debug=True)