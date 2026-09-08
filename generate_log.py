from datetime import datetime

def generate_log():
    """
    Generates a daily log file named log_YYYYMMDD.txt 
    containing predefined system actions.
    """
    log_data = ["User logged in", "User updated profile", "Report exported"]
    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"

    with open(filename, "w") as file:
        for entry in log_data:
            file.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filename

if __name__ == "__main__":
    generate_log()