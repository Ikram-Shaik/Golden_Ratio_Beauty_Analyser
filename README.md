# ✨ Golden Ratio Beauty Analyzer

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-007F7F?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

A web application that analyzes facial features from an image to calculate its alignment with the mathematical Golden Ratio (Φ ≈ 1.618).

---

## 📸 App Preview

![App Screenshot](https://github.com/Ikram-Shaik/Golden_Ratio_Beauty_Analyser/blob/main/app_screenshot.jpg)

---

## 📖 About The Project

This project is an interactive web app built with **Streamlit** that uses **Google's MediaPipe** library to perform real-time facial landmark detection. It takes a user-provided image (either through upload or webcam) and calculates several key facial proportions. These proportions are then compared to the Golden Ratio to generate an "Overall Beauty Score" and a detailed breakdown of each measurement.

The app is designed to be a fun and educational tool to explore the mathematical concepts of beauty and proportion.

---

## 🚀 Features

* **Dual Input Methods:** Upload an image file or use your webcam for real-time capture.
* **Advanced Facial Landmark Detection:** Utilizes MediaPipe Face Mesh to detect 478 key points on the face.
* **Comprehensive Ratio Analysis:** Calculates three key facial ratios:
    * Face Length / Face Width
    * Lips-Chin / Nose-Lips
    * Mouth Width / Nose Width
* **Detailed Scoring:** Provides an "Overall Beauty Score" as well as individual scores for each calculated ratio.
* **Visual Feedback:** Overlays the detected landmarks and measurement lines on the user's photo.
* **Responsive UI:** Features a clean, dark-theme interface with clear instructions and results.

---

## 🛠️ Tech Stack

* **Backend:** Python
* **Frontend/Web Framework:** Streamlit
* **Computer Vision:** OpenCV
* **Facial Landmark Detection:** MediaPipe
* **Numerical Operations:** NumPy

---

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/Ikram-Shaik/Golden_Ratio_Beauty_Analyser.git](https://github.com/Ikram-Shaik/Golden_Ratio_Beauty_Analyser.git)
cd golden_ratio_analyzer
````

**2. Create and activate a virtual environment (recommended):**

  * **macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  * **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

**3. Install the required libraries:**
Create a `requirements.txt` file with the following content:

```
streamlit
opencv-python
mediapipe
numpy
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

**4. Run the Streamlit app:**
Make sure your Python script is named `main.py` (or change the command accordingly).

```bash
streamlit run main.py
```

The application should now be running and accessible in your web browser.

-----

## Usage

1.  Open the application in your browser.
2.  Choose your input method: "Upload an Image" or "Use Webcam".
3.  Follow the on-screen photo guidelines for the best results.
4.  Upload a photo or take a picture.
5.  Wait for the analysis to complete.
6.  View your "Overall Beauty Score," the "Average Facial Ratio," and explore the "Detailed Ratio Breakdown" for more insights.

-----

## ⚖️ Disclaimer

This tool is for educational and entertainment purposes only. The concept of a "Golden Ratio Face" is a mathematical idealization. True beauty is subjective, diverse, and cannot be defined by any single algorithm or set of numbers.

-----

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

-----

## 🙏 Acknowledgments

  * Created by **Ikram Shaik**.
  * Built with the amazing **Streamlit** framework.
  * Facial analysis powered by **Google's MediaPipe**.

<!-- end list -->

```
```