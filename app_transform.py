import streamlit as st
from PIL import Image
import io
import os
from datetime import datetime
from hair_transform import HairTransformAI
import base64

st.set_page_config(
    page_title="AI Hair Try-On - Image Generation",
    page_icon="💇",
    layout="wide"
)

st.title("💇 Sentra Salon AI - Professional Hair Styling Consultation")
st.markdown("Professional hair styling visualization tool for salon consultations. Help customers visualize their new hairstyle before committing!")

# Initialize session state
if 'transformed_images' not in st.session_state:
    st.session_state.transformed_images = []

# Create temporary directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize AI client
@st.cache_resource
def get_ai_client():
    return HairTransformAI()

client = get_ai_client()

# Create two columns for image upload
col1, col2 = st.columns(2)

user_image_path = None
hairstyle_image_path = None

with col1:
    st.subheader("📸 Your Photo")
    user_image = st.file_uploader(
        "Upload your photo (front-facing works best)",
        type=['png', 'jpg', 'jpeg'],
        key='user_photo'
    )
    
    if user_image is not None:
        # Display uploaded image
        image = Image.open(user_image)
        st.image(image, caption="Your Photo", use_column_width=True)
        
        # Save uploaded image
        user_image_path = os.path.join(UPLOAD_DIR, f"user_{user_image.name}")
        with open(user_image_path, "wb") as f:
            f.write(user_image.getbuffer())

with col2:
    st.subheader("💇 Reference Hairstyle")
    hairstyle_image = st.file_uploader(
        "Upload the hairstyle you want to try",
        type=['png', 'jpg', 'jpeg'],
        key='hairstyle_photo'
    )
    
    if hairstyle_image is not None:
        # Display uploaded image
        image = Image.open(hairstyle_image)
        st.image(image, caption="Reference Hairstyle", use_column_width=True)
        
        # Save uploaded image
        hairstyle_image_path = os.path.join(UPLOAD_DIR, f"hairstyle_{hairstyle_image.name}")
        with open(hairstyle_image_path, "wb") as f:
            f.write(hairstyle_image.getbuffer())

# Advanced options
with st.expander("⚙️ Advanced Options"):
    generation_style = st.selectbox(
        "Generation Style",
        ["Photorealistic", "Natural Blend", "Exact Match", "Artistic"]
    )
    
    preserve_color = st.checkbox(
        "Try to preserve my original hair color",
        value=False,
        help="Attempts to keep your natural hair color while changing only the style"
    )
    
    enhance_quality = st.checkbox(
        "Enhance output quality",
        value=True,
        help="Apply additional processing for higher quality results"
    )

