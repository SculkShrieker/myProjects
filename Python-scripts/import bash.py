import os

def list_programs():
    return ["bash", "gnome-text-edit", "firefox", "nautilus"]

def main():
    programs = list_programs()
    print("Select programs to stop:\n")
    for i, prog in enumerate(programs, 1):
        print(f"{i}. {prog}")
    print("0. Exit without stopping any programs")  # 👈 Exit option

    choices = input("\nEnter numbers (comma-separated, e.g., 1,3): ").strip()
    if choices in ["", "0"]:
        print("Exiting... No programs stopped.")
        return  # 👈 Gracefully cancel
    

    try:
        selected = [programs[int(i)-1] for i in choices.split(",") if i.strip().isdigit() and int(i) in range(1, len(programs)+1)]
        if not selected:
            print("No valid selections made. Exiting.")
            return
        for prog in selected:
            print(f"Stopping {prog}...")
            os.system(f"pkill -9 {prog}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
