# 🎨 Virtual Hair Try-On Application

An advanced AI-powered hair transformation app using **Qwen Image Edit Plus** and **Qwen Vision** models for ultra-realistic hairstyle transfers.

## ✨ Features

- **Hybrid AI System**: Vision analysis + Image editing for maximum accuracy
- **Dual Input Modes**: Text description OR reference image OR both combined  
- **Real Image Generation**: Actual transformed photos, not just overlays
- **Dark Theme UI**: Modern glass-morphism design
- **Advanced Analysis**: 10+ hairstyle characteristics analyzed automatically
- **Download Results**: High-quality generated images
- **Multiple Styles**: Natural, Creative, and Color Adaptation modes

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the application**:
```bash
streamlit run app_vertex.py
```

3. **Open in browser**: `http://localhost:8501`

## Usage

1. **Upload Your Photo**: Select a clear, front-facing photo of yourself
2. **Upload Reference Hairstyle**: Choose a hairstyle image you want to try
3. **Click "Apply Hairstyle"**: The AI will process and generate your new look
4. **Download Results**: Save the images you like

## Tips for Best Results

- Use high-resolution, well-lit photos
- Front-facing angles work best
- Clear hairstyle reference images produce better results
- The system maintains your facial features while only changing the hairstyle

## Project Structure

```
Hair Tryon/
├── app.py              # Main Streamlit application
├── nano_banana.py      # Nano Banana API client implementation
├── requirements.txt    # Python dependencies
├── uploads/           # Temporary storage for uploaded images (created automatically)
└── outputs/           # Generated results (created automatically)
```

## 🤖 AI Technology

### Hybrid Dual-Model Architecture
1. **Qwen Vision (qwen-vl-max)**: Analyzes reference hairstyles in detail
2. **Qwen Image Edit Plus (qwen-image-edit-plus-2025-10-30)**: Performs hair transformations

### API Integration
- **Platform**: Alibaba Cloud DashScope
- **API Key**: `sk-f4e51b7452dc4d3ca3e8a8d48bfd4884`
- **Base URL**: `https://dashscope-intl.aliyuncs.com/api/v1`

📖 **Detailed API Documentation**: See `QWEN_API_DOCUMENTATION.md`  
⚡ **Quick Setup Guide**: See `QUICK_API_SETUP.md`

## 🎯 Advanced Features

- **Reference Image Analysis**: 10-point detailed hairstyle breakdown
- **Smart Fallback**: Handles analysis failures gracefully  
- **Multiple Input Modes**: Text + Image + Combined approaches
- **Generation Styles**: Natural, Creative, Color Adaptation
- **Dark Theme**: Modern UI with glass-morphism effects

## 🏗 Project Structure

```
Hair Tryon/
├── app_vertex.py              # Main Streamlit application  
├── qwen_ai_client.py          # Qwen API integration
├── requirements.txt           # Dependencies
├── QWEN_API_DOCUMENTATION.md  # Complete API docs
├── QUICK_API_SETUP.md         # Quick reference
├── uploads/                   # Temporary uploads
└── outputs/                   # Generated results
```

## 📚 Documentation

- **`QWEN_API_DOCUMENTATION.md`**: Complete API integration guide
- **`QUICK_API_SETUP.md`**: Quick copy-paste setup for other projects
- **API Key**: `sk-f4e51b7452dc4d3ca3e8a8d48bfd4884` (for reference/other projects)

---

**Developed by StammConnect**