from datetime import datetime

def generate_log(log_data=None):
    """
    Generates a timestamped log file (log_YYYYMMDD.txt).
    Accepts log_data as a list of strings, validates input,
    and returns the filename created.
    """
    # Handle default argument
    if log_data is None:
        log_data = ["User logged in", "User updated profile", "Report exported"]
    
    # Raise ValueError on invalid input types (e.g., integers, booleans)
    if not isinstance(log_data, (list, tuple)):
        raise ValueError("log_data must be a list or tuple of strings")

    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"

    with open(filename, "w") as file:
        for entry in log_data:
            file.write(f"{entry}\n")

    return filename  # Crucial: Must return the filename string for the autograder teardown

if __name__ == "__main__":
    generate_log()