# Math Captcha Generator

## Introduction

This Python script generates a simple math captcha and prompts the user to solve it. It randomly generates two numbers and an arithmetic operator (+, -, *) to form an equation. The user needs to input the result of the equation to pass the captcha.

## How It Works

1. **Captcha Generation**:
   - Randomly selects two numbers between 0 and 10 and an arithmetic operator.
   - Forms an equation in the format: "num1 operator num2 = ?"
   - Evaluates the equation to calculate the result.

2. **Display Captcha**:
   - Uses the `ImageCaptcha` library to generate an image containing the captcha equation.
   - Displays the captcha image to the user.

3. **User Input**:
   - Prompts the user to input the result of the math equation.
   - Compares the user's input with the calculated result.
   - Prints a success message if the input matches the result, otherwise prompts the user to try again.

## Requirements

- Python 3.x
- `captcha` library (install via `pip install captcha`)

## How to Run

1. Ensure Python and the required libraries are installed.
2. Run the script using the command:
   ```
   python math_captcha_generator.py
   ```

## Example

Upon running the script, a math captcha image will be displayed, and the user will be prompted to enter the result of the equation. If the input matches the calculated result, a success message will be printed; otherwise, the user will be asked to try again.

## License

This project is licensed under the MIT License.

---

Feel free to contribute to this project by forking the repository and submitting pull requests. Your contributions are always welcome!
