
# 🌿 Leaflytic

**Leaflytic** is a machine learning-powered web application that identifies plant leaf diseases with a model accuracy of **92%**. Users can upload images of plant leaves to get instant predictions, making it a valuable tool for farmers, gardeners, and plant pathologists.

---

## 🚀 Features

* 🌱 **Leaf Disease Detection** using a trained ML model
* 📷 **Image Upload** from device or camera
* 📊 **92% Model Accuracy** on test dataset
* 💻 **Simple Web Interface** built using Flask
* 📱 **Responsive Design** with HTML, CSS, JavaScript

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/umamanipraharshitha/Leaflytic.git
   cd Leaflytic
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   python leaflytic.py
   ```

5. **Open in Browser**

   Navigate to: [http://localhost:5000](http://localhost:5000)

---


### 🧠 ML Model Details – *Leaflytic*

🔍 **Goal**: Classify plant leaf images into different disease categories or as healthy.

📦 **Dataset**: [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)

* Pre-split into `train`, `val`, and `test` folders.
* Contains thousands of images across multiple plant disease classes.

⚙️ **Model Architecture**:

* **Base**: [MobileNetV2](https://arxiv.org/abs/1801.04381) (pre-trained on ImageNet)

  * Used for transfer learning (lightweight, fast, and accurate)
  * Frozen convolutional base to retain learned features
* **Top layers**:

  * `GlobalAveragePooling2D`
  * `Dense(128)` with ReLU
  * `Dropout(0.3)`
  * `Dense` with softmax (for multi-class classification)

📐 **Input Size**: 224 × 224 pixels
🎛 **Preprocessing**: Image augmentation (flip, rotate, zoom) to improve generalization.

🧪 **Training Setup**:

* **Optimizer**: Adam
* **Loss Function**: Categorical Crossentropy
* **Epochs**: 10
* **Batch Size**: 32
* **Callbacks**: EarlyStopping & ModelCheckpoint

📊 **Performance**:

* **Test Accuracy**: ✅ \~92%
* Validated using a separate test set with no data leakage



## 🧪 How to Use

1. Upload a plant leaf image.
2. Click **Submit** to get a prediction.
3. View the **disease result and confidence**.
4. Try another image if needed.

---

## 🧠 Model Info

* Model Type: Convolutional Neural Network (CNN)
* Accuracy: **92%** on validation dataset
* Trained using TensorFlow/Keras
* Input: Leaf image
* Output: Predicted disease name and confidence

---
## 📑 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Credits

* [Flask](https://flask.palletsprojects.com/)
* [TensorFlow/Keras](https://keras.io/)
* [Pillow](https://python-pillow.org/)
* Dataset used from Kaggle/PlantVillage

---

