from flask import Flask, redirect, url_for, session, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import io
import os
from werkzeug.utils import secure_filename

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import google.auth.transport.requests
from functools import wraps  # for proper login_required
model = load_model('leaf_disease_model.keras')
app = Flask(__name__)
app.secret_key = "leaflytic3"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLIENT_SECRETS_FILE = "client_secret.json"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_uri="http://127.0.0.1:5000/callback"
)

print("Loaded client config:", flow.client_config)
CLASS_NAMES = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url(prompt="consent")
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    try:
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        request_session = google.auth.transport.requests.Request()
        user_info = id_token.verify_oauth2_token(
            credentials.id_token, request_session, flow.client_config['client_id'])

        session["user"] = {
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "picture": user_info.get("picture")
        }

        return redirect(url_for("about"))
    except Exception as e:
        print(f"Error during callback: {e}")
        return f"Error: {e}"

# ✅ Properly decorated login_required
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ✅ Pages requiring login
@app.route("/completesignup")
@login_required
def completesignup():
    return render_template("completesignup.html", user=session["user"])

@app.route("/leaflens")
@login_required
def leaflens():
    return render_template("leaflens.html", user=session["user"])

@app.route("/search")
@login_required
def search():
    return render_template("search.html", user=session["user"])



# ✅ Public pages
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
def prepare_image(image, target_size=(224, 224)):
    """Convert uploaded image to model input format."""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize(target_size)
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = image_array / 255.0  # Normalize if model trained on normalized images
    return image_array
@app.route('/predict', methods=['POST'])
def predict():
    if 'leaf_image' not in request.files:
        return "No file part", 400

    file = request.files['leaf_image']
    if file.filename == '':
        return "No selected file", 400

    try:
        # Save the image
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Open and preprocess image
        image = Image.open(file_path)
        processed_image = prepare_image(image)
        preds = model.predict(processed_image)
        pred_index = np.argmax(preds)
        pred_label = CLASS_NAMES[pred_index]
        confidence = preds[0][pred_index]

        # Generate URL to display image
        uploaded_image_url = url_for('static', filename='uploads/' + filename)

        return render_template('results.html',
                               prediction=pred_label,
                               confidence=round(float(confidence) * 100, 2),
                               uploaded_image_url=uploaded_image_url)
    except Exception as e:
        return f"Error during prediction: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)
