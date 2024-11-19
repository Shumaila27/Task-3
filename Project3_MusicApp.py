from tkinter import filedialog  # Import the filedialog module from tkinter for folder/file selection
from tkinter import *  # Import all necessary components from the tkinter library to create GUI elements
import pygame  # Import pygame library to handle music playback
import os  # Import the os library to interact with the file system (e.g., get file paths)

# Create the main window for the music player
root = Tk()  # Initialize the Tkinter window
root.title("Music Player")  
root.geometry("500x300")  # Set the dimensions of the window (500 pixels wide, 300 pixels tall)
root.configure(bg="white")  # Set the background color of the window to white

# Initialize the pygame mixer to handle audio playback
pygame.mixer.init()  # This prepares the pygame mixer module for playing music

# Create a menu bar to allow users to select options (e.g., choose a folder)
menubar = Menu(root, bg="orange", fg="black")  # Create a menu bar with orange background and black text
root.config(menu=menubar)  # Attach the menu bar to the main window

# List to store song names, and variables to track the currently playing song and whether it's paused
songs = []  # An empty list to hold the song names from the selected folder
current_song = ""  # Variable to store the name of the current song that is playing
paused = False  # Boolean value to track if the song is paused or playing


def load_music():
    global current_song 
    root.directory = filedialog.askdirectory()  # Open a dialog to select a folder where music is stored
    songs.clear()  # Clear the previously loaded songs from the song list
    songlist.delete(0, END)  # Clear any previous song names displayed in the listbox

    # Loop through each file in the selected folder
    for song in os.listdir(root.directory):  # os.listdir gets all files in the folder
        name, ext = os.path.splitext(song)  # Split each file into a name and extension
        if ext == '.mp3':  # Check if the file is an MP3 (our target file type)
            songs.append(song)  # Add the song name to the list of songs

    # Insert all the song names into the listbox to display them
    for song in songs:
        songlist.insert("end", song)  # Insert each song into the listbox at the end

    # If there are songs in the list, set the first song as the default selection
    if songs:
        songlist.selection_set(0)  # Automatically select the first song in the list
        current_song = songs[songlist.curselection()[0]]  # Set the current song to the first one
        update_now_playing(current_song)  # Update the "Now Playing" label with the song name

# Function to update the "Now Playing" label with the currently playing song's name
def update_now_playing(song):
    now_playing_label.config(text=f"Now Playing: {song}")  # Update the label with the song name

# Function to play or resume the selected song
def play_music():
    global current_song, paused  # Allow modification of the current_song and paused variables
    if paused:  # If the song is currently paused, unpause it
        pygame.mixer.music.unpause()  # Resume playback
        paused = False  # Set the paused state to False
    else:  # If the song isn't paused, load and play the selected song
        pygame.mixer.music.load(os.path.join(root.directory, current_song))  # Load the song file
        pygame.mixer.music.play()  # Play the loaded song
        update_now_playing(current_song)  # Update the "Now Playing" label with the song name

# Function to pause the current song
def pause_music():
    global paused  # Allow modification of the paused variable
    if not paused:  # If the song is not already paused, pause it
        pygame.mixer.music.pause()  # Pause the song
        paused = True  # Set the paused state to True
    else:  # If the song is already paused, unpause it
        pygame.mixer.music.unpause()  # Unpause the song
        paused = False  # Reset the paused state to False

# Function to play the next song in the playlist
def next_music():
    global current_song, paused  # Allow modification of the current_song and paused variables
    try:
        paused = False  # Ensure that the next song starts from the beginning (not paused)
        current_index = songs.index(current_song)  # Find the index of the current song in the list
        if current_index < len(songs) - 1:  # Check if there is a next song
            songlist.selection_clear(0, END)  # Deselect the current song in the list
            songlist.selection_set(current_index + 1)  # Select the next song in the list
            current_song = songs[current_index + 1]  # Update the current song to the next one
            play_music()  # Play the next song
    except Exception as e:
        print(f"Error in next_music: {e}")  # Print an error message if something goes wrong

# Function to play the previous song in the playlist
def prev_music():
    global current_song, paused  # Allow modification of the current_song and paused variables
    try:
        paused = False  # Ensure that the previous song starts from the beginning (not paused)
        current_index = songs.index(current_song)  # Find the index of the current song in the list
        if current_index > 0:  # Check if there is a previous song
            songlist.selection_clear(0, END)  # Deselect the current song in the list
            songlist.selection_set(current_index - 1)  # Select the previous song in the list
            current_song = songs[current_index - 1]  # Update the current song to the previous one
            play_music()  # Play the previous song
    except Exception as e:
        print(f"Error in prev_music: {e}")  # Print an error message if something goes wrong

# Menu to organize and load songs from a folder
organise_menu = Menu(menubar, tearoff=False, bg="orange", fg="orange")  # Create a submenu for folder selection
organise_menu.add_command(label="Select Folder", command=load_music)  # Add the "Select Folder" command
menubar.add_cascade(label="Select Menu", menu=organise_menu)  # Attach the submenu to the menu bar

# Display the "Now Playing" label with black text on white background
now_playing_label = Label(root, text="Now Playing: ", fg="black", bg="white", font=("Helvetica", 12, "bold"))
now_playing_label.pack(pady=10)  # Add the label to the window and add some padding

# Create a listbox to display the songs from the folder with black background and white text
songlist = Listbox(root, bg="black", fg="white", selectbackground="orange", width=70, height=10)
songlist.pack(pady=10)  # Add the listbox to the window with some padding

# Load images for control buttons (play, pause, next, previous)
# In case the images are not found, placeholders will be used instead
try:
    play_btn_image = PhotoImage(file="play.png")  # Try to load the play button image
except:
    play_btn_image = None  # If the image is not found, set it to None

try:
    pause_btn_image = PhotoImage(file="pause.png")  # Try to load the pause button image
except:
    pause_btn_image = None

try:
    next_btn_image = PhotoImage(file="next.png")  # Try to load the next button image
except:
    next_btn_image = None

try:
    prev_btn_image = PhotoImage(file="previous.png")  # Try to load the previous button image
except:
    prev_btn_image = None

# Frame to hold the control buttons with a white background
control_frame = Frame(root, bg="white")  # Create a frame for the control buttons
control_frame.pack(pady=20)  # Add the frame to the window with some padding

# Create control buttons with fallback text if images are missing
prev_btn = Button(control_frame, image=prev_btn_image, compound=LEFT, borderwidth=0, command=prev_music, bg="orange", fg="black")
play_btn = Button(control_frame, image=play_btn_image, compound=LEFT, borderwidth=0, command=play_music, bg="orange", fg="black")
pause_btn = Button(control_frame, image=pause_btn_image, compound=LEFT, borderwidth=0, command=pause_music, bg="orange", fg="black")
next_btn = Button(control_frame, image=next_btn_image, compound=LEFT, borderwidth=0, command=next_music, bg="orange", fg="black")

# Arrange the buttons in a grid within the control frame
prev_btn.grid(row=0, column=0, padx=10)  # Place the previous button in the first column
play_btn.grid(row=0, column=1, padx=10)  # Place the play button in the second column
pause_btn.grid(row=0, column=2, padx=10)  # Place the pause button in the third column
next_btn.grid(row=0, column=3, padx=10)  # Place the next button in the fourth column

# Start the Tkinter GUI main loop
root.mainloop()  # This will display the window and handle user interactions
