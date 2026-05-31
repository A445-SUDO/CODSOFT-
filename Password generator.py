import random
import string


def generate_password(length, use_uppercase, use_numbers, use_symbols):
    """Generates a random password based on user-specified constraints."""
    # Core character set: Always include lowercase letters for basic structure
    character_pool = string.ascii_lowercase

    # Optional character sets based on user complexity choice
    if use_uppercase:
        character_pool += string.ascii_uppercase
    if use_numbers:
        character_pool += string.digits
    if use_symbols:
        character_pool += string.punctuation

    # Ensure the pool is not empty (failsafe)
    if not character_pool:
        return "Error: No character types selected!"

    # Generate the password by randomly choosing characters from the pool
    password_list = [random.choice(character_pool) for _ in range(length)]

    # Shuffle the list to mix character distribution thoroughly
    random.shuffle(password_list)

    # Combine the list items into a final string
    return "".join(password_list)


def get_boolean_input(prompt):
    """Helper function to get valid yes/no configurations from the user."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ["y", "yes"]:
            return True
        if choice in ["n", "no"]:
            return False
        print(" Invalid input! Please enter 'y' for Yes or 'n' for No.")


def main():
    print("=" * 45)
    print("       SECURE PASSWORD GENERATOR       ")
    print("=" * 45)

    # Step 1: Securely fetch and validate password length
    while True:
        try:
            length = int(input(" Enter the desired password length: "))
            if length <= 0:
                print(" Length must be a positive number greater than 0.")
                continue
            if length < 6:
                print(" Warning: Passwords shorter than 6 characters are weak.")
            break
        except ValueError:
            print(" Invalid input! Please enter a valid whole number.")

    print("\n--- Configure Password Complexity ---")

    # Step 2: Fetch complexity rules
    use_uppercase = get_boolean_input("Include Uppercase letters? (y/n): ")
    use_numbers = get_boolean_input("Include Numbers? (y/n): ")
    use_symbols = get_boolean_input("Include Special Symbols? (y/n): ")

    # Fallback checklist handling: If user says no to everything
    if not (use_uppercase or use_numbers or use_symbols):
        print("\n You selected 'no' for all complexities.")
        print(" Defaulting to a lowercase alphanumeric setup for security...")
        use_numbers = True

    # Step 3: Run processing engine
    generated_password = generate_password(
        length, use_uppercase, use_numbers, use_symbols
    )

    # Step 4: Display Output
    print("\n" + "=" * 45)
    print(" YOUR GENERATED PASSWORD IS:")
    print(f"  {generated_password}")
    print("=" * 45)


if __name__ == "__main__":
    main()
