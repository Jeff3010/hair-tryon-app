import streamlit as st
from PIL import Image
import os
from datetime import datetime
from styling_advisor import HairStylingAdvisor, STYLE_CATEGORIES

st.set_page_config(
    page_title="Sentra Salon AI - Styling Advisor",
    page_icon="💇",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .recommendation-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("💇 Sentra Salon AI - Professional Hair Styling Advisor")
st.markdown("Get personalized hair styling recommendations powered by AI! Upload your photo and receive expert advice.")

# Initialize session state
if 'consultations' not in st.session_state:
    st.session_state.consultations = []

# Create directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize advisor
@st.cache_resource
def get_advisor():
    return HairStylingAdvisor()

advisor = get_advisor()

# Main layout
tab1, tab2, tab3, tab4 = st.tabs(["📸 Style Analysis", "🔄 Compare Styles", "💫 Full Consultation", "📚 Style Gallery"])

with tab1:
    st.header("Personal Style Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Upload Your Photo")
        user_image = st.file_uploader(
            "Choose a clear, front-facing photo",
            type=['png', 'jpg', 'jpeg'],
            key='analysis_photo'
        )
        
        user_image_path = None
        if user_image is not None:
            image = Image.open(user_image)
            st.image(image, caption="Your Photo", use_column_width=True)
            
            # Save image
            user_image_path = os.path.join(UPLOAD_DIR, f"user_{user_image.name}")
            with open(user_image_path, "wb") as f:
                f.write(user_image.getbuffer())
    
    with col2:
        st.subheader("Describe Your Desired Style")
        
        # Style category selection
        category = st.selectbox(
            "Style Category:",
            [""] + list(STYLE_CATEGORIES.keys())
        )
        
        if category:
            style = st.selectbox(
                "Select Style:",
                STYLE_CATEGORIES[category]
            )
        else:
            style = st.text_input(
                "Or describe your desired style:",
                placeholder="e.g., Short layered bob with side-swept bangs"
            )
        
        # Preferences
        st.subheader("Your Preferences")
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            maintenance = st.select_slider(
                "Maintenance Level:",
                ["Low", "Medium", "High"]
            )
            
            color_open = st.checkbox("Open to color changes")
        
        with col2_2:
            occasion = st.selectbox(
                "Primary Use:",
                ["Everyday", "Professional", "Special Events", "Versatile"]
            )
            
            length_change = st.checkbox("Willing to change length significantly")
        
        if st.button("🔍 Analyze Style Compatibility", disabled=not (user_image_path and style)):
            with st.spinner("Analyzing your features and style compatibility..."):
                preferences = {
                    "maintenance": maintenance,
                    "color_open": color_open,
                    "occasion": occasion,
                    "length_change": length_change
                }
                
                result = advisor.analyze_face_and_recommend(
                    user_image_path,
                    style,
                    preferences
                )
                
                if result["status"] == "success":
                    st.success("✅ Analysis Complete!")
                    
                    # Display analysis in a nice format
                    st.markdown("### 📊 Your Personalized Style Analysis")
                    st.markdown(result["analysis"])
                    
                    # Save to history
                    st.session_state.consultations.append({
                        "type": "analysis",
                        "style": style,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "result": result["analysis"]
                    })
                else:
                    st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")

with tab2:
    st.header("Compare Multiple Styles")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Upload Your Photo")
        compare_image = st.file_uploader(
            "Choose a clear photo",
            type=['png', 'jpg', 'jpeg'],
            key='compare_photo'
        )
        
        compare_image_path = None
        if compare_image is not None:
            image = Image.open(compare_image)
            st.image(image, caption="Your Photo", use_column_width=True)
            
            # Save image
            compare_image_path = os.path.join(UPLOAD_DIR, f"compare_{compare_image.name}")
            with open(compare_image_path, "wb") as f:
                f.write(compare_image.getbuffer())
    
    with col2:
        st.subheader("Select Styles to Compare")
        
        # Multi-select for styles
        selected_styles = []
        
        for i in range(1, 5):
            style_option = st.text_input(
                f"Style Option {i}:",
                key=f"style_{i}",
                placeholder=f"Enter style {i} (e.g., Pixie Cut)"
            )
            if style_option:
                selected_styles.append(style_option)
        
        st.info(f"📝 {len(selected_styles)} styles selected for comparison")
        
        if st.button("🔄 Compare Styles", disabled=not (compare_image_path and len(selected_styles) >= 2)):
            with st.spinner("Comparing styles for your features..."):
                result = advisor.compare_styles(compare_image_path, selected_styles)
                
                if result["status"] == "success":
                    st.success("✅ Comparison Complete!")
                    
                    st.markdown("### 📊 Style Comparison Results")
                    st.markdown(result["comparison"])
                    
                    # Save to history
                    st.session_state.consultations.append({
                        "type": "comparison",
                        "styles": selected_styles,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "result": result["comparison"]
                    })
                else:
                    st.error(f"Comparison failed: {result.get('error', 'Unknown error')}")

with tab3:
    st.header("Complete Virtual Consultation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Upload Your Photo")
        consult_image = st.file_uploader(
            "Choose your best photo",
            type=['png', 'jpg', 'jpeg'],
            key='consult_photo'
        )
        
        consult_image_path = None
        if consult_image is not None:
            image = Image.open(consult_image)
            st.image(image, caption="Your Photo", use_column_width=True)
            
            # Save image
            consult_image_path = os.path.join(UPLOAD_DIR, f"consult_{consult_image.name}")
            with open(consult_image_path, "wb") as f:
                f.write(consult_image.getbuffer())
    
    with col2:
        st.subheader("Consultation Type")
        
        consultation_type = st.radio(
            "What kind of consultation would you like?",
            [
                ("General Styling Advice", "general"),
                ("Complete Makeover Ideas", "makeover"),
                ("Professional/Office Looks", "professional"),
                ("Special Event Styling", "special_event")
            ],
            format_func=lambda x: x[0]
        )
        
        st.markdown(f"**Selected:** {consultation_type[0]}")
        
        consultation_descriptions = {
            "general": "Get comprehensive advice on styles, colors, and maintenance",
            "makeover": "Explore dramatic changes and trending styles",
            "professional": "Find polished, office-appropriate styles",
            "special_event": "Discover elegant styles for weddings and events"
        }
        
        st.info(consultation_descriptions[consultation_type[1]])
        
        if st.button("💫 Start Virtual Consultation", disabled=not consult_image_path):
            with st.spinner("Your virtual consultation is being prepared..."):
                result = advisor.virtual_consultation(
                    consult_image_path,
                    consultation_type[1]
                )
                
                if result["status"] == "success":
                    st.success("✅ Your Virtual Consultation is Ready!")
                    
                    st.markdown(f"### 💇 {consultation_type[0]}")
                    st.markdown(result["consultation"])
                    
                    # Option to download consultation
                    consultation_text = f"""
SENTRA SALON AI - VIRTUAL CONSULTATION REPORT
=============================================
Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Type: {consultation_type[0]}

{result["consultation"]}

---
Generated by Sentra Salon AI
Professional Hair Styling Advisor
                    """
                    
                    st.download_button(
                        "📥 Download Consultation Report",
                        consultation_text,
                        f"consultation_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                    
                    # Save to history
                    st.session_state.consultations.append({
                        "type": "consultation",
                        "consultation_type": consultation_type[0],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "result": result["consultation"]
                    })
                else:
                    st.error(f"Consultation failed: {result.get('error', 'Unknown error')}")

with tab4:
    st.header("Style Gallery & Inspiration")
    
    # Display style categories
    for category, styles in STYLE_CATEGORIES.items():
        st.subheader(f"💇 {category} Styles")
        
        cols = st.columns(5)
        for idx, style in enumerate(styles):
            with cols[idx % 5]:
                st.markdown(f"**{style}**")
        
        st.divider()
    
    # Consultation History
    if st.session_state.consultations:
        st.header("📜 Your Consultation History")
        
        for consultation in reversed(st.session_state.consultations[-5:]):
            with st.expander(f"{consultation['type'].title()} - {consultation['timestamp']}"):
                if consultation['type'] == 'analysis':
                    st.markdown(f"**Style Analyzed:** {consultation.get('style', 'N/A')}")
                elif consultation['type'] == 'comparison':
                    st.markdown(f"**Styles Compared:** {', '.join(consultation.get('styles', []))}")
                else:
                    st.markdown(f"**Type:** {consultation.get('consultation_type', 'General')}")
                
                st.markdown("---")
                st.markdown(consultation['result'][:500] + "..." if len(consultation['result']) > 500 else consultation['result'])

# Sidebar
with st.sidebar:
    st.header("💇 How It Works")
    st.markdown("""
    ### Our AI Styling Advisor:
    
    1. **Analyzes Your Features**
       - Face shape detection
       - Skin tone analysis
       - Feature compatibility
    
    2. **Provides Recommendations**
       - Style compatibility scores
       - Professional modifications
       - Alternative suggestions
    
    3. **Offers Expert Advice**
       - Styling techniques
       - Product recommendations
       - Maintenance tips
    
    ### Benefits:
    ✅ No image generation required
    ✅ Professional consultation
    ✅ Personalized recommendations
    ✅ Multiple style comparisons
    ✅ Detailed styling guides
    
    ### Perfect For:
    - Pre-salon consultations
    - Style exploration
    - Makeover planning
    - Professional guidance
    """)
    
    st.divider()
    
    st.info("""
    💡 **Pro Tip:** Save your consultation reports to show your hairstylist exactly what you're looking for!
    """)
    
    st.caption("Powered by Google AI")
    st.caption("© 2024 Sentra Salon AI")