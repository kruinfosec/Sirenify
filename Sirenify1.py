from tkinter import *
from tkinter import filedialog
import pygame
import os
from PIL import ImageTk

class Sirenify:
    def __init__(self, root):
        self.root = root
        self.root.title('Sirenify')
        self.root.geometry('500x300')

        pygame.mixer.init()

        self.songs = []
        self.current_song = ""
        self.paused = False

        self.create_widgets()

    def create_widgets(self):
        # Create a listbox for displaying songs
        self.songlist = Listbox(self.root, bg='black', fg='green', height=45, width=240)
        self.songlist.pack()

        # Create a menubar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Create a "File" menu in the menubar
        organise_menu = Menu(menubar, tearoff=False)
        organise_menu.add_command(label='Open a Playlist', command=self.load_music)
        menubar.add_cascade(label='File', menu=organise_menu)

        # Load images for buttons
        play_img = ImageTk.PhotoImage(file='play.png')
        pause_img = ImageTk.PhotoImage(file='pause.png')
        back_img = ImageTk.PhotoImage(file='back.png')
        forward_img = ImageTk.PhotoImage(file='forward.png')
        repeat_img = ImageTk.PhotoImage(file='repeat.png')

        # Create a frame for control buttons
        control_frame = Frame(self.root)
        control_frame.pack()

        # Create buttons with corresponding images and commands
        play_btn = Button(control_frame, image=play_img, borderwidth=0, command=self.play_music)
        pause_btn = Button(control_frame, image=pause_img, borderwidth=0, command=self.pause_music)
        back_btn = Button(control_frame, image=back_img, borderwidth=0, command=self.prev_music)
        forward_btn = Button(control_frame, image=forward_img, borderwidth=0, command=self.next_music)
        repeat_btn = Button(control_frame, image=repeat_img, borderwidth=0)

        # Grid layout for buttons
        play_btn.grid(row=0, column=1, padx=7, pady=10)
        pause_btn.grid(row=0, column=2, padx=7, pady=10)
        back_btn.grid(row=0, column=0, padx=7, pady=10)
        forward_btn.grid(row=0, column=3, padx=7, pady=10)
        repeat_btn.grid(row=0, column=4, padx=7, pady=10)

    def load_music(self):
        # Reset variables
        self.current_song = ""
        self.paused = False

        # Ask user to select a directory
        self.root.directory = filedialog.askdirectory()

        # Iterate over files in the selected directory
        for song in os.listdir(self.root.directory):
            name, ext = os.path.splitext(song)
            if ext == '.mp3':
                self.songs.append(song)

        # Display songs in the listbox
        for song in self.songs:
            self.songlist.insert('end', song)

        # Select the first song in the list
        self.songlist.selection_set(0)
        self.current_song = self.songs[self.songlist.curselection()[0]]

    def play_music(self):
        if not self.paused:
            # Load and play the selected song
            pygame.mixer.music.load(os.path.join(self.root.directory, self.current_song))
            pygame.mixer.music.play()
        else:
            # Unpause the music if paused
            pygame.mixer.music.unpause()
            self.paused = False

    def pause_music(self):
        # Pause the music
        pygame.mixer.music.pause()
        self.paused = True

    def next_music(self):
        try:
            # Select the next song in the list
            self.songlist.select_clear(0, END)
            self.songlist.selection_set(self.songs.index(self.current_song) + 1)
            self.current_song = self.songs[self.songlist.curselection()[0]]
            self.play_music()
        except IndexError:
            pass

    def prev_music(self):
        try:
            # Select the previous song in the list
            self.songlist.selection_clear(0, END)
            self.songlist.selection_set(self.songs.index(self.current_song) - 1)
            self.current_song = self.songs[self.songlist.curselection()[0]]
            self.play_music()
        except IndexError:
            pass

if __name__ == "__main__":
    root = Tk()
    app = Sirenify(root)
    root.mainloop()
