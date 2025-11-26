import streamlit as st
from PIL import Image
import io
import os
from datetime import datetime
from qwen_ai_client import QwenHairTransfer

st.set_page_config(
    page_title="Virtual Hair Try-On - Qwen AI",
    page_icon="💇",
    layout="wide"
)

# Custom CSS for dark theme and better UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .upload-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }
    
    .stFileUploader > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 2rem !important;
    }
    
    .stFileUploader > div > div > div > div {
        color: #ffffff !important;
    }
    
    .uploadedFile {
        display: none !important;
    }
    
    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    h1 {
        color: #ffffff !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
    }
    
    .main-subtitle {
        color: #b8b8b8 !important;
        text-align: center !important;
        font-size: 1.2rem !important;
        margin-bottom: 2rem !important;
    }
    
    .stImage {
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Hide unwanted file uploader elements */
    .stFileUploader > div > div > button {
        display: none !important;
    }
    
    .stFileUploader > div > div > div > small {
        display: none !important;
    }
    
    .stFileUploader > div > div > div > svg {
        display: none !important;
    }
    
    /* Hide the green plus and tick marks */
    .uploadedFile > div > div:first-child {
        display: none !important;
    }
    
    .uploadedFileName {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 5px !important;
        padding: 0.5rem !important;
    }
    
    /* Improve sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.2) !important;
    }
    
    .sidebar .element-container {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Custom upload area styling */
    .stFileUploader > div {
        border: none !important;
        background: none !important;
    }
    
    .stFileUploader > div > div {
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: rgba(255, 255, 255, 0.4) !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Virtual Hair Try-On with Qwen AI")
st.markdown('<p class="main-subtitle">Upload your photo and describe your dream hairstyle to generate a realistic transformation!</p>', unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

# Create temporary directory for uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Qwen AI client
@st.cache_resource
def get_qwen_client():
    return QwenHairTransfer()

client = get_qwen_client()

# Upload section with custom styling
st.markdown('<div class="upload-section">', unsafe_allow_html=True)

# Create wider columns for better layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📸 Your Photo")
    user_image = st.file_uploader(
        "Drag and drop your photo here or click to browse",
        type=['png', 'jpg', 'jpeg'],
        key='user_photo',
        help="Upload a clear front-facing photo for best results"
    )
    
    if user_image is not None:
        # Display uploaded image
        image = Image.open(user_image)
        st.image(image, caption="✅ Your Photo Uploaded", use_column_width=True)
        
        # Save uploaded image temporarily
        user_image_path = os.path.join(UPLOAD_DIR, f"user_{user_image.name}")
        with open(user_image_path, "wb") as f:
            f.write(user_image.getbuffer())
    else:
        user_image_path = None
        # Show placeholder when no image
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 2px dashed rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 3rem;
            text-align: center;
            color: #888;
            margin-top: 1rem;
        ">
            <p>👤 No photo uploaded yet</p>
            <small>Upload your photo to get started</small>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 💇 Reference Hairstyle (Optional)")
    hairstyle_image = st.file_uploader(
        "Upload a reference image for inspiration (optional)",
        type=['png', 'jpg', 'jpeg'],
        key='hairstyle_photo',
        help="Optional: Upload a reference hairstyle for visual inspiration"
    )
    
    if hairstyle_image is not None:
        # Display uploaded image
        image = Image.open(hairstyle_image)
        st.image(image, caption="✅ Reference Uploaded", use_column_width=True)
        
        # Save uploaded image temporarily
        hairstyle_image_path = os.path.join(UPLOAD_DIR, f"hairstyle_{hairstyle_image.name}")
        with open(hairstyle_image_path, "wb") as f:
            f.write(hairstyle_image.getbuffer())
    else:
        hairstyle_image_path = None
        # Show placeholder when no image
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 2px dashed rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 3rem;
            text-align: center;
            color: #888;
            margin-top: 1rem;
        ">
            <p>💡 Optional Reference</p>
            <small>You can upload a hairstyle for inspiration, or just describe it below</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Hair transformation description
st.markdown("### ✍️ Describe Your Hair Transformation (Optional if reference image uploaded)")
hair_description = st.text_area(
    "Describe the hairstyle you want (optional with reference image):",
    placeholder="Example: Give me a bob cut with bangs, shoulder-length wavy hair, or short pixie cut with layers... Leave empty to use reference image only.",
    help="Optional: Describe the specific hairstyle. If you upload a reference image, you can leave this empty.",
    height=100
)

# Advanced options
with st.expander("⚙️ Advanced Options"):
    generation_style = st.radio(
        "Generation Style",
        ["Natural Hair Transfer", "Creative Style Fusion", "Color Adaptation"]
    )
    
    custom_prompt = st.text_area(
        "Custom Instructions (Optional)",
        placeholder="Add any specific requirements for the hair transformation",
        help="Provide specific instructions for the hair style transfer"
    )

# Process button - requires user image and either description OR reference image
button_disabled = (user_image is None) or (not hair_description.strip() and hairstyle_image is None)
if st.button("✨ Generate Hair Transformation", type="primary", disabled=button_disabled):
    if user_image is not None and user_image_path is not None and (hair_description.strip() or hairstyle_image is not None):
        with st.spinner("🔄 Generating hair transformation images..."):
            try:
                # Create comprehensive prompt - handle case with no text description
                if hair_description.strip():
                    base_prompt = f"Transform this person's hairstyle to: {hair_description}"
                else:
                    base_prompt = "Transform this person's hairstyle"
                
                if generation_style == "Creative Style Fusion":
                    style_instruction = "Adapt the hairstyle creatively to suit their face shape and features. Make it unique while keeping their identity intact."
                elif generation_style == "Color Adaptation":
                    style_instruction = "Adapt the hair color to complement their skin tone for the most flattering result."
                else:
                    style_instruction = "Apply the transformation naturally and realistically."
                
                # Only add style instruction if we have a text description
                if hair_description.strip():
                    full_prompt = f"{base_prompt}. {style_instruction}"
                else:
                    full_prompt = None  # Let the API handle default prompting for reference images
                
                if custom_prompt:
                    if full_prompt:
                        full_prompt += f" Additional requirements: {custom_prompt}"
                    else:
                        full_prompt = custom_prompt
                
                if full_prompt and not hairstyle_image_path:
                    full_prompt += " Keep all facial features, skin tone, clothing, and background exactly the same. Only change the hair."
                
                # Call Qwen AI with text-based transformation
                result = client.hair_transfer(
                    user_image_path=user_image_path,
                    hairstyle_image_path=hairstyle_image_path,  # Pass the optional reference
                    prompt_override=full_prompt
                )
                
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    # Display results
                    st.success("✅ Hair transformation complete!")
                    
                    if result.get("status") == "success" and "generated_images" in result:
                        # Display generated images
                        st.subheader("🎨 Your New Hair Transformations")
                        
                        generated_images = result.get("generated_images", [])
                        
                        if generated_images:
                            # Display the generated image
                            for i, img_path in enumerate(generated_images):
                                try:
                                    transformed_img = Image.open(img_path)
                                    st.image(transformed_img, 
                                           caption="✨ Your Hair Transformation", 
                                           use_column_width=True)
                                    
                                    # Center the download button
                                    col1, col2, col3 = st.columns([1, 2, 1])
                                    with col2:
                                        with open(img_path, "rb") as file:
                                            st.download_button(
                                                label="📥 Download Your Transformation",
                                                data=file.read(),
                                                file_name="hair_transformation.png",
                                                mime="image/png",
                                                key=f"download_{i}",
                                                use_container_width=True
                                            )
                                except Exception as e:
                                    st.error(f"Error displaying transformation: {str(e)}")
                        
                        # Add to history
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.analysis_results.append({
                            'timestamp': timestamp,
                            'description': result.get("description", "Hair transformation generated"),
                            'generated_images': generated_images,
                            'type': generation_style
                        })
                        
                        st.info(f"💡 {result.get('description', 'Images generated successfully')}")
                        
                    else:
                        st.warning("⚠️ Transformation completed but no images were generated")
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Note: Make sure you have installed the required libraries: pip install openai pillow streamlit")

# Display history
if st.session_state.analysis_results:
    st.divider()
    st.subheader("📜 Recent Transformations")
    
    for analysis in reversed(st.session_state.analysis_results[-5:]):
        with st.expander(f"{analysis['type']} - {analysis['timestamp']}"):
            if 'generated_images' in analysis and analysis['generated_images']:
                # Display thumbnail images from history
                cols = st.columns(len(analysis['generated_images']))
                for i, img_path in enumerate(analysis['generated_images']):
                    if os.path.exists(img_path):
                        with cols[i]:
                            img = Image.open(img_path)
                            st.image(img, caption=f"Result {i+1}", use_column_width=True)
            else:
                st.markdown(analysis.get('description', 'No description available')[:300] + "...")

# Instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. **Upload Your Photo**: Choose a clear front-facing photo
    2. **Upload Reference Hairstyle** (Optional): Select the exact hairstyle you want
    3. **Describe Hairstyle** (Optional if reference uploaded): Text description
    4. **Click Generate**: Get AI-powered hair transformations
    
    ### 💡 How Hair Transfer Works:
    - **With Reference Image**: The AI copies the exact hairstyle from your reference image onto your face
    - **With Text Only**: The AI creates a hairstyle based on your description
    - **Both**: Combines reference image with text refinements
    - Preserves your facial features, skin tone, and background
    
    ### 🎯 Best Results:
    - Use clear, front-facing photos
    - Reference images with visible, distinct hairstyles work best
    - The AI will transfer hair color, length, texture, and style from reference
    
    ### ⚠️ Hair Transfer Technology:
    Uses Qwen AI Image Edit Plus with optimized prompts for precise hairstyle transfer.
    The AI understands which image is the person and which is the target hairstyle.
    """)
    
    st.divider()
    st.caption("Powered by Qwen AI Image Edit Plus Model")