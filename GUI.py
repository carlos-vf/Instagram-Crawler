# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, ttk

import instagram_crawler as ic
      
###############################################################################
################################## LOGIN ######################################
###############################################################################

def show_login_window():
    
    def show_login():
        
        user = username_entry.get()
        password = password_entry.get()
        
        try:
            
            ic.instagram_login(user, password)
            messagebox.showinfo("Login Successful", f"Welcome {user}!")
            root.destroy()  # Close the login window
            show_main_window()
            
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))   
            
    
    # Create the main window
    root = tk.Tk()
    root.title("Login")
    
    # Create a frame for the username and password fields
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)
    
    # Add a label and entry for the username
    username_label = tk.Label(frame, text="Username")
    username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1, pady=5)
    
    # Add a label and entry for the password
    password_label = tk.Label(frame, text="Password")
    password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
    password_entry = tk.Entry(frame, show="*")
    password_entry.grid(row=1, column=1, pady=5)
    
    # Add a login button
    login_button = tk.Button(frame, text="Login", command=show_login)
    login_button.grid(row=2, columnspan=2, pady=10)
    
    # Run the application
    root.mainloop()
    
    
    

###############################################################################
################################## MAIN #######################################
###############################################################################

def show_main_window(user='self'):  
    
    try:
        global profile
        profile = ic.get_profile(user)
        
    except Exception as e:
        messagebox.showerror("Failed at getting profile", str(e))   
        
    
    # Create a new window
    info_window = tk.Tk()
    info_window.title("Instagram Account Info")

    # Create a frame for account info
    info_frame = tk.Frame(info_window, padx=10, pady=10)
    info_frame.pack(padx=10, pady=10)

    # Display account info
    username_label = tk.Label(info_frame, text=f"Username: {profile.username}")
    username_label.grid(row=0, column=0, sticky=tk.W, pady=5)

    full_name_label = tk.Label(info_frame, text=f"Full Name: {profile.full_name}")
    full_name_label.grid(row=1, column=0, sticky=tk.W, pady=5)

    followers_label = tk.Label(info_frame, text=f"Followers: {profile.followers}")
    followers_label.grid(row=2, column=0, sticky=tk.W, pady=5)

    following_label = tk.Label(info_frame, text=f"Following: {profile.followees}")
    following_label.grid(row=3, column=0, sticky=tk.W, pady=5)

    posts_label = tk.Label(info_frame, text=f"Number of Posts: {profile.mediacount}")
    posts_label.grid(row=4, column=0, sticky=tk.W, pady=5)

    # Create buttons
    not_following_button = tk.Button(info_frame, text="Get Unfollowers", command=not_following_action)
    not_following_button.grid(row=5, column=0, pady=10)

    new_unfollowers_button = tk.Button(info_frame, text="New Unfollowers", command=new_unfollowers_action)
    new_unfollowers_button.grid(row=6, column=0, pady=10)
    
    another_account_button = tk.Button(info_frame, text="See Another Account Details", command=lambda: see_another_account(info_window))
    another_account_button.grid(row=7, column=0, pady=10)

    # Create a scrollable frame for detailed data
    create_scrollable_frame(info_window)
 
    
 
def not_following_action():
    """Action for 'Not Following Me' button."""
    not_following_back = ic.get_non_followers(profile)
    print(not_following_back)
    
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    for i, user in enumerate(not_following_back, start=1):
        label = tk.Label(scrollable_frame, text=user)
        label.pack(anchor="w", pady=2)
    
    
def new_unfollowers_action():
    """Action for 'New Unfollowers' button."""
    messagebox.showinfo("New Unfollowers", "Not implemented")


def create_scrollable_frame(parent):
    """Create a scrollable frame for displaying detailed data."""
    global scrollable_frame

    container = ttk.Frame(parent)
    container.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")
    
    

###############################################################################
############################# ANOTHER ACCOUNT #################################
###############################################################################

def see_another_account(parent):
    """Open a new window to enter another account username."""
    parent.destroy()
    
    global another_account_window
    another_account_window = tk.Tk()
    another_account_window.title("See Another Account Details")

    # Create a frame for entering the username
    frame = tk.Frame(another_account_window, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    username_label = tk.Label(frame, text="Username")
    username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1, pady=5)

    search_button = tk.Button(frame, text="Search", command=lambda: search_account(username_entry.get(), another_account_window))
    search_button.grid(row=1, columnspan=2, pady=10)    
    
    
def search_account(user, another_account_window):
    """Search for another account and display its details."""
    try:
        another_account_window.destroy()  # Close the login window
        show_main_window(user)
    except Exception as e:
        messagebox.showerror("Failed at getting profile", str(e))   
        
        
show_login_window()