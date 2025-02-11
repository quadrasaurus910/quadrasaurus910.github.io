name = input("What is your name?\n")
if not name:
    print("Hello, world!")
else:
    name = name.strip().title()
    print(f"Hello, {name}!")