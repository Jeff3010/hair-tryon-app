# Quick Qwen API Setup for Other Projects

## Essential Information

### API Key
```
sk-f4e51b7452dc4d3ca3e8a8d48bfd4884
```

### Basic Setup Code
```python
import dashscope
from dashscope import MultiModalConversation

# Configure Qwen API
dashscope.api_key = "sk-f4e51b7452dc4d3ca3e8a8d48bfd4884"
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
```

### Installation
```bash
pip install dashscope>=1.25.0
```

## Model Usage Examples

### Vision Analysis (qwen-vl-max)
```python
response = MultiModalConversation.call(
    model="qwen-vl-max",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Describe this image in detail"},
                {"image": "path/to/image.jpg"}
            ]
        }
    ]
)
```

### Image Generation/Editing (qwen-image-edit-plus-2025-10-30)
```python
response = MultiModalConversation.call(
    model="qwen-image-edit-plus-2025-10-30",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Edit this image according to instructions"},
                {"image": "input_image.jpg"}
            ]
        }
    ]
)
```

### Error Handling Template
```python
try:
    response = MultiModalConversation.call(...)
    
    if response.status_code == 200:
        # Success - process response.output
        print("Success:", response.output)
    else:
        # API error
        print("Error:", response)
        
except Exception as e:
    # Connection/library error
    print("Exception:", str(e))
```

---
**Copy this setup for quick integration into any project using Qwen AI models.**

**Developed by StammConnect**