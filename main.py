# BMI Calculator in Python

def calculate_bmi(weight, height):
    """Calculate BMI given weight (kg) and height (m)."""
    return weight / (height ** 2)


def categorize_bmi(bmi):
    """Categorize BMI into health categories."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


def main():
    # Input from the user
    try:
        weight = float(input("Enter your weight in kilograms: "))
        height = float(input("Enter your height in meters: "))

        if weight <= 0 or height <= 0:
            print("Error: Weight and height must be positive values.")
            return

        # Calculate BMI
        bmi = calculate_bmi(weight, height)

        # Categorize BMI
        category = categorize_bmi(bmi)

        # Output result
        print(f"Your BMI is: {bmi:.2f}")
        print(f"Category: {category}")
    except ValueError:
        print("Error: Please enter valid numbers for weight and height.")


if __name__ == "__main__":
    main()
