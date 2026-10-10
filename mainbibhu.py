import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ==========================================
# DATABASE CONFIGURATION
# ==========================================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Bibhusql@969"  # Your MySQL root password
DB_NAME = "movie_booking_db"

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to connect to MySQL: {err}")
        return None

# ==========================================
# 1. LOGIN WINDOW
# ==========================================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Booking System - Login")
        self.root.geometry("380x280")
        self.root.resizable(False, False)

        tk.Label(root, text="Admin Login", font=("Arial", 18, "bold")).pack(pady=20)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(frame, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(root, text="Login", command=self.login, font=("Arial", 11, "bold"), bg="#28a745", fg="white", width=12).pack(pady=15)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password!")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                messagebox.showinfo("Success", "Login Successful!")
                self.root.destroy()
                open_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Username or Password!")

# ==========================================
# 2. DASHBOARD / MAIN APPLICATION WINDOW
# ==========================================
class DashboardWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking Management System")
        self.root.geometry("980x620")
        self.root.resizable(False, False)

        # Selected booking ID tracker for update/delete
        self.selected_id = None

        # Title Header
        tk.Label(
            root, 
            text="🎬 Movie Ticket Booking Management System", 
            font=("Arial", 18, "bold"), 
            bg="#343a40", 
            fg="white", 
            pady=12
        ).pack(fill="x")

        # Main Layout Container
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- FORM FRAME (LEFT SIDE) ----------------
        form_frame = tk.LabelFrame(main_frame, text=" Booking Details ", font=("Arial", 11, "bold"), padx=15, pady=15)
        form_frame.place(x=10, y=10, width=380, height=530)

        tk.Label(form_frame, text="Customer Name:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
        self.name_entry = tk.Entry(form_frame, width=22, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, pady=8)

        tk.Label(form_frame, text="Phone Number:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
        self.phone_entry = tk.Entry(form_frame, width=22, font=("Arial", 10))
        self.phone_entry.grid(row=1, column=1, pady=8)

        tk.Label(form_frame, text="Select Movie:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
        self.movie_cb = ttk.Combobox(
            form_frame, 
            values=["Avatar 2", "Inception", "Interstellar", "Oppenheimer", "Avengers"], 
            state="readonly", 
            width=20, 
            font=("Arial", 10)
        )
        self.movie_cb.grid(row=2, column=1, pady=8)

        tk.Label(form_frame, text="Show Time:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8)
        self.time_cb = ttk.Combobox(
            form_frame, 
            values=["10:00 AM", "01:30 PM", "05:00 PM", "08:30 PM"], 
            state="readonly", 
            width=20, 
            font=("Arial", 10)
        )
        self.time_cb.grid(row=3, column=1, pady=8)

        tk.Label(form_frame, text="Seats:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=8)
        self.seats_entry = tk.Entry(form_frame, width=22, font=("Arial", 10))
        self.seats_entry.grid(row=4, column=1, pady=8)

        tk.Label(form_frame, text="Price / Ticket ($):", font=("Arial", 10)).grid(row=5, column=0, sticky="w", pady=8)
        self.price_entry = tk.Entry(form_frame, width=22, font=("Arial", 10))
        self.price_entry.insert(0, "12.00")
        self.price_entry.grid(row=5, column=1, pady=8)

        # Buttons Frame
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Add Booking", command=self.add_booking, bg="#007bff", fg="white", font=("Arial", 10, "bold"), width=13).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Update", command=self.update_booking, bg="#ffc107", fg="black", font=("Arial", 10, "bold"), width=13).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_booking, bg="#dc3545", fg="white", font=("Arial", 10, "bold"), width=13).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Clear/Reset", command=self.clear_fields, bg="#6c757d", fg="white", font=("Arial", 10, "bold"), width=13).grid(row=1, column=1, padx=5, pady=5)

        # Logout Button
        tk.Button(form_frame, text="Logout", command=self.logout, bg="#343a40", fg="white", font=("Arial", 10, "bold"), width=28).grid(row=7, column=0, columnspan=2, pady=10)

        # ---------------- TABLE & SEARCH FRAME (RIGHT SIDE) ----------------
        right_frame = tk.Frame(main_frame)
        right_frame.place(x=400, y=10, width=550, height=530)

        # Search Bar Area
        search_frame = tk.LabelFrame(right_frame, text=" Search Records ", font=("Arial", 10, "bold"), padx=10, pady=5)
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(search_frame, text="Keyword:", font=("Arial", 10)).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=20)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_booking, bg="#17a2b8", fg="white", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", command=self.fetch_bookings, bg="#6c757d", fg="white", font=("Arial", 9, "bold")).pack(side="left", padx=5)

        # Treeview Scrollable Table
        table_container = tk.Frame(right_frame)
        table_container.pack(fill="both", expand=True)

        scroll_y = tk.Scrollbar(table_container, orient="vertical")
        scroll_x = tk.Scrollbar(table_container, orient="horizontal")

        self.tree = ttk.Treeview(
            table_container, 
            columns=("ID", "Name", "Phone", "Movie", "Time", "Seats", "Total"), 
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Customer")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Movie", text="Movie")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Seats", text="Seats")
        self.tree.heading("Total", text="Total ($)")

        self.tree.column("ID", width=35, anchor="center")
        self.tree.column("Name", width=100)
        self.tree.column("Phone", width=90)
        self.tree.column("Movie", width=100)
        self.tree.column("Time", width=80)
        self.tree.column("Seats", width=50, anchor="center")
        self.tree.column("Total", width=70, anchor="e")

        self.tree["show"] = "headings"
        self.tree.pack(fill="both", expand=True)

        # Bind row selection event
        self.tree.bind("<ButtonRelease-1>", self.get_selected_row)

        # Initial fetch of all bookings
        self.fetch_bookings()

    # ==========================================
    # DATABASE & EVENT LOGIC
    # ==========================================
    def fetch_bookings(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bookings")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            conn.close()

    def add_booking(self):
        if not self.validate_fields():
            return

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        movie = self.movie_cb.get()
        time = self.time_cb.get()
        seats = int(self.seats_entry.get().strip())
        price_per_seat = float(self.price_entry.get().strip())
        total = seats * price_per_seat

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO bookings (customer_name, phone, movie_name, show_time, seats, total_price) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, phone, movie, time, seats, total))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Booking added successfully!")
            self.clear_fields()
            self.fetch_bookings()

    def get_selected_row(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        content = self.tree.item(selected_item)
        row = content["values"]

        if row:
            self.clear_fields()
            self.selected_id = row[0]
            self.name_entry.insert(0, row[1])
            self.phone_entry.insert(0, row[2])
            self.movie_cb.set(row[3])
            self.time_cb.set(row[4])
            self.seats_entry.insert(0, row[5])

    def update_booking(self):
        if not self.selected_id:
            messagebox.showwarning("Select Record", "Please select a booking from the table to update.")
            return

        if not self.validate_fields():
            return

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        movie = self.movie_cb.get()
        time = self.time_cb.get()
        seats = int(self.seats_entry.get().strip())
        price_per_seat = float(self.price_entry.get().strip())
        total = seats * price_per_seat

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE bookings SET customer_name=%s, phone=%s, movie_name=%s, show_time=%s, seats=%s, total_price=%s WHERE booking_id=%s"
            cursor.execute(query, (name, phone, movie, time, seats, total, self.selected_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Booking updated successfully!")
            self.clear_fields()
            self.fetch_bookings()

    def delete_booking(self):
        if not self.selected_id:
            messagebox.showwarning("Select Record", "Please select a booking from the table to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?")
        if confirm:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (self.selected_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Booking deleted successfully!")
                self.clear_fields()
                self.fetch_bookings()

    def search_booking(self):
        query_text = self.search_entry.get().strip()
        if not query_text:
            messagebox.showwarning("Input Error", "Please enter a customer name or movie title to search.")
            return

        self.tree.delete(*self.tree.get_children())
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM bookings WHERE customer_name LIKE %s OR movie_name LIKE %s"
            cursor.execute(query, (f"%{query_text}%", f"%{query_text}%"))
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            conn.close()

    def validate_fields(self):
        if not self.name_entry.get().strip() or not self.phone_entry.get().strip() or not self.movie_cb.get() or not self.time_cb.get():
            messagebox.showwarning("Validation Error", "All fields are required!")
            return False
        if not self.seats_entry.get().strip().isdigit():
            messagebox.showwarning("Validation Error", "Seats must be a valid numeric integer!")
            return False
        try:
            float(self.price_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Validation Error", "Price per ticket must be a valid decimal number!")
            return False
        return True

    def clear_fields(self):
        self.selected_id = None
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.movie_cb.set('')
        self.time_cb.set('')
        self.seats_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def logout(self):
        self.root.destroy()
        open_login()

# ==========================================
# APPLICATION ENTRY POINTS
# ==========================================
def open_login():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

def open_dashboard():
    root = tk.Tk()
    app = DashboardWindow(root)
    root.mainloop()

if __name__ == "__main__":
    open_login()