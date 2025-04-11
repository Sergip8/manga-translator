import base64
from io import BytesIO
import logging
from fastapi import FastAPI, File, UploadFile
from PIL import Image

from traslate_manga_image import MangaTranslator
from dotenv import load_dotenv
load_dotenv()  

logging.getLogger('torch').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)  

app = FastAPI()

@app.post("/translate")
async def translate(file: UploadFile = File(...)):
    image = Image.open(file.file)
    processed_image = MangaTranslator().translate_manga_page(image, "es")
    output_buffer = BytesIO()
    processed_image.save(output_buffer, format="JPEG")
    processed_image_bytes = output_buffer.getvalue()
    encoded_image = base64.b64encode(processed_image_bytes).decode('utf-8')
    return {"status": "ok", "image": encoded_image}