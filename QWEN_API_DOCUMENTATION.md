# Qwen AI API Integration Documentation

## Overview
This Hair Tryon application uses Qwen AI models through Alibaba Cloud's DashScope platform for advanced hair style transformation and analysis.

## API Access Details

### Base Configuration
- **Platform**: Alibaba Cloud DashScope
- **Base URL**: `https://dashscope-intl.aliyuncs.com/api/v1`
- **Authentication**: API Key based
- **Library**: `dashscope` Python SDK

### API Key Information
- **Current API Key**: `sk-f4e51b7452dc4d3ca3e8a8d48bfd4884`
- **Key Type**: DashScope API Key for international service
- **Usage**: This key provides access to Qwen models including vision and image editing capabilities

### Models Used

#### 1. Qwen Vision Model (qwen-vl-max)
**Purpose**: Hairstyle analysis and detailed description
**Capabilities**:
- Image analysis and understanding
- Detailed visual description generation
- Feature extraction and categorization

**Usage Example**:
```python
import dashscope
from dashscope import MultiModalConversation

dashscope.api_key = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

response = MultiModalConversation.call(
    model="qwen-vl-max",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Analyze this hairstyle in detail..."},
                {"image": "path/to/image.jpg"}
            ]
        }
    ]
)
```

#### 2. Qwen Image Edit Plus (qwen-image-edit-plus-2025-10-30)
**Purpose**: Hair transformation and image generation
**Capabilities**:
- Image editing and modification
- Style transfer and transformation
- Hair replacement and styling

**Usage Example**:
```python
response = MultiModalConversation.call(
    model="qwen-image-edit-plus-2025-10-30",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Transform this person's hair..."},
                {"image": "user_photo.jpg"},
                {"image": "reference_style.jpg"}
            ]
        }
    ]
)
```

## Implementation Architecture

### Hybrid AI Workflow
Our application implements a sophisticated dual-model approach:

1. **Analysis Phase** (qwen-vl-max):
   - Analyzes reference hairstyle image
   - Extracts detailed characteristics
   - Generates comprehensive description

2. **Transfer Phase** (qwen-image-edit-plus-2025-10-30):
   - Uses analysis results + visual references
   - Performs precise hair transformation
   - Generates realistic output images

### Code Structure

#### Main Client Class
```python
class QwenHairTransfer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("QWEN_API_KEY", "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884")
        dashscope.api_key = self.api_key
        dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
        self.model = "qwen-image-edit-plus-2025-10-30"
```

#### Key Methods
- `analyze_hairstyle()`: Vision-based hairstyle analysis
- `hair_transfer()`: Main hair transformation function
- `generate_transformation_guide()`: Result processing

## Setting Up for Different Projects

### 1. Installation
```bash
pip install dashscope>=1.25.0
```

### 2. Basic Setup
```python
import dashscope
from dashscope import MultiModalConversation

# Configure API access
dashscope.api_key = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
```

### 3. Environment Variables (Recommended)
Create a `.env` file:
```
QWEN_API_KEY=sk-f4e51b7452dc4d3ca3e8a8d48bfd4884
```

Load in your application:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("QWEN_API_KEY")
```

## API Response Structure

### Successful Response
```json
{
  "status_code": 200,
  "output": {
    "choices": [
      {
        "message": {
          "content": [
            {
              "text": "Analysis or response text",
              "image": "generated_image_url"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  }
}
```

### Error Response
```json
{
  "status_code": 400,
  "code": "InvalidParameter",
  "message": "Error description",
  "request_id": "unique_request_id"
}
```

## Best Practices

### 1. Error Handling
```python
try:
    response = MultiModalConversation.call(...)
    if response.status_code == 200:
        # Process successful response
        pass
    else:
        # Handle API errors
        print(f"API Error: {response}")
except Exception as e:
    # Handle connection/library errors
    print(f"Exception: {str(e)}")
```

### 2. Image Handling
- **Supported formats**: PNG, JPG, JPEG
- **File paths**: Use absolute paths for reliability
- **Image size**: Optimize for better performance
- **Multiple images**: Order matters for reference-based tasks

### 3. Prompt Engineering
- Be specific and detailed in instructions
- Use structured prompts for complex tasks
- Include clear role definitions for multiple images
- Provide step-by-step guidance for better results

## Rate Limits and Quotas

- Check DashScope documentation for current limits
- Implement retry logic for rate limit errors
- Monitor usage through DashScope console
- Consider caching for repeated requests

## Security Considerations

### API Key Management
- **Never commit API keys to version control**
- Use environment variables for production
- Rotate keys regularly
- Monitor usage for unauthorized access

### Data Privacy
- Images are processed on Alibaba Cloud servers
- Temporary files should be cleaned up
- Consider data residency requirements
- Review Alibaba Cloud privacy policies

## Troubleshooting

### Common Issues
1. **Authentication Errors**: Verify API key and base URL
2. **Model Not Found**: Ensure model name is correct
3. **Image Loading Errors**: Check file paths and formats
4. **Rate Limiting**: Implement exponential backoff
5. **Network Issues**: Add timeout and retry logic

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Alternative Projects Integration

For other projects wanting to use this API setup:

1. **Copy the API configuration**:
   ```python
   dashscope.api_key = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"
   dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
   ```

2. **Adapt the model calls** for your specific use case
3. **Modify prompts** to match your requirements
4. **Implement error handling** appropriate for your application

## Resources

- **DashScope Documentation**: https://help.aliyun.com/zh/dashscope/
- **Qwen Models**: https://qwenlm.github.io/
- **Python SDK**: https://pypi.org/project/dashscope/
- **API Reference**: https://dashscope.console.aliyun.com/

---

**Note**: This API key (`sk-f4e51b7452dc4d3ca3e8a8d48bfd4884`) is configured for the Hair Tryon project. For production use in different projects, consider obtaining separate API keys for better security and usage tracking.

**Developed by StammConnect**