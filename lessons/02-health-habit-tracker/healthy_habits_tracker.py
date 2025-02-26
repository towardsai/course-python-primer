# Healthy Habits Tracker

# Define daily goals for each habit (dictionary)
daily_goals = {
    'water_intake': 8,      # cups of water
    'exercise_minutes': 30, # minutes
    'sleep_hours': 7        # hours
}

# Create a dictionary that will store lists of entries for each habit
habits_data = {
    'water_intake': [],
    'exercise_minutes': [],
    'sleep_hours': []
}

# We use a tuple for habit names (tuples can't be changed once created)
HABIT_NAMES = ('water_intake', 'exercise_minutes', 'sleep_hours')

while True:
    # Debugging statement to see that the loop starts each time
    print("\nDebug: Starting a new loop iteration.")

    habit_choice = input("Enter a habit to track (water_intake / exercise_minutes / sleep_hours), 'delete' to remove the last entry, \n 'reset' to clear all data, or 'done' to exit: ")

    if habit_choice == 'done':
        break
    elif habit_choice == 'reset':
        # Reset all data
        for habit in habits_data:
            habits_data[habit].clear()
        print("All habit data has been reset!")
    elif habit_choice in HABIT_NAMES:
        try:
            # Ask for the time period
            time_period = input("Is this entry for morning, afternoon, or evening? ").strip().lower()

            # Validate the time period
            if time_period not in ['morning', 'afternoon', 'evening']:
                print("Invalid time period. Please enter 'morning', 'afternoon', or 'evening'.")
                continue

            # Ask for the value or delete the last entry
            user_value_str = input(f"Enter the amount for {habit_choice} (or type 'delete' to remove the last entry): ").strip()

            if user_value_str.lower() == 'delete':
                if habits_data[habit_choice]:
                    removed_value = habits_data[habit_choice].pop()
                    print(f"Deleted the last entry: {removed_value}")
                else:
                    print(f"No entries to delete for {habit_choice}.")
            else:
                # Convert the input to a float
                user_value = float(user_value_str)

                # Validate inputs (e.g., sleep hours cannot exceed 24)
                if habit_choice == 'sleep_hours' and user_value > 24:
                    print("That can't be correct. Please enter a realistic value for sleep hours.")
                    continue

                # Append the time period and value as a tuple
                habits_data[habit_choice].append((time_period, user_value))

                # Provide feedback using control flow
                if user_value >= daily_goals[habit_choice]:
                    print(f"Great job! You've met or exceeded today's goal for {habit_choice}!")
                else:
                    print(f"Keep going, you're on your way to meeting your {habit_choice} goal!")
        except ValueError:
            print("Invalid input. Enter a valid number.")
    else:
        print("Unknown habit. Choose a valid option or type 'done'.")

# Print a summary of what was entered
print("\n--- Daily Summary ---")
for habit in HABIT_NAMES:
    entries = habits_data[habit]
    if entries:
        # Calculate total and average
        total_amount = sum(entry[1] for entry in entries)  # Sum the numeric values
        average_amount = total_amount / len(entries)
        print(f"{habit} - Total: {total_amount}, Average: {average_amount:.2f}")
        print(f"Entries: {entries}")
    else:
        print(f"No entries recorded for {habit}.")

print("Thank you for using the Healthy Habits Tracker!")