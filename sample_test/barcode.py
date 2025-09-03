import cv2
from pyzxing import BarCodeReader

def scan_barcode(image_path):
    """
    Scans a barcode/QR code from an image, decodes it to string,
    and returns a clean list of results.
    """
    # --- Preprocess image for better detection ---
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Increase contrast
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Save temporary preprocessed image
    temp_path = "temp_processed.png"
    cv2.imwrite(temp_path, thresh)

    # --- Decode using pyzxing ---
    reader = BarCodeReader()
    results = reader.decode(temp_path)

    cleaned_results = []
    if results:
        for r in results:
            raw_data = r.get("parsed") or r.get("raw", "")
            # ✅ Decode if it's bytes
            if isinstance(raw_data, bytes):
                raw_data = raw_data.decode("utf-8")
            raw_data = raw_data.strip()
            # ✅ Optional: Validate ISBN format (10 or 13 digits only)
            if raw_data.isdigit() and len(raw_data) in (10, 13):
                cleaned_results.append(raw_data)
    #print(cleaned_results)
    return cleaned_results


