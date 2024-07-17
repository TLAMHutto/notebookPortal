# Server/app.py

import tkinter as tk
from tkinter import scrolledtext
from server import server_instance  # Ensure that server_instance is imported correctly

def start_server():
    server_instance.start_server()
    update_server_status()
    root.after(2000, update_connections)  # Update connections every 2 seconds

def stop_server():
    server_instance.stop_server()
    update_server_status()

def update_server_status():
    if server_instance.is_running:
        status_label.config(text="Server Status: Running")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
    else:
        status_label.config(text="Server Status: Stopped")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def update_connections():
    connections_list.delete('1.0', tk.END)  # Clear the text area

    # Process all items in the connection queue
    while not server_instance.connection_queue.empty():
        item = server_instance.connection_queue.get()
        if item:
            ip, name = item
            connections_list.insert(tk.END, f"{ip} - {name}\n")  # Add IP and name of the computer

    # Append all current connections to the text area
    connections = server_instance.get_connections()
    for ip, name in connections:
        connections_list.insert(tk.END, f"{ip} - {name}\n")  # Add IP and name of the computer

    root.after(5000, update_connections)  # Adjust to update every 5 seconds (5000 ms)


# Create the main application window
root = tk.Tk()
root.title("Server GUI")

# Create a frame for server controls
control_frame = tk.Frame(root)
control_frame.pack(padx=10, pady=10)

start_button = tk.Button(control_frame, text="Start Server", command=start_server)
start_button.pack(side=tk.LEFT, padx=5, pady=5)

stop_button = tk.Button(control_frame, text="Stop Server", command=stop_server, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5, pady=5)

status_label = tk.Label(root, text="Server Status: Stopped")
status_label.pack(padx=10, pady=(0, 10))

connections_list = scrolledtext.ScrolledText(root, height=10, width=50, wrap=tk.WORD)
connections_list.pack(padx=10, pady=10)

# Initialize the server status and start updating connections
update_server_status()
root.after(2000, update_connections)  # Start the update loop for connections

# Run the application
root.mainloop()
