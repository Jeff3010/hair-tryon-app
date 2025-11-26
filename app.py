import streamlit as st
from PIL import Image
import io
import os
from datetime import datetime
from nano_banana import NanoBanana
import base64

st.set_page_config(
    page_title="Virtual Hair Try-On",
    page_icon="💇",
    layout="wide"
)

st.title("🎨 Virtual Hair Try-On")
st.markdown("Upload your photo and a reference hairstyle to see how you'd look with a new hairstyle!")

# Initialize session state
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = []

# Create temporary directory for uploads
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Nano Banana client
@st.cache_resource
def get_nano_banana_client():
    return NanoBanana()

client = get_nano_banana_client()

# Create two columns for image upload
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Your Photo")
    user_image = st.file_uploader(
        "Upload your photo",
        type=['png', 'jpg', 'jpeg'],
        key='user_photo'
    )
    
    if user_image is not None:
        # Display uploaded image
        image = Image.open(user_image)
        st.image(image, caption="Your Photo", use_column_width=True)
        
        # Save uploaded image temporarily
        user_image_path = os.path.join(UPLOAD_DIR, f"user_{user_image.name}")
        with open(user_image_path, "wb") as f:
            f.write(user_image.getbuffer())

with col2:
    st.subheader("💇 Reference Hairstyle")
    hairstyle_image = st.file_uploader(
        "Upload reference hairstyle",
        type=['png', 'jpg', 'jpeg'],
        key='hairstyle_photo'
    )
    
    if hairstyle_image is not None:
        # Display uploaded image
        image = Image.open(hairstyle_image)
        st.image(image, caption="Reference Hairstyle", use_column_width=True)
        
        # Save uploaded image temporarily
        hairstyle_image_path = os.path.join(UPLOAD_DIR, f"hairstyle_{hairstyle_image.name}")
        with open(hairstyle_image_path, "wb") as f:
            f.write(hairstyle_image.getbuffer())

# Advanced options
with st.expander("⚙️ Advanced Options"):
    custom_prompt = st.text_area(
        "Custom Prompt (Optional)",
        placeholder="Leave empty to use optimized default prompt for best results",
        help="Provide specific instructions if needed. The default prompt is optimized for preserving facial features."
    )
    
    preserve_color = st.checkbox(
        "Try to preserve original hair color",
        value=False,
        help="When checked, attempts to keep your original hair color while changing only the style"
    )

# Process button
if st.button("🎨 Apply Hairstyle", type="primary", disabled=(user_image is None or hairstyle_image is None)):
    if user_image is not None and hairstyle_image is not None:
        with st.spinner("🔄 Processing your new look... This may take 30-60 seconds"):
            try:
                # Prepare custom prompt if needed
                final_prompt = None
                if custom_prompt:
                    final_prompt = custom_prompt
                elif preserve_color:
                    final_prompt = """
                    Transfer ONLY the hairstyle shape, texture, and styling from the reference image to the user.
                    PRESERVE the user's original hair color completely.
                    MAINTAIN all facial features, skin tone, and identity exactly as in the original.
                    The output should look photorealistic with natural integration.
                    """
                
                # Call Nano Banana API
                result = client.hair_transfer(
                    user_image_path=user_image_path,
                    hairstyle_image_path=hairstyle_image_path,
                    prompt_override=final_prompt
                )
                
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    # Generate output filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(OUTPUT_DIR, f"hair_tryon_{timestamp}.png")
                    
                    # Save the result
                    if client.save_result_image(result, output_path):
                        # Display result
                        st.success("✅ Hair try-on complete!")
                        
                        # Show before and after
                        st.subheader("Before & After")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.image(user_image_path, caption="Original", use_column_width=True)
                        
                        with col2:
                            result_image = Image.open(output_path)
                            st.image(result_image, caption="With New Hairstyle", use_column_width=True)
                            
                            # Download button
                            with open(output_path, "rb") as file:
                                btn = st.download_button(
                                    label="📥 Download Result",
                                    data=file,
                                    file_name=f"hair_tryon_{timestamp}.png",
                                    mime="image/png"
                                )
                        
                        # Add to history
                        st.session_state.processed_images.append({
                            'timestamp': timestamp,
                            'output_path': output_path
                        })
                    else:
                        st.error("❌ Failed to process the image. Please try again.")
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Display history
if st.session_state.processed_images:
    st.divider()
    st.subheader("📜 Recent Try-Ons")
    
    cols = st.columns(4)
    for idx, img_data in enumerate(reversed(st.session_state.processed_images[-8:])):
        with cols[idx % 4]:
            if os.path.exists(img_data['output_path']):
                st.image(img_data['output_path'], use_column_width=True)
                st.caption(f"Created: {img_data['timestamp']}")

# Instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. **Upload Your Photo**: Choose a clear front-facing photo
    2. **Upload Reference Hairstyle**: Select the hairstyle you want to try
    3. **Click Apply**: Wait for the AI to process your new look
    4. **Download**: Save your favorite results
    
    ### 💡 Tips for Best Results:
    - Use high-quality, well-lit photos
    - Front-facing photos work best
    - Clear hairstyle reference images give better results
    - The AI preserves your facial features while changing only the hair
    
    ### 🎯 Features:
    - Preserves your exact facial features
    - Adapts hairstyle naturally to your head shape
    - Maintains photo realism
    - Quick processing with Gemini 2.5 Flash
    """)
    
    st.divider()
    st.caption("Powered by Nano Banana API & Gemini 2.5 Flash Image Model")