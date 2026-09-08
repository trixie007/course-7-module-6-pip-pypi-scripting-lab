from datetime import datetime

def generate_log(log_data=None):
    if log_data is None:
        log_data = ["User logged in", "User updated profile", "Report exported"]
    
    if not isinstance(log_data, list):
        raise ValueError("log_data must be a list")

    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"

    with open(filename, "w") as file:
        for entry in log_data:
            file.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filename

if __name__ == "__main__":
    generate_log()
    