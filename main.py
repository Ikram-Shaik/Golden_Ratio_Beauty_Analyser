import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import math
from PIL import Image

# --- Custom CSS for Dark Theme Compatibility ---
st.markdown("""
<style>
    /* Main app theming */
    body {
        color: #FAFAFA;
    }
    /* Header and subheader */
    .header {
        color: #FF4B4B; /* Red-orange for title */
        text-align: center;
        font-size: 2.5rem !important;
    }
    .subheader {
        color: #A0AEC0; /* Lighter grey for dark theme */
        text-align: center;
        margin-bottom: 2rem;
    }

    /* THEME FIX: This box now has a dark background */
    .result-box {
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #262730; /* Dark grey background */
        border: 1px solid #4A5568; /* Subtle border */
        color: #FAFAFA; /* Ensures text inside is light */
    }
    
    .golden-ratio {
        color: #D4AF37; /* Gold color for ratios */
        font-weight: bold;
    }
    .beauty-score {
        font-size: 1.8rem !important;
        font-weight: bold;
        text-align: center;
    }

    /* THEME FIX: Dark background for the progress bar track */
    .progress-container {
        height: 30px;
        background-color: #4A5568; /* Darker grey for the track */
        border-radius: 15px;
        margin: 1rem 0;
    }
    .progress-bar {
        height: 100%;
        border-radius: 15px;
        background: linear-gradient(90deg, #F59E0B, #EF4444);
        transition: width 0.5s ease-in-out;
    }

    /* THEME FIX: Dark background for radio buttons */
    .stRadio > div {
        background-color: #262730; /* Dark grey background */
        border: 1px solid #4A5568; /* Subtle border */
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Buttons (unchanged, already looks good) */
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(
    page_title="Golden Ratio Beauty Analyzer",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- App Header ---
st.markdown('<p class="header">✨ Golden Ratio Beauty Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Discover how closely your facial features align with the golden ratio (1.618)</p>', unsafe_allow_html=True)

# --- MediaPipe Initialization ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)
GOLDEN_RATIO = 1.6180339887

# --- Input Method ---
option = st.radio(
    "Choose Image Input Method:",
    ["Upload an Image", "Use Webcam"],
    horizontal=True
)

# --- Photo Guidelines ---
with st.expander("📸 Photo Guidelines for Best Results"):
    st.markdown("""
    - **Face Forward:** Look directly at the camera.
    - **Neutral Expression:** Keep your face relaxed, without smiling or frowning.
    - **Good Lighting:** Use even lighting with no strong shadows on your face.
    - **Clear Forehead:** Pull your hair back so your hairline and eyebrows are visible.
    - **Remove Glasses:** Eyeglasses can obscure key facial landmarks.
    - **Full Face Visible:** Ensure your entire face is in the frame.
    """)

# --- Core Logic for Analysis ---
def analyze_facial_proportions(image):
    """
    Analyzes facial landmarks to calculate key ratios and scores based on the Golden Ratio.
    """
    GOLDEN_RATIO = 1.618
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if not results.multi_face_landmarks:
        return None, None, None, None, None

    landmarks = results.multi_face_landmarks[0].landmark
    h, w = image.shape[:2]

    def get_coord(idx):
        return int(landmarks[idx].x * w), int(landmarks[idx].y * h)

    # Define all necessary landmark points for the desired ratios
    points = {
        'hairline': get_coord(10),
        'chin': get_coord(152),
        'left_cheek': get_coord(234),
        'right_cheek': get_coord(454),
        'nose_bottom': get_coord(2),
        'lip_center_top': get_coord(13),
        'lip_center_bottom': get_coord(14),
        'mouth_left': get_coord(61),
        'mouth_right': get_coord(291),
        'left_nostril': get_coord(278),
        'right_nostril': get_coord(48),
    }

    # Calculate the 3 key ratios
    ratios = {}
    try:
        # 1. Face Length / Face Width
        face_length = math.dist(points['hairline'], points['chin'])
        face_width = math.dist(points['left_cheek'], points['right_cheek'])
        ratios['Face Length / Width'] = face_length / face_width

        # 2. Lips-Chin / Nose-Lips
        lip_center = ((points['lip_center_top'][0] + points['lip_center_bottom'][0]) // 2,
                      (points['lip_center_top'][1] + points['lip_center_bottom'][1]) // 2)
        nose_to_lips = math.dist(points['nose_bottom'], lip_center)
        lips_to_chin = math.dist(lip_center, points['chin'])
        ratios['Lips-Chin / Nose-Lips'] = lips_to_chin / nose_to_lips

        # 3. Mouth Width / Nose Width
        mouth_width = math.dist(points['mouth_left'], points['mouth_right'])
        nose_width = math.dist(points['left_nostril'], points['right_nostril'])
        ratios['Mouth Width / Nose Width'] = mouth_width / nose_width
    except (ZeroDivisionError, KeyError):
        return None, None, None, None, None

    # Calculate scores for each ratio based on proximity to GOLDEN_RATIO
    scores = {}
    for name, value in ratios.items():
        deviation = abs(value - GOLDEN_RATIO)
        score = max(0, 100 * (1 - deviation / GOLDEN_RATIO))
        scores[name] = score

    # Calculate the overall score and overall ratio
    overall_score = np.mean(list(scores.values()))
    overall_ratio = np.mean(list(ratios.values())) # NEW: Average of the ratios

    # Annotate the image
    annotated_image = image.copy()
    for key, pt in points.items():
        if key in ['hairline', 'chin', 'left_cheek', 'right_cheek']:
             cv2.circle(annotated_image, pt, 5, (0, 255, 0), -1)

    cv2.line(annotated_image, points['hairline'], points['chin'], (255, 0, 0), 2)
    cv2.line(annotated_image, points['left_cheek'], points['right_cheek'], (0, 0, 255), 2)

    return ratios, scores, overall_score, overall_ratio, annotated_image


# --- Image Input Logic ---
image_np = None
if option == "Upload an Image":
    uploaded = st.file_uploader(
        "Upload a clear front-facing photo",
        type=['jpg', 'jpeg', 'png'],
        label_visibility="collapsed"
    )
    if uploaded:
        image = Image.open(uploaded).convert('RGB')
        image_np = np.array(image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

elif option == "Use Webcam":
    img_file_buffer = st.camera_input("Take a picture", label_visibility="collapsed")
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer).convert('RGB')
        image_np = np.array(image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)


# --- Process and Display Results ---
if image_np is not None:
    with st.spinner("Analyzing facial features..."):
        time.sleep(1)

        ratios, scores, overall_score, overall_ratio, output_image = analyze_facial_proportions(image_np)

        if ratios:
            display_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
            st.image(display_image, caption="Facial Landmarks Analysis", use_container_width=True)

            with st.container():
                st.markdown("## 📊 Analysis Results")

                # --- NEW: Overall Score and Ratio Section using st.metric ---
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Overall Beauty Score", value=f"{overall_score:.2f}%")
                with col2:
                    st.metric(
                        label="Average Facial Ratio",
                        value=f"{overall_ratio:.3f}",
                        delta=f"{overall_ratio - GOLDEN_RATIO:.3f} from ideal",
                        delta_color="inverse"
                    )

                # Detailed Breakdown Section
                with st.expander("Show Detailed Ratio Breakdown", expanded=True):
                    for (name, ratio_val), score_val in zip(ratios.items(), scores.values()):
                        st.markdown(f"**{name}**: `{ratio_val:.3f}` (Score: `{score_val:.2f}%`)")
                    st.info(f"The ideal Golden Ratio is `{GOLDEN_RATIO}`. The score is based on proximity to this number.")

            # Fun Facts
            with st.expander("💡 Did You Know?"):
                st.markdown("""
                - The golden ratio (1.618) appears throughout nature and art.
                - Many famous artworks like the Mona Lisa use golden ratio proportions.
                - While interesting, facial symmetry and proportions are just one aspect of beauty.
                - Cultural perceptions of beauty vary widely across the world.
                """)

        else:
            st.error("""
            **No face detected.** Please try again with:
            - A clear, front-facing photo
            - Good, even lighting
            - No obstructions (e.g., glasses, hair covering the forehead)
            """)
            display_error_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            st.image(display_error_image, caption="Uploaded Image", use_column_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>Note: This tool is just for fun. Remember, real beauty shines from the soul — every face tells a unique and beautiful story. ❤️</p>
    <p>Created with ❤️ By Ikram Shaik</p>
</div>
""", unsafe_allow_html=True)