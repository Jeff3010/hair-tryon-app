# Virtual Hair Try-On Application

A Streamlit-based application that allows users to virtually try on different hairstyles using AI-powered image processing through the Nano Banana API with Gemini 2.5 Flash Image model.

## Features

- Upload your photo and a reference hairstyle image
- AI-powered hairstyle transfer while preserving facial features
- High-quality photorealistic results
- Download processed images
- Recent try-on history
- Advanced options for customization

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

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

## API Configuration

The application uses the Nano Banana API with the following configuration:
- Model: `gemini-2.5-flash-image`
- API Key: Hardcoded in `nano_banana.py` (line 13)

## Advanced Features

- **Custom Prompts**: Override the default prompt for specific styling requirements
- **Preserve Original Hair Color**: Option to keep your hair color while changing only the style
- **Batch Processing**: View and download multiple try-on results

## Technical Details

The application uses an optimized prompt that:
- Preserves 100% of facial features and identity
- Transfers hairstyle shape, texture, and flow
- Ensures natural integration and photorealistic results
- Adapts hair color to look natural with skin tone