import csv
import os
from datetime import datetime

# -----------------------------------------
# INDUCTION MOTOR PREDICTIVE MAINTENANCE
# -----------------------------------------

CSV_FILE = "motor_readings.csv"

# Example thresholds only.
# Adjust them according to your motor specifications.
TEMP_LIMIT = 75.0          # Temperature in °C
VIBRATION_LIMIT = 4.5      # Vibration in mm/s
CURRENT_LIMIT = 10.0       # Current in amperes


def predict_motor_condition(temperature, vibration, current):
    warnings = []

    # Check motor temperature
    if temperature >= TEMP_LIMIT:
        warnings.append("High motor temperature")

    # Check motor vibration
    if vibration >= VIBRATION_LIMIT:
        warnings.append("Excessive motor vibration")

    # Check motor current
    if current >= CURRENT_LIMIT:
        warnings.append("High motor current")

    # Estimate condition based on threshold violations
    if len(warnings) >= 2:
        condition = "HIGH RISK"
    elif len(warnings) == 1:
        condition = "WARNING"
    else:
        condition = "NORMAL"

    return condition, warnings


def save_reading(temperature, vibration, current,
                 condition, warnings):

    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date and Time",
                "Temperature (C)",
                "Vibration (mm/s)",
                "Current (A)",
                "Estimated Condition",
                "Warnings"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            temperature,
            vibration,
            current,
            condition,
            "; ".join(warnings) if warnings else "None"
        ])


def main():
    print("=" * 48)
    print(" INDUCTION MOTOR PREDICTIVE MAINTENANCE ")
    print("=" * 48)

    while True:
        try:
            print("\nEnter motor sensor readings:")

            temperature = float(
                input("Temperature (°C): ")
            )

            vibration = float(
                input("Vibration (mm/s): ")
            )

            current = float(
                input("Current (A): ")
            )

            # Validate input
            if temperature < 0 or vibration < 0 or current < 0:
                print("Error: Readings cannot be negative.")
                continue

            # Estimate motor condition
            condition, warnings = predict_motor_condition(
                temperature, vibration, current
            )

            # Display results
            print("\n========== RESULTS ==========")
            print(f"Temperature : {temperature:.2f} °C")
            print(f"Vibration   : {vibration:.2f} mm/s")
            print(f"Current     : {current:.2f} A")
            print(f"Condition   : {condition}")

            if warnings:
                print("\nPossible issues:")
                for warning in warnings:
                    print(f"- {warning}")
            else:
                print("No configured thresholds exceeded.")

            # Save readings to CSV
            save_reading(
                temperature,
                vibration,
                current,
                condition,
                warnings
            )

            print(f"\nReadings saved to {CSV_FILE}")

            choice = input(
                "\nCheck another reading? (y/n): "
            ).strip().lower()

            if choice != "y":
                print("\nMonitoring session completed.")
                break

        except ValueError:
            print("Invalid input. Please enter numeric values.")

        except OSError as error:
            print(f"File error: {error}")


if __name__ == "__main__":
    main()