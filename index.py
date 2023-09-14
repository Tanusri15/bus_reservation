import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="bus_reservation_system"
)

cursor = db.cursor()

def list_buses():
    cursor.execute("SELECT b.id, b.bus_number, b.total_seats, (b.total_seats - COUNT(r.id)) AS seats_left FROM buses b LEFT JOIN reservations r ON b.id = r.bus_id GROUP BY b.id, b.bus_number, b.total_seats")
    buses = cursor.fetchall()
    
    bus_treeview.delete(*bus_treeview.get_children())
    for bus in buses:
        bus_treeview.insert("", "end", values=(bus[0], bus[1], bus[3], bus[2]))

def reserve_seat():
    selected_item = bus_treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a bus to reserve a seat.")
        return

    passenger_name = passenger_name_entry.get()
    if not passenger_name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    bus_id = bus_treeview.item(selected_item)['values'][0]
    
    cursor.execute("INSERT INTO reservations (passenger_name, bus_id) VALUES (%s, %s)", (passenger_name, bus_id))
    db.commit()
    # messagebox.showinfo("Success", "Seat reserved successfully!")
    

# Create the main window
root = tk.Tk()
root.title("RedBus - Bus Reservation System")

# Header Label
header_label = tk.Label(root, text="RedBus - Bus Reservation System", font=("Helvetica", 16))
header_label.pack(pady=10)

# Bus List Treeview
bus_treeview = ttk.Treeview(root, columns=("ID", "Bus Number", "Seats Left", "Total Seats"), show="headings", height=10)
bus_treeview.heading("ID", text="ID")
bus_treeview.heading("Bus Number", text="Bus Number")
bus_treeview.heading("Total Seats", text="Total Seats")
bus_treeview.heading("Seats Left", text="Seats Left")
bus_treeview.pack(padx=20, pady=10)

# Refresh Button
refresh_button = tk.Button(root, text="Refresh Bus List", command=list_buses, width=20)
refresh_button.pack(pady=5)

# Passenger Name Entry
passenger_name_label = tk.Label(root, text="Enter your name:", font=("Helvetica", 12))
passenger_name_label.pack(pady=5)

passenger_name_entry = tk.Entry(root, width=30)
passenger_name_entry.pack()

# Reserve Button
reserve_button = tk.Button(root, text="Reserve Seat", command=reserve_seat, width=20, font=("Helvetica", 12))
reserve_button.pack(pady=10)

# Initial bus list
list_buses()

root.mainloop()

# Close the database connection
db.close()
