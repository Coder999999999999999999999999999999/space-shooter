import random
import os


image_path = 'image.png'

def play_game():
    print("Welcome to the 'Guess the Number' game!")
    print("I'm thinking of a number between 1 and 100. Can you guess it?")

    number_to_guess = random.randint(1, 100)
    attempts = 0
    
    while True:
        try:
            user_guess = int(input("Enter your guess: "))
            attempts += 1
            
            if user_guess < number_to_guess:
                print("Too low! Try again.")
            elif user_guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
              
                show_image()
                break
        except ValueError:
            print("Please enter a valid number.")

def show_image():
    try:
        os.system(f'open "{image_path}"')  
     
    except Exception as e:
        print(f"Error displaying the image: {e}")

# Start the game
if __name__ == "__main__":
    play_game()
