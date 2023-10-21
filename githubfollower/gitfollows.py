import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import math

# Create the main GUI window
root = tk.Tk()
root.title("GitHub Statistics and Unfollower Tool")
root.geometry("540x530")  
root.resizable(False, False)
base_url = 'https://api.github.com'


bg_color = "#1A1C23"  # Background color
fg_color = "#C0CAF5"  # Foreground color (text color)
label_bg_color = "#1E2029"  # Label background color
button_bg_color = "#34353E"  # Button background color
entry_bg_color = "#34353E"  # Entry background color
entry_fg_color = "#C0CAF5"  # Entry text color

# Create a frame as the background
background_frame = tk.Frame(root, bg=bg_color)
background_frame.place(x=0, y=0, relwidth=1, relheight=1)

# Function to draw the wave animation
def draw_wave():
    canvas.delete("wave")  
    x_start = 0

    while x_start < 540:
        y = 305 + 10 * math.sin((x_start / 20) - phase)
        canvas.create_line(x_start, y, x_start + 1, y, fill="#C0CAF5", tags="wave", width=22)
        x_start += 1


def update_wave_animation():
    global phase
    draw_wave()
    phase += 0.05
    root.after(50, update_wave_animation)  

phase = 0

canvas = tk.Canvas(background_frame, width=540, height=530, bg=bg_color)
canvas.grid(row=0, column=0, rowspan=7, columnspan=4, sticky="nsew",pady=(5, 0))

background_rectangle = canvas.create_rectangle(0, 305, 540, 530, fill="#C0CAF5")



root.after(100, update_wave_animation)

def fetch_user_info():
    username = username_entry.get()
    token = token_entry.get()

    if not username or not token:
        messagebox.showerror("Error", "Please enter both a username and a token.")
        return

    user_url = f'{base_url}/users/{username}'
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        followers = user_data['followers']
        public_repos = user_data['public_repos']

       
        stars = get_stars_count(username, token)

       
        followers_label.config(text=f"Followers: {followers}")
        repos_label.config(text=f"Repositories: {public_repos}")
        stars_label.config(text=f"Stars: {stars}")

        rate_limit, remaining_requests = get_rate_limit(username, token)
        if rate_limit is not None and remaining_requests is not None:
            rate_limit_label.config(text=f"Rate Limit: {rate_limit}")
            remaining_requests_label.config(text=f"Remaining Requests: {remaining_requests}")
    else:
        messagebox.showerror("Error", "Failed to fetch user data.")

def get_stars_count(username, token):
    headers = {
        'Authorization': f'token {token}'
    }
    repos_url = f'{base_url}/users/{username}/repos'
    response = requests.get(repos_url, headers=headers)
    if response.status_code == 200:
        repos_data = response.json()
        stars_count = sum(repo['stargazers_count'] for repo in repos_data)
        return stars_count
    return 0

def get_rate_limit(username, token):
    headers = {
        'Authorization': f'token {token}'
    }
    rate_limit_url = 'https://api.github.com/rate_limit'
    response = requests.get(rate_limit_url, headers=headers)
    if response.status_code == 200:
        rate_limit_data = response.json()
        rate_limit = rate_limit_data['resources']['core']['limit']
        remaining_requests = rate_limit_data['resources']['core']['remaining']
        return rate_limit, remaining_requests
    return None, None


def unfollow_user(username, token):
    unfollow_url = f'https://api.github.com/user/following/{username}'

    headers = {
        'Authorization': f'token {token}',
    }

    response = requests.delete(unfollow_url, headers=headers)

    if response.status_code == 204:
        print(f"Unfollowed {username}.")
    else:
        print(f"Failed to unfollow {username} with status code {response.status_code}.")

def check_and_unfollow_non_followers():
    username = username_entry.get() 
    token = token_entry.get()
    if not username:
        messagebox.showerror("Error", "Please enter a valid username.")
        return

    followers_url = f'{base_url}/users/{username}/followers'
    following_url = f'{base_url}/users/{username}/following'
    headers = {
        'Authorization': f'token {token}'
    }

    followers_response = requests.get(followers_url, headers=headers)
    if followers_response.status_code == 200:
        followers = [user['login'] for user in followers_response.json()]
    else:
        messagebox.showerror("Error", "Failed to fetch followers.")
        return

    response = requests.get(following_url, headers=headers)
    if response.status_code == 200:
        following = [user['login'] for user in response.json()]
    else:
        messagebox.showerror("Error", "Failed to fetch users you are following.")
        return

    not_following_back = [user for user in following if user not in followers]

    response = messagebox.askquestion("Unfollow Non-Followers", "Do you want to unfollow non-followers?")
    if response == "yes":
        for user_to_unfollow in not_following_back:
            unfollow_user(user_to_unfollow, token)
        messagebox.showinfo("Unfollowed", f"Unfollowed {len(not_following_back)} non-followers.")


root.configure(bg=bg_color)


original_image = Image.open("github-mark-white.png") 
resized_image = original_image.resize((100, 100))  
octocat_image = ImageTk.PhotoImage(resized_image)
octocat_label = tk.Label(root, image=octocat_image, bg=bg_color)
octocat_label.image = octocat_image
octocat_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


title_label = tk.Label(root, text="GitHub Statistics and Unfollower Tool", font=("Helvetica", 16), fg=fg_color, bg=bg_color)
title_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

username_label = tk.Label(root, text="Enter GitHub Username:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
username_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

username_entry = ttk.Entry(root, style="Custom.TEntry", foreground=entry_fg_color)
username_entry.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

token_label = tk.Label(root, text="Enter Personal Access Token:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
token_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

token_entry = ttk.Entry(root, style="Custom.TEntry", show="*", foreground=entry_fg_color)
token_entry.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

commit_streak_label = tk.Label(root, text="Commit Streak: 0", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
commit_streak_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

followers_label = tk.Label(root, text="Followers: 0", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
followers_label.grid(row=4, column=1, padx=5, pady=10, sticky="w")

repos_label = tk.Label(root, text="Repositories: 0", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
repos_label.grid(row=4, column=2, padx=5, pady=10, sticky="w")

stars_label = tk.Label(root, text="Stars: 0", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
stars_label.grid(row=4, column=3, padx=10, pady=10, sticky="w")

fetch_button = ttk.Button(root, text="Fetch User Info", command=fetch_user_info, style="Custom.TButton")
fetch_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

unfollow_button = ttk.Button(root, text="Unfollow Non-Followers", command=check_and_unfollow_non_followers, style="Custom.TButton")
unfollow_button.grid(row=6, column=0, columnspan=4, padx=10, pady=10)



style = ttk.Style()
style.configure("Custom.TButton", background=button_bg_color)
style.configure("Custom.TEntry", fieldbackground=entry_bg_color)

root.mainloop()
