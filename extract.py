import easyocr
import re
import os
import cv2
import numpy as np
import fitz  
import pymupdf 

reader = easyocr.Reader(['en'])

def preprocess_image(image_path):
    """ Preprocess the image to improve OCR accuracy """
    image = cv2.imread(image_path)
    image = cv2.resize(image, (0, 0), fx=1.5, fy=1.5)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    enhanced = cv2.convertScaleAbs(gray, alpha=1.3, beta=20)
    thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 21, 15)
    return thresh

def extract_text(image_path):
    """ Extracts text from image or PDF using OCR """
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return ""
    
    if image_path.lower().endswith(".pdf"):
        doc = fitz.open(image_path)
        text = ""
        for page in doc:
            img = page.get_pixmap()
            img_array = np.frombuffer(img.samples, dtype=np.uint8).reshape((img.height, img.width, img.n))
            text += " ".join(reader.readtext(img_array, detail=0)) + "\n"
        return text.strip()
    
    image = preprocess_image(image_path)
    return " ".join(reader.readtext(image, detail=0))

def is_aadhaar(text):
    """Check if Aadhaar card is present based on pattern and keywords"""
    text_lower = text.lower()
    aadhaar_number_pattern = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
    keywords = ["aadhaar", "mera aadhaar", "meri pehchaan", "government of india", "unique identification authority of india"]
    return bool(aadhaar_number_pattern or any(k in text_lower for k in keywords))

# -------------------- Style B --------------------
# Developer B: concise, uses inline comments, camelCase
def isPAN(text):
    text = text.upper()
    return bool(re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)) or \
           "permanent account number" in text.lower() or \
           "income tax department" in text.lower()

def isPassport(text):
    return bool(re.search(r"\b[A-Z][0-9]{7}\b", text)) or "passport" in text.lower()

def detectDocType(text):  # shorter name style
    if is_aadhaar(text): return "Aadhaar Card"
    if isPAN(text): return "PAN Card"
    if isPassport(text): return "Passport"
    return "Unknown"

def handleUpload(expectedType):  # camelCase naming
    imagePath = input(f"\nUpload your {expectedType} (JPG, PNG, PDF): ").strip()
    text = extract_text(imagePath)

    if not text:
        print("No text detected or file missing.")
        return False

    # Debug info
    print("\n>>> Full OCR Text <<<")
    print(text)
    print(">>> ---------------- <<<\n")

    docType = detectDocType(text)
    print(f"Document Detected: {docType}")
    print(f"Sample Text: {text[:200]}...")

    if docType == expectedType:
        print(f"{expectedType} verified.\n")
        return True
    else:
        print(f"Incorrect file. Expected: {expectedType}, but got: {docType}\n")
        return False

# Main workflow (mixed style)
if __name__ == "__main__":
    docs = ["Aadhaar Card", "PAN Card", "Passport"]

    for doc in docs:
        while True:
            ok = handleUpload(doc)
            if ok:
                break
            print(f"Please re-upload a valid {doc}.")





































































        



     
     

