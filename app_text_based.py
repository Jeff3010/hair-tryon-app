import streamlit as st
from PIL import Image
import os
from datetime import datetime
from text_based_transform import TextBasedHairTransform, HAIRSTYLE_TEMPLATES

st.set_page_config(
    page_title="Sentra Salon AI - Text-Based Hair Styling",
    page_icon="💇",
    layout="wide"
)

st.title("💇 Sentra Salon AI - Hair Styling Consultation")
st.markdown("Describe the hairstyle you want, and see how it would look on you!")

# Initialize session state
if 'transformed_images' not in st.session_state:
    st.session_state.transformed_images = []

# Create directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize AI client
@st.cache_resource
def get_ai_client():
    return TextBasedHairTransform()

client = get_ai_client()

# Main layout
col1, col2 = st.columns([1, 2])

user_image_path = None

with col1:
    st.subheader("📸 Your Photo")
    user_image = st.file_uploader(
        "Upload your photo",
        type=['png', 'jpg', 'jpeg'],
        key='user_photo',
        help="Upload a clear, front-facing photo for best results"
    )
    
    if user_image is not None:
        image = Image.open(user_image)
        st.image(image, caption="Your Photo", use_column_width=True)
        
        # Save uploaded image
        user_image_path = os.path.join(UPLOAD_DIR, f"user_{user_image.name}")
        with open(user_image_path, "wb") as f:
            f.write(user_image.getbuffer())

with col2:
    st.subheader("💇 Describe Your Desired Hairstyle")
    
    # Option 1: Select from templates
    st.markdown("**Option 1: Choose from popular styles**")
    selected_template = st.selectbox(
        "Select a hairstyle template:",
        ["Custom Description"] + list(HAIRSTYLE_TEMPLATES.keys())
    )
    
    if selected_template != "Custom Description":
        template_description = HAIRSTYLE_TEMPLATES[selected_template]
        st.info(f"📝 {template_description}")
    
    # Option 2: Custom description
    st.markdown("**Option 2: Describe your ideal hairstyle**")
    
    if selected_template == "Custom Description":
        hairstyle_description = st.text_area(
            "Describe the hairstyle you want:",
            placeholder="Example: Short layered bob with side-swept bangs, blonde highlights, professional look suitable for office",
            height=100
        )
    else:
        hairstyle_description = st.text_area(
            "Add custom details or modifications:",
            value=HAIRSTYLE_TEMPLATES[selected_template],
            height=100
        )
    
    # Additional details
    st.markdown("**Additional Preferences**")
    col2_1, col2_2 = st.columns(2)
    
    with col2_1:
        hair_length = st.select_slider(
            "Hair Length:",
            options=["Very Short", "Short", "Medium", "Long", "Very Long"],
            value="Medium"
        )
        
        hair_color = st.selectbox(
            "Hair Color Preference:",
            ["Keep Natural", "Black", "Brown", "Blonde", "Red", "Gray/Silver", "Highlights", "Ombre", "Balayage"]
        )
    
    with col2_2:
        hair_texture = st.selectbox(
            "Hair Texture:",
            ["Natural", "Straight", "Wavy", "Curly", "Coily", "Kinky"]
        )
        
        styling_occasion = st.selectbox(
            "Styling For:",
            ["Everyday", "Professional/Office", "Formal Event", "Casual", "Wedding", "Photo Shoot"]
        )

# Advanced options
with st.expander("⚙️ Advanced Styling Options"):
    face_shape = st.selectbox(
        "Face Shape (helps with styling recommendations):",
        ["Auto-detect", "Oval", "Round", "Square", "Heart", "Diamond", "Oblong"]
    )
    
    maintenance = st.radio(
        "Maintenance Preference:",
        ["Low maintenance", "Moderate maintenance", "High maintenance styling OK"]
    )
    
    age_appropriate = st.checkbox(
        "Suggest age-appropriate adaptations",
        value=True
    )

