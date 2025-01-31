import cv2
from pyzbar import pyzbar
import pandas as pd
import os

# Initialize webcam
cap = cv2.VideoCapture(0)

# List to store unique barcode data
barcode_data_list = []

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Decode barcodes in the frame
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            if barcode_data not in barcode_data_list:
                barcode_data_list.append(barcode_data)
                print(f"Barcode Detected: {barcode_data}")

        # Display the frame
        cv2.imshow("Barcode Scanner", frame)

        # Listen for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Save barcode data to Excel
    if barcode_data_list:
        try:
            df = pd.DataFrame({"Barcodes": barcode_data_list})
            excel_path = "data.xlsx"
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"Barcode data saved to '{os.path.abspath(excel_path)}'")
        except Exception as e:
            print(f"Failed to save Excel file: {e}")

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("Resources released. Goodbye!")