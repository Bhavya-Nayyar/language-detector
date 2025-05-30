import cv2 as cv
from PIL import Image
import pytesseract
from langdetect import DetectorFactory
DetectorFactory.seed = 0
from langdetect import detect
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract OCR\tesseract.exe'

def rescale(frame, scale=0.70):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def blur(image):
    gaussian = cv.GaussianBlur(image, (3, 3), 3)
    return gaussian

def grayscaling(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray

def thresholding(image):
    adaptive_thresh = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 19, 11)
    return adaptive_thresh

def tesseract(image):
    custom_config = r'--oem 3 --psm 6 -l hin+eng+de+fr+es+it+zh-cn+pa+ru+sa+ta+ur'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return "Unknown Language"
    
def language_id(code):
    language_mapping = {
        "en": "English",
        "hi": "Hindi",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "it": "Italian",
        "zh-cn": "Chinese",
        "pa": "Punjabi",
        "ru": "Russian",
        "sa": "Sanskrit",
        "ta": "Tamil",
        "ur": "Urdu"
    }
    return language_mapping.get(code, "Unknown Language")

def process_webcam():
    capture = cv.VideoCapture(1)
    if not capture.isOpened():
        print("Error: Could not open webcam")
        return

    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    capture.set(cv.CAP_PROP_FPS, 30)

    frame_count = 0
    language_name = "Detecting..."

    while True:
        ret, frame = capture.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % 10 == 0:
            frame = rescale(frame)
            frame = grayscaling(frame)
            frame = blur(frame)
            frame = thresholding(frame)
            
            text = tesseract(frame)

            language_code = detect_language(text)

            language_name = language_id(language_code)

        cv.rectangle(frame, (5, 10), (630, 100), (0, 0, 0), -1)    

        cv.putText(frame, f'Detected Language: {language_name}', (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)

        cv.imshow('Webcam', frame)

        if cv.waitKey(1) & 0xFF == ord('e'):  
            break

    capture.release()
    cv.destroyAllWindows()

def process_image(image_path):
    img = cv.imread(image_path)

    if img is None:
        print("Error: Could not read image.")
        return

    img = rescale(img)
    img = grayscaling(img)
    img = blur(img)
    img = thresholding(img)

    text = tesseract(img)
    language_code = detect_language(text)
    language_name = language_id(language_code)

    with open("Image_Output.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Detected Language:", language_name)

def select_photo():
    image_path = filedialog.askopenfilename(title="Select an Image",
                                             filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if image_path:
        process_image(image_path)

def select_webcam():
    process_webcam()

def main():
    root = tk.Tk()
    root.title("Language Detector")
    root.geometry("300x200")
    
    photo_button = tk.Button(root, text="Photo", command=select_photo, font=("Arial", 14))
    photo_button.pack(pady=20)
    
    webcam_button = tk.Button(root, text="Webcam", command=select_webcam, font=("Arial", 14))
    webcam_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()