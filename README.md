# Sorting Robot Arm

This project implements a sorting robot arm using an Arduino, servo motors, a webcam, and an LDR (Light Dependent Resistor) sensor. The robot arm is designed to detect and sort objects based on their color (red and blue) and also includes functionality to control an LED based on ambient light conditions.

## Features

*   **Color-based Sorting**: Detects red and blue objects using computer vision (OpenCV) and moves the robot arm to designated positions for sorting.
*   **Light Detection**: Utilizes an LDR sensor to detect ambient light levels and control an LED accordingly.
*   **Arduino Integration**: Communicates with an Arduino board via `pyfirmata` for precise control of servo motors and reading sensor data.
*   **Real-time Video Processing**: Processes video frames from a webcam in real-time for object detection.

## Hardware Requirements

*   Arduino Board (e.g., Arduino Uno)
*   3 Servo Motors (for base, shoulder, and elbow)
*   LDR (Light Dependent Resistor)
*   LED
*   Webcam
*   Connecting Wires
*   Breadboard (optional, for LDR and LED)

## Software Requirements

*   Python 3.x
*   `pyfirmata` library
*   `opencv-python` library

## Setup and Installation

1.  **Arduino Setup**:
    *   Upload the `StandardFirmata` sketch to your Arduino board using the Arduino IDE. This sketch is usually found under `File > Examples > Firmata > StandardFirmata`.
    *   Connect your Arduino to your computer via USB.

2.  **Hardware Connections**:
    *   **Base Motor**: Connect to Digital Pin 9 on Arduino.
    *   **Shoulder Motor**: Connect to Digital Pin 10 on Arduino.
    *   **Elbow Motor**: Connect to Digital Pin 11 on Arduino.
    *   **LDR Sensor**: Connect one leg to Analog Pin A0 and the other leg to GND through a 10k Ohm resistor. Connect the junction of the LDR and resistor to 5V.
    *   **LED**: Connect the anode (longer leg) to Digital Pin 4 (through a current-limiting resistor, e.g., 220 Ohm) and the cathode (shorter leg) to GND.

3.  **Python Environment Setup**:
    *   Ensure you have Python 3 installed.
    *   Install the required Python libraries using pip:

        ```bash
        pip install pyfirmata opencv-python
        ```

## Usage

1.  **Update Arduino Port**: Open the `CV.py` file and change the Arduino port to match your system. For example, on Windows it might be `COMx` (e.g., `COM11`), and on Linux/macOS it might be `/dev/ttyUSBx` or `/dev/tty.usbmodemxxxx`.

    ```python
    board = Arduino("COM11")  # Replace with your Arduino port
    ```

2.  **Adjust Thresholds (Optional)**:
    *   You may need to adjust the `LDR_THRESHOLD` value in `CV.py` based on your LDR sensor and lighting conditions.
    *   The `red_pixels > 500` and `blue_pixels > 500` thresholds for color detection might also need fine-tuning depending on your webcam and object size.

3.  **Run the Script**:

    ```bash
    python CV.py
    ```

    The script will:
    *   Initialize the robot arm to its starting positions.
    *   Open a webcam feed, displaying the original frame and masks for red and blue detection.
    *   Continuously read LDR sensor values and control the LED.
    *   Detect red and blue objects in the webcam feed and actuate the robot arm to sort them.

## Troubleshooting

*   **`Error: Unable to access the camera`**: Ensure your webcam is properly connected and not in use by another application. You might also need to check camera permissions.
*   **Arduino Connection Issues**: Verify the correct COM port is specified in `CV.py`. Ensure the `StandardFirmata` sketch is successfully uploaded to your Arduino.
*   **Servo Jitter/Incorrect Movement**: Check your servo connections and ensure they are receiving sufficient power. Calibrate servo positions if necessary.
*   **Color Detection Inaccuracy**: Adjust the HSV color ranges (`lower_red1`, `upper_red1`, etc.) and pixel thresholds (`red_pixels > 500`) in `CV.py` to match your specific lighting conditions and object colors.

## Future Enhancements

*   Implement more robust object tracking to prevent false positives.
*   Add support for detecting and sorting more colors.
*   Integrate inverse kinematics for more precise arm movements.
*   Develop a user interface for easier control and calibration.
*   Improve error handling and add more detailed logging.

## License

This project is open-source and available under the [MIT License](LICENSE).

