from fastapi import File, UploadFile, Request, FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import torch
from torch import nn, optim
from torchvision import transforms
from PIL import Image
import matplotlib.image as mpimg
from torchvision import datasets, models, transforms
import mlflow.pytorch


mlflow.set_tracking_uri("http://127.0.0.1:5000")
MODEL_PATH = "./mlruns/0/db5ea138df96488baf74d2164d466db8/artifacts/model"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def infer_image(model_path, image_path):
 
    model_vgg = mlflow.pytorch.load_model(model_path)
    model_vgg.eval() 
    
    class_names = ['LeafBlast', 'Healthy', 'Hispa', 'BrownSpot']
    transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    img = Image.open(image_path)
    img_tensor = transform(img).unsqueeze(0)

    # Move input tensor to GPU if available
    if torch.cuda.is_available():
        img_tensor = img_tensor.cuda()

    prediction = model_vgg(img_tensor)
    prediction = prediction.cpu().data.numpy().argmax()

    print('Detected: {}'.format(class_names[prediction]))
    return class_names[prediction]



@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        file_location = "./static/uploads/"+ file.filename
        with open("./static/uploads/"+ file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not upload image")

    finally:
        file.file.close()
    
    print(file_location)
    return {"image" : file.filename , "message" : "image Uploaded" }




@app.post("/classify")
async def classify(request: Request):
    body = await request.json()
    print('body', body)
    file_location = "./static/uploads/"+  body["image"]
    print('aaaa', file_location)
    image_class =  'Duck'
    image_class = infer_image(MODEL_PATH, file_location)
    return {"message" : "image classified successfully", "imageClass" : image_class }



@app.get("/")
def main(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)