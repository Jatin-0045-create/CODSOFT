import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store contacts
CONTACTS_FILE = "contacts.json"

# Load existing contacts
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

# Save contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Validate contact details
def validate_contact(name, phone, email, address):
    if not name.strip():
        messagebox.showerror("Error", "Name is required.")
        return False
    if any(char.isdigit() for char in name):
        messagebox.showerror("Error", "Name cannot contain numbers.")
        return False
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone number must contain only digits.")
        return False
    if len(phone) < 7 or len(phone) > 15:
        messagebox.showerror("Error", "Phone number must be between 7 and 15 digits.")
        return False
    if email.strip() and ("@" not in email or "." not in email.split("@")[-1]):
        messagebox.showerror("Error", "Invalid email format.")
        return False
    if not address.strip():
        messagebox.showerror("Error", "Address is required.")
        return False
    return True

# Add new contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get("1.0", tk.END).strip()

    if not validate_contact(name, phone, email, address):
        return

    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts()
    messagebox.showinfo("Success", "Contact added successfully!")
    clear_entries()
    view_contacts()

# View all contacts
def view_contacts():
    contact_list.delete(0, tk.END)
    for contact in contacts:
        contact_list.insert(tk.END, f"{contact['name']} - {contact['phone']}")

# Search contacts
def search_contact():
    query = simpledialog.askstring("Search", "Enter name or phone number:")
    if not query:
        return

    contact_list.delete(0, tk.END)
    for contact in contacts:
        if query.lower() in contact['name'].lower() or query in contact['phone']:
            contact_list.insert(tk.END, f"{contact['name']} - {contact['phone']}")

# Update contact
def update_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a contact to update.")
        return

    index = selected[0]
    contact = contacts[index]

    name = simpledialog.askstring("Update", "Enter new name:", initialvalue=contact['name'])
    phone = simpledialog.askstring("Update", "Enter new phone:", initialvalue=contact['phone'])
    email = simpledialog.askstring("Update", "Enter new email:", initialvalue=contact['email'])
    address = simpledialog.askstring("Update", "Enter new address:", initialvalue=contact['address'])

    if not validate_contact(name, phone, email, address):
        return

    contacts[index] = {"name": name, "phone": phone, "email": email, "address": address}
    save_contacts()
    view_contacts()
    messagebox.showinfo("Success", "Contact updated successfully!")

# Delete contact
def delete_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a contact to delete.")
        return

    index = selected[0]
    confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{contacts[index]['name']}'?")
    if confirm:
        contacts.pop(index)
        save_contacts()
        view_contacts()
        messagebox.showinfo("Deleted", "Contact deleted successfully!")

# Delete all contacts
def delete_all_contacts():
    if not contacts:
        messagebox.showerror("Error", "No contacts to delete.")
        return
    confirm = messagebox.askyesno("Delete All", "Are you sure you want to delete ALL contacts?")
    if confirm:
        contacts.clear()
        save_contacts()
        view_contacts()
        messagebox.showinfo("Deleted", "All contacts deleted successfully!")

# Clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete("1.0", tk.END)

# Initialize window
root = tk.Tk()
root.title("Contact Management System")
root.geometry("550x550")
root.resizable(False, False)

contacts = load_contacts()

# Input fields
frame_input = tk.LabelFrame(root, text="Add / Update Contact", font=("Arial", 12))
frame_input.pack(fill="x", padx=10, pady=5)

tk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = tk.Entry(frame_input, width=40)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
phone_entry = tk.Entry(frame_input, width=40)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
email_entry = tk.Entry(frame_input, width=40)
email_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Address:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
address_entry = tk.Text(frame_input, width=30, height=3)
address_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame_input, text="Add Contact", command=add_contact, bg="lightgreen").grid(row=4, column=0, padx=5, pady=10)
tk.Button(frame_input, text="Clear", command=clear_entries, bg="lightgray").grid(row=4, column=1, padx=5, pady=10, sticky="w")

# Contact list
frame_list = tk.LabelFrame(root, text="Contact List", font=("Arial", 12))
frame_list.pack(fill="both", expand=True, padx=10, pady=5)

contact_list = tk.Listbox(frame_list, height=12, width=50)
contact_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")
contact_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=contact_list.yview)

# Buttons for actions
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="View All", command=view_contacts, bg="lightblue", width=12).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Search", command=search_contact, bg="khaki", width=12).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Update", command=update_contact, bg="orange", width=12).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Delete", command=delete_contact, bg="red", width=12).grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="Delete All", command=delete_all_contacts, bg="darkred", fg="white", width=12).grid(row=1, column=0, columnspan=4, pady=5)

view_contacts()
root.mainloop()