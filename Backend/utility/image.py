from PIL import Image
import io
import base64

def resize_image_base64(base64_string):
    # separate html and image
    img1 = base64_string.split(",")[1]
    width = 200
    height = 200
    # Decode base64 string to image bytes
    image_bytes = base64.b64decode(img1)
    
    # Open image from bytes
    image = Image.open(io.BytesIO(image_bytes))

    if(image.size[0] < width or image.size[1] < height):
      width = min(width, height)
      height = min(width, height)
    
    # Resize and crop image
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image_width, image_height = image.size
    left = (image_width - width) / 2
    top = (image_height - height) / 2
    right = (image_width + width) / 2
    bottom = (image_height + height) / 2
    image = image.crop((left, top, right, bottom))

    # Convert image to base64 string
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Combine html and image
    img_str = f"data:image/jpeg;base64,{img_str}"

    return img_str