# Generate button
if st.button("🎨 Generate Hair Visualization", type="primary", disabled=(user_image is None or not hairstyle_description)):
    if user_image_path and hairstyle_description:
        with st.spinner("🔄 Creating your personalized hair visualization..."):
            try:
                # Build comprehensive description
                full_description = hairstyle_description
                
                # Add additional details
                additional_details = []
                
                if hair_length != "Medium":
                    additional_details.append(f"Hair length: {hair_length}")
                
                if hair_color != "Keep Natural":
                    additional_details.append(f"Hair color: {hair_color}")
                
                if hair_texture != "Natural":
                    additional_details.append(f"Hair texture: {hair_texture}")
                
                if styling_occasion != "Everyday":
                    additional_details.append(f"Styled for: {styling_occasion}")
                
                if face_shape != "Auto-detect":
                    additional_details.append(f"Optimized for {face_shape} face shape")
                
                additional_details.append(f"Maintenance level: {maintenance}")
                
                additional_details_str = ". ".join(additional_details)
                
                # Generate the visualization
                result = client.generate_with_text_description(
                    user_image_path=user_image_path,
                    hairstyle_description=full_description,
                    additional_details=additional_details_str
                )
                
                if result["status"] == "success" and result.get("generated_image"):
                    # Save the generated image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(OUTPUT_DIR, f"styled_{timestamp}.png")
                    
                    if client.save_generated_image(result, output_path):
                        st.success("✅ Hair visualization complete!")
                        
                        # Display results
                        st.subheader("Your Styling Visualization")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.image(user_image_path, caption="Original", use_column_width=True)
                        
                        with col2:
                            st.image(output_path, caption="Your New Style! 🎉", use_column_width=True)
                        
                        # Styling details
                        st.divider()
                        st.subheader("Styling Details")
                        st.markdown(f"**Requested Style:** {hairstyle_description}")
                        if additional_details:
                            st.markdown(f"**Additional Specifications:** {additional_details_str}")
                        
                        # Download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="📥 Download Your Styling Visualization",
                                data=file,
                                file_name=f"hair_style_{timestamp}.png",
                                mime="image/png"
                            )
                        
                        # Add to history
                        st.session_state.transformed_images.append({
                            'timestamp': timestamp,
                            'output_path': output_path,
                            'description': hairstyle_description[:50] + "..."
                        })
                    else:
                        st.error("Failed to save the visualization")
                        
                elif result.get("text_response"):
                    st.warning("⚠️ The AI provided styling advice instead of an image:")
                    st.info(result["text_response"])
                    
                    # Provide alternative approach
                    st.markdown("### 💡 Try These Tips:")
                    st.markdown("""
                    - Use more general descriptions (avoid specific person references)
                    - Focus on style attributes (length, texture, shape)
                    - Try selecting from the template options
                    - Describe the style as for a "salon mannequin" or "style guide"
                    """)
                else:
                    st.error(f"Visualization failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display history
if st.session_state.transformed_images:
    st.divider()
    st.subheader("📜 Recent Styles")
    
    cols = st.columns(4)
    for idx, img_data in enumerate(reversed(st.session_state.transformed_images[-8:])):
        with cols[idx % 4]:
            if os.path.exists(img_data['output_path']):
                st.image(img_data['output_path'], use_column_width=True)
                st.caption(f"{img_data['description']}")

# Sidebar
with st.sidebar:
    st.header("💇 Salon Styling Guide")
    st.markdown("""
    ### How to Describe Your Style:
    
    **Be Specific About:**
    - Length (pixie, bob, shoulder, long)
    - Texture (straight, wavy, curly)
    - Layers (heavy, light, none)
    - Bangs (side-swept, straight, none)
    - Color (if desired)
    
    **Example Descriptions:**
    - "Shoulder-length bob with subtle layers and side-swept bangs"
    - "Short pixie cut with textured top and tapered sides"
    - "Long beachy waves with face-framing layers"
    - "Professional medium-length style with soft waves"
    
    ### Pro Tips:
    - Describe styles, not specific people
    - Focus on technical hair terms
    - Mention your lifestyle needs
    - Consider maintenance requirements
    
    ### Popular Requests:
    - Classic Bob
    - Modern Pixie
    - Beach Waves
    - Professional Layers
    - Natural Curls
    """)
    
    st.divider()
    st.caption("Powered by Google AI")
    st.caption("Sentra Salon AI System")