def controller(x):
    print("\n🤖 What do you want to do?")
    print("[1] Summary")
    print("[2] Timeline summary")
    print("[3] Ask a question")
    choice = input("Choose 1 / 2 / 3: ")
    return {"mode": {"1": "summary", "2": "timeline", "3": "qa"}.get(choice, "summary")}