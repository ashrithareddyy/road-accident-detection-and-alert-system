import cv2
from detection import AccidentDetectionModel
import numpy as np
from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = 'Enter your sid'
AUTH_TOKEN = 'Enter your auth_token'
FROM_PHONE = 'enter virtual number '
TO_PHONE = 'enter phone number'

twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_alert(message):
    """Send an alert message via Twilio."""
    twilio_client.messages.create(
        body=message,
        from_=FROM_PHONE,
        to=TO_PHONE
    )

model = AccidentDetectionModel("model.json", 'model_weights.h5')
font = cv2.FONT_HERSHEY_SIMPLEX

def startapplication(video_path):
    """Start the application with the selected video path."""
    video = cv2.VideoCapture(video_path)  # Use the selected video path
    message_sent = False  # Flag to track if a message has been sent
    
    while True:
        ret, frame = video.read()
        if not ret:
            break  # Exit if no frame is returned

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        if pred == "Accident":
            prob = (round(prob[0][0] * 100, 2))
            # Send alert if the probability exceeds 100
            if prob >= 100 and not message_sent:
                message_sent = True  # Set flag to true
                alert_message = f"Accident detected with {prob}% probability."
                send_alert(alert_message)  # Send Twilio alert

            cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
            cv2.putText(frame, f"{pred} {prob}%", (20, 30), font, 1, (255, 255, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break  # Allow exiting the video display with 'q'

    video.release()
    cv2.destroyAllWindows()  # Ensure the OpenCV window is closed
