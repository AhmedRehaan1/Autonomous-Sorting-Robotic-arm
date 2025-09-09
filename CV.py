import cv2
from pyfirmata import Arduino, util
import time

# Set up the Arduino
board = Arduino('COM11')  # Replace 'COM11' with your Arduino port
base_motor = board.get_pin('d:9:s')      # Base motor (pin 9)
shoulder_motor = board.get_pin('d:10:s') # Shoulder motor (pin 10)
elbow_motor = board.get_pin('d:11:s')    # Elbow motor (pin 11)
ldr_pin = board.get_pin('a:0:i')         # LDR analog input (pin A0)
led_pin = board.get_pin('d:4:o')         # LED output (pin 4)

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to access the camera")
    board.exit()
    exit()

# Define the color range for red and blue in HSV color space
lower_red1 = (0, 120, 70)
upper_red1 = (10, 255, 255)
lower_red2 = (170, 120, 70)
upper_red2 = (180, 255, 255)

lower_blue = (100, 150, 0)
upper_blue = (140, 255, 255)

# Threshold for LDR sensor (adjust based on testing)
LDR_THRESHOLD = 0.5

# Function to control servo motor
def move_servo(servo, position, motor_name):
    position = max(0, min(position, 180))  # Ensure the position is within 0-180
    servo.write(position)
    print(f"{motor_name} moved to position {position}")
    time.sleep(0.5)  # Adjusted delay for quicker response

# Initialize servo positions
base_motor.write(0)
shoulder_motor.write(60)
elbow_motor.write(0)




print("Base motor set to 0 degrees.")
print("Shoulder motor set to 30 degrees.")
print("Elbow motor set to 0 degrees.")

# Start the iterator for analog input
it = util.Iterator(board)
it.start()
ldr_pin.enable_reporting()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Keep the elbow motor at 0 degrees
        elbow_motor.write(0)

        # Read the analog value of the LDR sensor
        ldr_value = ldr_pin.read()

        if ldr_value is None:
            continue  # Skip if the value is not yet available

        print(f"LDR Value: {ldr_value:.2f}")

        # Control LED based on LDR value
        if ldr_value > LDR_THRESHOLD:  # If light intensity is low
            led_pin.write(1)  # Turn ON the LED
            print("Low light detected: LED is ON")
        else:  # If light intensity is high
            led_pin.write(0)  # Turn OFF the LED
            print("Bright light detected: LED is OFF")

        # Convert the frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create masks for red and blue colors
        mask_red1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        # Count non-zero pixels in the masks
        red_pixels = cv2.countNonZero(mask_red)
        blue_pixels = cv2.countNonZero(mask_blue)

        # Check for red detection
        if red_pixels > 500:  # Threshold for red detection
            print("Red detected: Moving base and shoulder motors")
            base_position = 90
            #shoulder_position 
            move_servo(base_motor, base_position, "Base Motor")
           # move_servo(shoulder_motor, shoulder_position, "Shoulder Motor")

        # Check for blue detection
        if blue_pixels > 500:  # Threshold for blue detection
            print("Blue detected: Moving base and shoulder motors")
            base_position = 140
            #shoulder_position = 70
            move_servo(base_motor, base_position, "Base Motor")
           # move_servo(shoulder_motor, shoulder_position, "Shoulder Motor")

        # Display the original frame and the masks
        cv2.imshow('Frame', frame)
        cv2.imshow('Red Mask', mask_red)
        cv2.imshow('Blue Mask', mask_blue)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Release the resources
    cap.release()
    cv2.destroyAllWindows()
    led_pin.write(0)  # Turn off the LED
    base_motor.write(0)  # Reset base motor to 0
    shoulder_motor.write(30)  # Reset shoulder motor to 30
    elbow_motor.write(0)  # Ensure elbow motor stays at 0
    board.exit()