def greet(name):
    """Greets the given name."""
    message = f"Hello, {name}!"
    for char in message:
        print(char, end='')
    print()

if __name__ == "__main__":
    greet("World")
    print("Welcome to AI Code Analyst!")

# A simple loop for demonstration
for i in range(3):
    print(f"Iteration {i+1}")