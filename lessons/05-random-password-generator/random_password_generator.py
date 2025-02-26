# Random Password Generator

import random

# 1) Mini test function
def test_generate_password():
    """
    This function tests if the generated password has the correct length.
    """
    test_password = generate_password(10, True, "!@#$%^&*", True)
    if len(test_password) == 10:
        print("Test passed: The generated password has the correct length.")
    else:
        print("Test failed: The password length is incorrect.")

# 2) Function to generate the password
def generate_password(length, include_numbers, custom_special_chars, include_uppercase):
    """
    generate_password Algorithm:
    1. Start with a base set of lowercase letters.
    2. If numbers are included, add digits to the set.
    3. If special chars are included, add user-provided special symbols to the set.
    4. If uppercase letters are included, add uppercase letters to the set.
    5. Loop 'length' times, each time randomly pick one character from the set.
    6. Return the final string as the password.
    """

    # Base set: lowercase letters
    characters = "abcdefghijklmnopqrstuvwxyz"

    # If the user wants numbers, append digits
    if include_numbers:
        characters += "0123456789"

    # Use the user-provided special characters if given
    if custom_special_chars.strip():
        characters += custom_special_chars

    # If the user wants uppercase letters, append them
    if include_uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Ensure at least one character from each selected category is included
    password = []
    if include_numbers:
        password.append(random.choice("0123456789"))
    if custom_special_chars.strip():
        password.append(random.choice(custom_special_chars))
    if include_uppercase:
        password.append(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    password.append(random.choice("abcdefghijklmnopqrstuvwxyz"))

    # Fill the rest of the password length with random characters
    while len(password) < length:
      password.append(random.choice(characters))

    # Shuffle the password to ensure randomness
    random.shuffle(password)

    return "".join(password)

# 3) Function to measure password strength
def measure_password_strength(pwd, used_numbers, used_special, used_upper):
    """
    Measures the strength of a password based on its length and character types.
    """
    score = len(pwd)
    if used_numbers:
        score += 2
    if used_special:
        score += 3
    if used_upper:
        score += 2

    if score < 10:
        "Weak"
    elif score < 16:
        "Medium"
    else:
        return "Strong"

# 4) Main part of the program
def main():
    """
    This is where we:
    - Ask the user for the password length.
    - Ask whether to include numbers, special chars, uppercase letters.
    - Generate and print the random password.
    - Measure password strength.
    - Store generated passwords for reuse.
    - Handle input errors.
    """

    print("Welcome to the Random Password Generator!")
    generated_passwords = []

    while True:
        try:
            # Prompt for length
            length_input = input("Enter the password length (>= 6), or type 'done' to exit: ")
            if length_input.lower() == "done":
                break

            length = int(length_input)

            # Enforce minimum password length
            if length < 6:
               ("Password length is too short! Please enter at least 6.")
               continue

            # Prompt for including different character types
            include_numbers_input = input("Include numbers? (yes/no): ").lower()
            include_special_input = input("Include special characters? (yes/no): ").lower()
            include_uppercase_input = input("Include uppercase letters? (yes/no): ").lower()

            # Convert these yes/no answers to booleans
            include_numbers = (include_numbers_input == "yes")
            include_uppercase = (include_uppercase_input == "yes")

            # Ask for custom special characters if needed
            custom_special_chars = ""
            if include_special_input == "yes":
                custom_special_chars = input("Enter the special characters you want to include (e.g., !@#$%^&*): ")

            # Generate the password
            new_password = generate_password(length, include_numbers, custom_special_chars, include_uppercase)

            # Print the password
            print("Your random password is:", new_password)

            # Measure and display password strength
            strength = measure_password_strength(new_password, include_numbers, bool(custom_special_chars.strip()), include_uppercase)
            print("Password strength:", strength)

            # Save to a list
            generated_passwords.append(new_password)

            # Run our mini test function
            test_generate_password()

        except ValueError:
            # If the user typed something that's not an integer
            print("Invalid input for password length, please enter an integer.")

    # Print all passwords from this session
    if generated_passwords:
        print("\nHere are all the passwords you generated this session:")
        for pwd in generated_passwords:
            print("-", pwd)

    print("Thanks for using the Random Password Generator!")

# 5) Run the main program
if __name__ == "__main__":
    main()