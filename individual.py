#GUI(INTERFACE)
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

messagebox.showinfo("Greeting", "HOLA! WELCOME TO CHICSAE!!")

def calculate_total():
    total = 0.0
    for item, details in selected_items.items():
        total += details['price'] * details['quantity']
    total_label.config(text=f"Total: RM{total:.2f}")
    return total

def add_to_cart():
    item = menu_var.get()
    quantity = quantity_var.get()
    spiciness = spiciness_var.get()

    try:
        quantity = int(quantity_var.get())
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please select a valid item and quantity.")
        return

    if item in selected_items:
        selected_items[item]['quantity'] += quantity
    else:
        selected_items[item] = {
            'price': menu[item],
             'quantity': quantity,
                'spiciness': spiciness
        }

    update_cart()
    calculate_total()

def update_cart():
    cart_text.delete(1.0, tk.END)
    for item, details in selected_items.items():
        cart_text.insert(
            tk.END, 
            f"{item} x{details['quantity']} ({details['spiciness']} - RM{details['price'] * details['quantity']:.2f}\n"
        )

def confirm_order():
    print("Confirm Order button clicked!")  # Debug
    total = calculate_total()
    if not selected_items:
        messagebox.showerror("No Items", "Oh No! Your cart is empty!")
        return

    order_type = order_type_var.get()
    payment_method = payment_var.get()
    pickup_time = None
    coupons= coupon_var

    # Handle order type
    order_type = order_type_var.get()
    if order_type == "Pick-Up":
        pickup_time = simpledialog.askstring("Pickup Time", "Please enter your pickup time (e.g., 3:00 PM):")
        if not pickup_time:
            messagebox.showerror("Missing Information", "Pickup time is required for pick-up orders.")
            return

    order_type = order_type_var.get()
    payment_method = payment_var.get()
    if order_type not in ["Delivery", "Pick-Up"] or payment_method not in ["Card", "Cash"]:
        messagebox.showerror("Invalid Input", "Please select a valid order type and payment method.")
        return

    # Compile order details
    order_summary = "\n".join([
            f"{item} x{details['quantity']} ({details['spiciness']}) - RM{details['price'] * details['quantity']:.2f}"
            for item, details in selected_items.items()
        ])
    order_details = (
            f"Customer: {customer_name}\n"
            f"Contact: {contact_number}\n"
            f"Order Type: {order_type}\n"
            f"Pickup Time: {pickup_time if pickup_time else 'N/A'}\n"
            f"Discounted Total: RM{final_total:.2f}\n\n"
            f"Order Summary:\n{order_summary}\n"
            f"Address:\n{address}"
        )

    # Display order confirmation
    messagebox.showinfo("Order Confirmed", order_details)
    clear_order()

def clear_order():
    selected_items.clear()
    update_cart()
    calculate_total()
   
# Initialize Tkinter
root = tk.Tk()
root.title("CHICSAE Booking System")

# Customer Name and Contact Number Entry
def get_customer_details():
    global customer_name, contact_number, address 

    # Get Customer Name
    while True:
        customer_name = simpledialog.askstring("Customer Name", "Please enter your name:")
        if customer_name and customer_name.strip():
            customer_name = customer_name.strip()  # Remove leading/trailing spaces
            break
        else:
            messagebox.showerror("Input Error", "Name cannot be empty. Please try again.")

    # Get Contact Number
    while True:
        contact_number = simpledialog.askstring("Contact Number", "Please enter your contact number:")
        if not contact_number:
            messagebox.showerror("Input Error", "Contact number cannot be empty. Please try again.")
            continue
        if not contact_number.isdigit() or len(contact_number) < 10 or len(contact_number) > 15:
            messagebox.showerror("Input Error", "Contact number must contain only digits and be 10-15 characters long.")
            continue
        break
    # Get Address
    while True:
        address = simpledialog.askstring("Address", "Please enter your address:")
        if address and address.strip():
            address = address.strip()  # Remove leading/trailing spaces
            break
        else:
            messagebox.showerror("Input Error", "Address cannot be empty. Please try again.")

# Prompt to get the customer's details when the app starts
get_customer_details()

# Set the window size to landscape (wide)
root.geometry("700x695")  # Width x Height (width is larger than height)

# Customize fonts
title_font = ("Helvetica", 30, "bold")
label_font = ("Arial", 30)
button_font = ("Verdana", 30, "bold")

# Customize colors
bg_color = "#FFFACD"  # lemon chiffon background
btn_color = "#FFDB58"  #  Mustard Yellow buttons
btn_text_color = "white"

root.configure(bg=bg_color)

from tkinter import ttk

style = ttk.Style()
style.theme_use("default")  # Choose a theme like 'clam', 'alt', 'default', etc.
style.configure("TButton", font=("Verdana", 25, "bold"), background=btn_color)
style.configure("TLabel", font=label_font, background=bg_color)

# Update widgets
menu_label = tk.Label(root, text="Menu:", font=label_font, bg=bg_color)
add_button = tk.Button(root, text="Add to Cart", font=button_font, bg=btn_color, fg=btn_text_color)

menu_frame = tk.Frame(root, bg=bg_color)
menu_frame.pack()

cart_frame = tk.Frame(root, bg=bg_color)
cart_frame.pack()

# Menu Items and Prices
menu = {
    "Chicken Bucket": 25.99,
    "Bucket Loaded Fries": 9.49,
    "Soft Drink": 2.99,
    "Chicken Wings": 10.49,
    "Caesar Salad": 6.99
}

selected_items = {}

