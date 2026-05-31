import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


class ContactBookApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("750x500")
        self.root.minsize(700, 450)

        self.DATA_FILE = "contacts.json"
        self.contacts = self.load_contacts()

        self.setup_ui()
        self.refresh_contact_list()

    # --- Data Persistence ---
    def load_contacts(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_contacts(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.contacts, f, indent=4)

    # --- UI Setup ---
    def setup_ui(self):
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        # Left Frame: Form Fields
        form_frame = ttk.LabelFrame(self.root, text=" Contact Details ", padding=15)
        form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Form Inputs
        fields = [
            ("Name:", "name"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Address:", "address"),
        ]
        self.entries = {}

        for i, (label_text, field_name) in enumerate(fields):
            lbl = ttk.Label(form_frame, text=label_text, font=("Arial", 10))
            lbl.grid(row=i * 2, column=0, sticky="w", pady=(5, 2))

            entry = ttk.Entry(form_frame, font=("Arial", 10))
            entry.grid(row=i * 2 + 1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            self.entries[field_name] = entry

        form_frame.columnconfigure(0, weight=1)

        # Action Buttons inside Form Frame
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        btn_frame.columnconfigure((0, 1), weight=1)

        self.btn_add = ttk.Button(
            btn_frame, text="Add Contact", command=self.add_contact
        )
        self.btn_add.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_update = ttk.Button(
            btn_frame, text="Update", command=self.update_contact, state="disabled"
        )
        self.btn_update.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.btn_clear = ttk.Button(
            btn_frame, text="Clear Form", command=self.clear_form
        )
        self.btn_clear.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Right Frame: View & Search
        view_frame = ttk.Frame(self.root, padding=15)
        view_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        view_frame.columnconfigure(0, weight=1)
        view_frame.rowconfigure(1, weight=1)

        # Search Bar
        search_frame = ttk.Frame(view_frame)
        search_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search:", font=("Arial", 10)).grid(
            row=0, column=0, padx=(0, 5)
        )
        self.search_entry = ttk.Entry(search_frame, font=("Arial", 10))
        self.search_entry.grid(row=0, column=1, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.search_contacts)

        # Contact Treeview List
        columns = ("name", "phone")
        self.tree = ttk.Treeview(
            view_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone Number")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("phone", width=150, anchor="w")
        self.tree.grid(row=1, column=0, sticky="nsew")

        # Scrollbar for List
        scrollbar = ttk.Scrollbar(
            view_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_contact_select)

        # Delete Button
        self.btn_delete = ttk.Button(
            view_frame, text="Delete Selected Contact", command=self.delete_contact
        )
        self.btn_delete.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")

    # --- Backend Functions ---
    def refresh_contact_list(self, filter_dict=None):
        """Populates the list view. Can be filtered by search."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        target_list = filter_dict if filter_dict is not None else self.contacts

        # Sort alphabetically by name
        for name in sorted(target_list.keys()):
            phone = target_list[name]["phone"]
            self.tree.insert("", "end", iid=name, values=(name, phone))

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["name"].config(state="normal")
        self.btn_add.config(state="normal")
        self.btn_update.config(state="disabled")
        self.tree.selection_remove(self.tree.selection())

    def on_contact_select(self, event):
        """Fills the form when a contact is clicked in the list."""
        selected = self.tree.selection()
        if not selected:
            return

        name = selected[0]
        details = self.contacts[name]

        self.clear_form()

        # Populate form
        self.entries["name"].insert(0, name)
        self.entries["name"].config(state="disabled")  # Primary Key locked
        self.entries["phone"].insert(0, details["phone"])
        self.entries["email"].insert(0, details["email"])
        self.entries["address"].insert(0, details["address"])

        self.btn_add.config(state="disabled")
        self.btn_update.config(state="normal")

    def add_contact(self):
        name = self.entries["name"].get().strip()
        phone = self.entries["phone"].get().strip()
        email = self.entries["email"].get().strip()
        address = self.entries["address"].get().strip()

        if not name or not phone:
            messagebox.showwarning("Error", "Name and Phone Number are required!")
            return

        if name in self.contacts:
            messagebox.showwarning(
                "Error", "A contact with this name already exists."
            )
            return

        self.contacts[name] = {"phone": phone, "email": email, "address": address}
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_form()
        messagebox.showinfo("Success", "Contact added successfully!")

    def update_contact(self):
        name = self.entries["name"].get().strip()
        phone = self.entries["phone"].get().strip()
        email = self.entries["email"].get().strip()
        address = self.entries["address"].get().strip()

        if not phone:
            messagebox.showwarning("Error", "Phone Number cannot be empty!")
            return

        if name in self.contacts:
            self.contacts[name] = {
                "phone": phone,
                "email": email,
                "address": address,
            }
            self.save_contacts()
            self.refresh_contact_list()
            self.clear_form()
            messagebox.showinfo("Success", "Contact updated successfully!")

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a contact from the list to delete."
            )
            return

        name = selected[0]
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete {name}?"
        )

        if confirm:
            del self.contacts[name]
            self.save_contacts()
            self.refresh_contact_list()
            self.clear_form()
            messagebox.showinfo("Deleted", "Contact deleted successfully.")

    def search_contacts(self, event):
        """Filters the contact list dynamically as the user types."""
        query = self.search_entry.get().strip().lower()
        if not query:
            self.refresh_contact_list()
            return

        filtered = {}
        for name, details in self.contacts.items():
            if query in name.lower() or query in details["phone"]:
                filtered[name] = details

        self.refresh_contact_list(filter_dict=filtered)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
