# app.py

import socket
import tkinter as tk
from text_editor import create_text_editor_frame

def run_text_editor():
    # Create the main application window
    root = tk.Tk()
    root.title("Text Editor with Server Dropdown")
    
    # Create the text editor frame
    create_text_editor_frame(root)
    
    # Add a drop-down menu for displaying running servers
    server_dropdown = tk.StringVar(root)
    server_dropdown.set("No running servers")  # Default value
    dropdown_menu = tk.OptionMenu(root, server_dropdown, "No running servers")
    dropdown_menu.pack(padx=10, pady=(0, 10))
    
    # Function to update the drop-down menu with running servers
    def update_servers():
        servers = get_running_servers()
        if servers:
            server_dropdown.set(servers[0])
        else:
            server_dropdown.set("No running servers")
    
    def get_running_servers():
        # Returns a list of running servers
        servers = []
        try:
            # Try connecting to the server to check if it's running
            with socket.create_connection(('192.168.0.7', 65432), timeout=1):
                servers.append("192.168.0.7:65432")
        except (socket.timeout, ConnectionRefusedError):
            pass
        return servers
    
    update_servers()  # Initialize the drop-down menu

    # Add a Refresh button to update the server list
    refresh_button = tk.Button(root, text="Refresh Servers", command=update_servers)
    refresh_button.pack(pady=(0, 10))
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    run_text_editor()