# Dropdown for Menu
menu_var = tk.StringVar(value=list(menu.keys())[0])
menu_label = tk.Label(root, text="Menu:")
menu_label.pack(pady=5)
menu_dropdown = tk.OptionMenu(root, menu_var,*menu.keys())
menu_dropdown.pack(pady=5)

# Spiciness Selector
spiciness_var = tk.StringVar(value="None")
spiciness_label = tk.Label(root, text="Spiciness Level:")
spiciness_label.pack(pady=5)
spiciness_dropdown = tk.OptionMenu(root, spiciness_var, "None", "Original", "Mild", "Medium", "Spicy")
spiciness_dropdown.pack(pady=5)

# Quantity Selector
quantity_var = tk.IntVar(value=1)
quantity_label = tk.Label(root, text="Quantity:" )
quantity_label.pack(pady=5)
quantity_entry = tk.Entry(root, textvariable=quantity_var, width=10)
quantity_entry.pack(pady=5)

# Add to Cart Button
add_button = tk.Button(root, text="Add to Cart", command=add_to_cart, bg="grey", fg="white")
add_button.pack(pady=5)

# Cart Display
cart_label = tk.Label(root, text="Cart:")
cart_label.pack(pady=5)
cart_text = tk.Text(root, height=5, width=40)
cart_text.pack(pady=5)

# Total Price
total_label = tk.Label(root, text="Total: RM0.00")
total_label.pack(pady= 5)


# Order Type
order_type_var = tk.StringVar(value="Delivery")
order_type_label = tk.Label(root, text="Order Type:")
order_type_label.pack()
order_type_dropdown = tk.OptionMenu(root, order_type_var, "Delivery", "Pick-Up")
order_type_dropdown.pack(pady= 5)

# customer request
request_var = tk.StringVar()
request_label = tk.Label(root, text="Other Added Information:")
request_label.pack()
request_entry = tk.Entry(root, textvariable=request_var, width=50)
request_entry.pack()

# coupons
coupons = {
    "CHICSAE10": 10,  # 10% discount
    "SAVE15": 15,     # 15% discount
}
# Coupon Section
coupon_label = tk.Label(root, text="Enter Coupon Code:")
coupon_label.pack(pady=5)
coupon_var = tk.StringVar()
coupon_entry = tk.Entry(root, textvariable=coupon_var, width=30)
coupon_entry.pack(pady=5)
apply_coupon_button = tk.Button(root, text="Apply Coupon", command=lambda: apply_coupon(coupon_var.get()))
apply_coupon_button.pack(pady=5)

# Payment Method
payment_var = tk.StringVar(value="Card")
payment_label = tk.Label(root, text="Payment Method:")
payment_label.pack()
payment_dropdown = tk.OptionMenu(root, payment_var, "Card", "Cash")
payment_dropdown.pack(pady=5)

# Confirm and Clear Buttons
confirm_button = tk.Button(root, text="Confirm Order", command=confirm_order, bg="grey", fg="white")
confirm_button.pack(pady=5)

def confirm_order():
    print("Confirm Order button clicked!")  # Debug message
    # Calculate the total, including discounts
    total = calculate_total()
    if coupon_entry.get():  # Assuming `coupon_entry` is an Entry widget
        try:
                discount = float(coupon_entry.get())
                discounted_total= max(0, total / discount)  # Ensure total doesn't go negative
        except ValueError:
                messagebox.showerror("Invalid Coupon", "Please enter a valid discount value.")
                return

def apply_coupon(code):
    """Apply a coupon and calculate the discounted total."""
    global final_total  # Ensure the discounted total persists across functions
    code = code.strip().upper()  # Standardize the coupon code

    if code in coupons:
        discount = coupons[code]
        total = calculate_total()  # Calculate the current total
        final_total = total * (1 - discount / 100)  # Apply discount
        total_label.config(text=f"Total after {discount}% discount: RM{final_total:.2f}")
        messagebox.showinfo("Coupon Applied", f"Coupon '{code}' applied successfully!")
    else:
        messagebox.showerror("Invalid Coupon", "The coupon code entered is invalid.")

def confirm_order():
    """Confirm the order and display the order details."""
    try:
        # Ensure the cart has items
        if not selected_items:
            messagebox.showerror("No Items", "Your cart is empty!")
            return

        # Order type and pickup time logic
        order_type = order_type_var.get()
        pickup_time = None
        if order_type == "Pick-Up":
            pickup_time = simpledialog.askstring("Pickup Time", "Enter your pickup time (e.g., 3:00 PM):")
            if not pickup_time:
                messagebox.showerror("Missing Information", "Pickup time required for pick-up orders.")
                return

        # Calculate the total (use discounted total if available)
        total = calculate_total()
        final_total = total

        # Compile order details
        order_summary = "\n".join([
            f"{item} x{details['quantity']} ({details.get('spiciness', 'None')}) - RM{details['price'] * details['quantity']:.2f} - Address: {address}"
            for item, details in selected_items.items()
        ])  
        order_details = (
           f"Customer: {customer_name}\n"
            f"Contact: {contact_number}\n"
            f"Order Type: {order_type}\n"
            f"Pickup Time: {pickup_time if pickup_time else 'N/A'}\n"
            f"Discounted Total: RM{final_total:.2f}\n\n"
            f"Order Summary:\n{order_summary}\n"
            f"Address:\n{address}"
        )

        # Display confirmation
        messagebox.showinfo("Order Confirmed", order_details)
        clear_order()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Clear button
clear_button = tk.Button(root, text="Clear Cart", command=clear_order, bg="grey", fg="white")
clear_button.pack(pady=5)

# Run Tkinter main loop
root.mainloop()