# Generate button
if st.button("🎨 Generate My New Look", type="primary", disabled=(user_image is None or hairstyle_image is None)):
    if user_image_path and hairstyle_image_path:
        with st.spinner("🔄 AI is creating your new hairstyle... This may take 15-30 seconds"):
            try:
                # Customize prompt based on options
                custom_prompt = None
                
                if generation_style == "Natural Blend":
                    custom_prompt = """
                    Professional salon consultation: Create a natural styling visualization showing how this hairstyle 
                    would look on the customer. This is for professional beauty consultation to help the customer 
                    decide on their new style. Adapt the hairstyle naturally to their features.
                    """
                elif generation_style == "Exact Match":
                    custom_prompt = """
                    Professional salon consultation: Show exactly how this specific hairstyle from our style catalog 
                    would appear on the customer. This visualization helps them make an informed styling decision 
                    at our salon. Maintain their natural features while demonstrating the exact style.
                    """
                elif generation_style == "Artistic":
                    custom_prompt = """
                    Professional salon consultation: Create a creative styling interpretation showing an artistic 
                    version of how this hairstyle could be adapted for the customer. This helps explore creative 
                    styling options for their salon appointment.
                    """
                
                if preserve_color:
                    base_prompt = custom_prompt or ""
                    custom_prompt = f"{base_prompt}\nIMPORTANT: Keep the original hair color from the first image, only change the style and shape."
                
                if enhance_quality:
                    base_prompt = custom_prompt or ""
                    custom_prompt = f"{base_prompt}\nGenerate in highest quality with perfect details, professional photography standard."
                
                # Call the AI transformation
                result = client.hair_transfer(
                    user_image_path=user_image_path,
                    hairstyle_image_path=hairstyle_image_path,
                    prompt_override=custom_prompt
                )
                
                if result["status"] == "success" and result.get("generated_image"):
                    # Save the generated image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(OUTPUT_DIR, f"transformed_{timestamp}.png")
                    
                    if client.save_generated_image(result, output_path):
                        st.success("✅ Transformation complete!")
                        
                        # Display results
                        st.subheader("Your New Look")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.image(user_image_path, caption="Original", use_column_width=True)
                        
                        with col2:
                            st.image(hairstyle_image_path, caption="Reference Style", use_column_width=True)
                        
                        with col3:
                            st.image(output_path, caption="Your New Look! 🎉", use_column_width=True)
                        
                        # Larger view of the result
                        st.divider()
                        st.subheader("Detailed View")
                        st.image(output_path, caption="Your transformed look - Ready to save!", use_column_width=False, width=500)
                        
                        # Download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="📥 Download Your New Look",
                                data=file,
                                file_name=f"my_new_hairstyle_{timestamp}.png",
                                mime="image/png"
                            )
                        
                        # Add to history
                        st.session_state.transformed_images.append({
                            'timestamp': timestamp,
                            'output_path': output_path,
                            'style': generation_style
                        })
                    else:
                        st.error("❌ Failed to save the generated image")
                        
                elif result["status"] == "text_only":
                    st.warning("⚠️ " + result.get("message", "Image generation not available"))
                    if result.get("text_response"):
                        st.info("AI Response: " + result["text_response"][:500])
                else:
                    error_msg = result.get("error", "Unknown error occurred")
                    st.error(f"❌ Transformation failed: {error_msg}")
                    
                    # Provide helpful guidance
                    if "safety" in error_msg.lower():
                        st.info("💡 Tip: Try using different photos that are clear and appropriate")
                    elif "quota" in error_msg.lower():
                        st.warning("API quota might be exceeded. Please try again later.")
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please ensure your photos are clear and try again.")

# Display history
if st.session_state.transformed_images:
    st.divider()
    st.subheader("📜 Your Transformations")
    
    cols = st.columns(4)
    for idx, img_data in enumerate(reversed(st.session_state.transformed_images[-8:])):
        with cols[idx % 4]:
            if os.path.exists(img_data['output_path']):
                st.image(img_data['output_path'], use_column_width=True)
                st.caption(f"{img_data['style']} - {img_data['timestamp']}")

# Sidebar with instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    ### Steps:
    1. **Upload Your Photo** - A clear, front-facing photo
    2. **Upload Hairstyle Reference** - The style you want to try
    3. **Adjust Settings** (Optional) - Choose generation style
    4. **Click Generate** - AI creates your new look
    5. **Download** - Save your transformed image
    
    ### 💡 Best Practices:
    - Use high-quality, well-lit photos
    - Front-facing portraits work best
    - Clear hairstyle references give better results
    - The AI preserves your facial features perfectly
    
    ### 🎯 Generation Styles:
    - **Photorealistic**: Most natural looking results
    - **Natural Blend**: Adapts color to suit you
    - **Exact Match**: Copies hairstyle precisely
    - **Artistic**: Creative interpretation
    
    ### ⚡ Features:
    - Real image generation (not just analysis)
    - Preserves your exact facial features
    - Multiple style options
    - High-quality output
    """)
    
    st.divider()
    st.caption("Powered by Google Gemini 2.0 Flash Image Generation")
    st.caption("Project: Sentra Salon AI")