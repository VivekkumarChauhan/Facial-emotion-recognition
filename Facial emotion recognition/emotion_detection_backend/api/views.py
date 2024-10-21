from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from keras.models import load_model
from PIL import Image
import numpy as np
import logging

model = load_model('D:\\Vs code\\Python\\Facial emotion recognition\\save\\emotion_detection_model.h5')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the pre-trained model
model = load_model('D:\\Vs code\\Python\\Facial emotion recognition\\save\\emotion_detection_model.h5')

# Preprocess function for input images
def preprocess_image(image):
    img = image.convert('L')  # Convert to grayscale
    img = img.resize((48, 48))  # Resize to 48x48 pixels
    img = np.array(img) / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = np.expand_dims(img, axis=-1)  # Add channel dimension for grayscale
    return img

class EmotionDetectionView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            raise ValidationError('No image file provided.')
        
        file = request.FILES['image']
        try:
            image = Image.open(file)
        except Exception as e:
            logging.error(f'Error opening image: {str(e)}')
            raise ValidationError(f'Error opening image: {str(e)}')

        # Preprocess the image for model input
        processed_image = preprocess_image(image)

        # Make a prediction
        try:
            prediction = model.predict(processed_image)
        except Exception as e:
            logging.error(f'Error during prediction: {str(e)}')
            raise ValidationError(f'Error during prediction: {str(e)}')

        emotion_label = np.argmax(prediction)

        # Define emotion classes
        emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        detected_emotion = emotions[emotion_label]

        return Response({'emotion': detected_emotion})
