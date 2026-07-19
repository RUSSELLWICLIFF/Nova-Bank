import tkinter as tk                    # Import tkinter library for creating GUI
from tkinter import messagebox         # Import messagebox to show popup alerts
from datetime import datetime          # Import datetime to get current date and time

# --- Dictionary to store all user accounts ---
accounts = {}

# --- Variable to track who is currently logged in ---
current_user = ""

# --- Function to get the current date and time as a string ---
def now():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")  # Format: 16-07-2026 05:30 PM

# --- Function to remove all widgets from the window (used when switching pages) ---
def clear(win):
    for widget in win.winfo_children():   # Loop through every widget in the window
        widget.destroy()                   # Delete/remove that widget


# ===================== LOGIN PAGE =====================
def login(win):
    clear(win)                             # Clear the window before showing login page
    win.title("Nova Bank - Login")         # Set the window title
    win.config(bg="white")                 # Set window background color to white

    # --- Header bar at the top ---
    header = tk.Frame(win, bg="#5A5A5A", height=55)
    header.pack(fill="x")                          # Stretch it across full width
    tk.Label(
        header,
        text="NOVA BANK",
        font=("Arial", 18, "bold"),
        bg="#5A5A5A",
        fg="white"
    ).pack(expand=True)                   # Center the label inside the header

    # --- Form frame (contains username, password, buttons) ---
    f = tk.Frame(win, bg="white")
    f.pack(expand=True, anchor="n", pady=(30, 0))  # Place at top-center with 30px padding

    # --- Username label and input box ---
    tk.Label(f, text="Username", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack()
    u = tk.StringVar()                    # Variable to store what user types in username box
    tk.Entry(f, textvariable=u, font=("Arial", 11), relief="solid", bd=1, width=20).pack(pady=4)

    # --- Password label and input box ---
    tk.Label(f, text="Password", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack()
    p = tk.StringVar()                    # Variable to store what user types in password box
    tk.Entry(f, textvariable=p, show="*", font=("Arial", 11), relief="solid", bd=1, width=20).pack(pady=4)

    # --- Login button action ---
    def do_login():
        global current_user               # Use the global variable current_user
        username = u.get().strip()        # Get username from input, remove extra spaces
        password = p.get().strip()        # Get password from input, remove extra spaces
        if not username or not password:
            messagebox.showwarning("Warning", "Fill all fields")
            return                        # Stop the function here
        if username not in accounts:
            messagebox.showerror("Error", "User not found")
            return
        if accounts[username]["password"] != password:
            messagebox.showerror("Error", "Wrong password")
            return
        current_user = username           # Save the logged in username
        dashboard(win)                    # Go to dashboard page

    # --- Login button ---
    tk.Button(
        f,
        text="Login",
        command=do_login,                 # Call do_login when clicked
        bg="#5A5A5A",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=20
    ).pack(pady=6)

    # --- Register button ---
    tk.Button(
        f,
        text="Register",
        command=lambda: register(win),    # lambda runs register(win) when clicked
        bg="#5A5A5A",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        width=20
    ).pack(pady=2)

    win.bind("<Return>", lambda e: do_login())  # Press Enter key to trigger login


# ==================== REGISTER PAGE ====================
def register(win):
    clear(win)                             # Clear the window
    win.title("Nova Bank - Register")
    win.config(bg="white")

    # --- Header bar ---
    header = tk.Frame(win, bg="#5A5A5A", height=50)
    header.pack(fill="x")
    tk.Label(
        header,
        text="Create Account",
        font=("Arial", 15, "bold"),
        bg="#5A5A5A",
        fg="white"
    ).pack(expand=True)

    # --- Form frame ---
    f = tk.Frame(win, bg="white", padx=40)
    f.pack(pady=15)

    # --- Full Name field ---
    tk.Label(f, text="Full Name", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(anchor="w")
    name = tk.StringVar()
    tk.Entry(f, textvariable=name, font=("Arial", 11), relief="solid", bd=1).pack(fill="x", pady=2)

    # --- Username field ---
    tk.Label(f, text="Username", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(anchor="w")
    uname = tk.StringVar()
    tk.Entry(f, textvariable=uname, font=("Arial", 11), relief="solid", bd=1).pack(fill="x", pady=2)

    # --- Password field ---
    tk.Label(f, text="Password", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(anchor="w")
    pwd = tk.StringVar()
    tk.Entry(f, textvariable=pwd, show="*", font=("Arial", 11), relief="solid", bd=1).pack(fill="x", pady=2)

    # --- Account Type dropdown ---
    tk.Label(f, text="Account Type", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(anchor="w")
    acc_type = tk.StringVar(value="Savings")               # Default selected value is Savings
    tk.OptionMenu(f, acc_type, "Savings", "Current", "Salary").pack(anchor="w")  # Dropdown menu

    # --- Register button action ---
    def do_register():
        n = name.get().strip()
        u = uname.get().strip()
        pw = pwd.get().strip()
        if not n or not u or not pw:
            messagebox.showwarning("Warning", "Fill all fields")
            return
        if len(pw) < 4:
            messagebox.showwarning("Warning", "Password min 4 chars")
            return
        if u in accounts:
            messagebox.showerror("Error", "Username taken")
            return
        acc_no = "NB" + str(1001 + len(accounts))         # Generate unique account number
        accounts[u] = {                                    # Save account in dictionary
            "name": n,
            "password": pw,
            "balance": 0.0,                                # Starting balance is Rs.0
            "acc_no": acc_no,
            "type": acc_type.get(),                        # Get selected account type
            "history": []                                  # Empty list for transactions
        }
        messagebox.showinfo("Success", "Account " + acc_no + " created!")
        login(win)                                         # Go back to login after registering

    # --- Register button ---
    tk.Button(
        f,
        text="Register",
        command=do_register,
        bg="#5A5A5A",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(fill="x", pady=8)

    # --- Back to Login button ---
    tk.Button(
        f,
        text="Back to Login",
        command=lambda: login(win),
        bg="#5A5A5A",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(fill="x", pady=2)


# ==================== DASHBOARD PAGE ====================
def dashboard(win):
    clear(win)                                        # Clear the window
    user = accounts[current_user]                     # Get the logged in user's data
    win.title("Nova Bank - " + user["name"])
    win.config(bg="#F2F2F2")

    # --- Header bar ---
    header = tk.Frame(win, bg="#5A5A5A")
    header.pack(fill="x")

    tk.Label(header, text="NOVA BANK", font=("Arial", 14, "bold"),
             bg="#5A5A5A", fg="white").pack(side="left", padx=14, pady=10)

    # Balance badge that updates when deposit/withdraw happens
    bal_badge = tk.Frame(header, bg="#787878", padx=12, pady=4)
    bal_badge.pack(side="left", padx=6)
    tk.Label(bal_badge, text="Balance", font=("Arial", 8),
             bg="#787878", fg="#DDDDDD").pack()
    bal_label = tk.Label(bal_badge, text="Rs." + str(round(user["balance"], 2)),
                         font=("Arial", 12, "bold"), bg="#787878", fg="white")
    bal_label.pack()

    # Right: user name + logout button
    right_hdr = tk.Frame(header, bg="#5A5A5A")
    right_hdr.pack(side="right", padx=10, pady=8)
    tk.Label(right_hdr, text=user["name"], font=("Arial", 10),
             bg="#5A5A5A", fg="#DDDDDD").pack(side="left", padx=(0, 12))

    # --- Logout button action ---
    def do_logout():
        global current_user
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            current_user = ""                                  # Clear logged in user
            login(win)                                         # Go back to login page

    # --- Logout button on the right side of header ---
    tk.Button(right_hdr, text="Logout", command=do_logout,
              bg="#DC2626", fg="white", font=("Arial", 9, "bold"),
              relief="flat", padx=12, pady=4, cursor="hand2").pack(side="left")

    # --- Main body area ---
    body = tk.Frame(win, bg="#F2F2F2")
    body.pack(fill="both", expand=True, padx=14, pady=12)
    body.columnconfigure(1, weight=1)
    body.rowconfigure(0, weight=1)

    # Helper: card frame with soft gray border
    def make_card(parent, **kw):
        return tk.Frame(parent, bg="white", bd=0,
                        highlightbackground="#BBBBBB", highlightthickness=1, **kw)

    # --- Left panel card ---
    left_card = make_card(body, width=230)
    left_card.grid(row=0, column=0, sticky="ns", padx=(0, 10))
    left_card.pack_propagate(False)                   # Prevent frame from shrinking

    # --- Account info header strip ---
    info_strip = tk.Frame(left_card, bg="#5A5A5A", height=34)
    info_strip.pack(fill="x")
    info_strip.pack_propagate(False)
    tk.Label(info_strip, text="Account Info", font=("Arial", 10, "bold"),
             bg="#5A5A5A", fg="white").pack(expand=True)

    # --- Account information rows ---
    info_body = tk.Frame(left_card, bg="white", padx=14, pady=10)
    info_body.pack(fill="x")
    for label, value in [("Name", user["name"]), ("A/C No", user["acc_no"]), ("Type", user["type"])]:
        row = tk.Frame(info_body, bg="white")
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, font=("Arial", 8), bg="white",
                 fg="#888888", width=7, anchor="w").pack(side="left")
        tk.Label(row, text=value, font=("Arial", 9, "bold"),
                 bg="white", fg="#333333", anchor="w").pack(side="left")

    # --- Quick Transaction section header ---
    tx_hdr = tk.Frame(left_card, bg="white", padx=14, pady=8)
    tx_hdr.pack(fill="x")
    tk.Label(tx_hdr, text="Quick Transaction", font=("Arial", 10, "bold"),
             bg="white", fg="#333333").pack(anchor="w")

    # --- Amount input ---
    tx_body = tk.Frame(left_card, bg="white", padx=14)
    tx_body.pack(fill="x")
    tk.Label(tx_body, text="Amount (Rs.)", font=("Arial", 9),
             bg="white", fg="#888888").pack(anchor="w", pady=(4, 2))
    amount = tk.StringVar()
    tk.Entry(tx_body, textvariable=amount, font=("Arial", 11),
             relief="solid", bd=1, bg="white", fg="#333333").pack(fill="x", pady=2)

    # --- Deposit and Withdraw buttons frame ---
    btn_frame = tk.Frame(left_card, bg="white", padx=14, pady=12)
    btn_frame.pack(fill="x")
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    # --- Right panel card - Transaction History ---
    right_card = make_card(body)
    right_card.grid(row=0, column=1, sticky="nsew")

    # --- Transaction history header strip ---
    hist_strip = tk.Frame(right_card, bg="#5A5A5A", height=34)
    hist_strip.pack(fill="x")
    hist_strip.pack_propagate(False)
    tk.Label(hist_strip, text="Transaction History", font=("Arial", 10, "bold"),
             bg="#5A5A5A", fg="white").pack(side="left", padx=12, anchor="w", expand=True)

    # --- Column headers ---
    col_hdr = tk.Frame(right_card, bg="#EEEEEE", padx=8, pady=5)
    col_hdr.pack(fill="x")
    for txt, w in [("Type", 10), ("Amount", 12), ("Balance", 14), ("Date & Time", 22)]:
        tk.Label(col_hdr, text=txt, font=("Arial", 8, "bold"),
                 bg="#EEEEEE", fg="#333333", width=w, anchor="w").pack(side="left")

    # --- Listbox to display all past transactions ---
    hist_frame = tk.Frame(right_card, bg="white")
    hist_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(hist_frame)
    scrollbar.pack(side="right", fill="y")
    history_box = tk.Listbox(hist_frame, font=("Courier", 9), relief="flat", bd=0,
                              bg="white", fg="#333333", selectbackground="#DDDDDD",
                              selectforeground="#333333", activestyle="none",
                              yscrollcommand=scrollbar.set)
    history_box.pack(fill="both", expand=True, padx=4, pady=4)
    scrollbar.config(command=history_box.yview)       # Connect scrollbar to listbox

    # --- Update balance label and refresh history list ---
    def update_balance():
        bal_label.config(text="Rs." + str(round(user["balance"], 2)))  # Update header balance
        history_box.delete(0, tk.END)                  # Clear all items from listbox
        if not user["history"]:
            history_box.insert(tk.END, "  No transactions yet.")
            return
        for i, t in enumerate(user["history"]):        # Loop through each transaction
            sign = "+" if t["type"] == "Deposit" else "-"
            line = ("  " + t["type"].ljust(10) + " " + sign + "Rs." +
                    str(t["amount"]).ljust(9) + "  Bal:Rs." +
                    str(t["balance"]).ljust(10) + "  " + t["time"])
            history_box.insert(tk.END, line)
            # Alternate row shading
            if i % 2 == 0:
                history_box.itemconfig(i, bg="#F7F7F7", fg="#333333")
            else:
                history_box.itemconfig(i, bg="white", fg="#333333")

    # --- Save a transaction to history ---
    def add_record(ttype, amt):
        user["history"].insert(0, {                    # Add at the beginning (latest first)
            "type": ttype, "amount": amt,
            "time": now(),                             # Save current time
            "balance": user["balance"]                 # Save balance after transaction
        })

    # --- Deposit money ---
    def deposit():
        if not amount.get():
            messagebox.showwarning("Warning", "Enter Amount"); return
        try:
            amt = int(amount.get())                    # Convert input text to number
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")
            amount.set(""); return
        if amt <= 0:
            messagebox.showerror("Error", "Invalid Amount")
        elif amt > 100000:
            messagebox.showwarning("Warning", "Max deposit is Rs.1,00,000")
        else:
            user["balance"] += amt                     # Add amount to balance
            add_record("Deposit", amt)                 # Save to history
            update_balance()                           # Refresh display
            messagebox.showinfo("Success", "Amount Deposited Successfully")
        amount.set("")                                 # Clear amount input

    # --- Withdraw money ---
    def withdraw():
        if not amount.get():
            messagebox.showwarning("Warning", "Enter Amount"); return
        try:
            amt = int(amount.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")
            amount.set(""); return
        if amt <= 0:
            messagebox.showerror("Error", "Invalid Amount")
        elif amt > user["balance"]:
            messagebox.showerror("Error", "Insufficient Balance")
        elif amt > 50000:
            messagebox.showwarning("Warning", "Max withdraw is Rs.50,000")
        else:
            user["balance"] -= amt                     # Subtract amount from balance
            add_record("Withdraw", amt)                # Save to history
            update_balance()                           # Refresh display
            messagebox.showinfo("Success", "Amount Withdrawn Successfully")
        amount.set("")                                 # Clear amount input

    # --- Deposit button ---
    tk.Button(btn_frame, text="Deposit", command=deposit,
              bg="#16A34A", fg="white", font=("Arial", 9, "bold"),
              relief="flat", cursor="hand2", pady=7
              ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

    # --- Withdraw button ---
    tk.Button(btn_frame, text="Withdraw", command=withdraw,
              bg="#DC2626", fg="white", font=("Arial", 9, "bold"),
              relief="flat", cursor="hand2", pady=7
              ).grid(row=0, column=1, sticky="ew")

    update_balance()       # Load history and balance when dashboard opens


# ===================== START APP =====================
root = tk.Tk()                     # Create the main window
root.geometry("800x500")           # Set window size: 800 wide, 500 tall
root.resizable(True, True)         # Allow window to be resized
login(root)                        # Show the login page first
root.mainloop()                    # Start the app and keep it running