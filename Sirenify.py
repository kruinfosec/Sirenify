from tkinter import * #'*' is to import all the tkinter modules 6
from tkinter import filedialog #To access all file from machine
import pygame
import os
from PIL import ImageTk, Image
#PIL function is use so that jpg files can be read, by default png can be read by PhotoImage function

root = Tk() #initialising tkinter to star our programme. root is basically our window here
root.title('Sirenify') #to set title
root.geometry('500x300')

pygame.mixer.init() #initialising pygame music mixer to allow us to play audio

#Global Variables used
songs = []
current_song = ""
paused = False

#Function for add music
def load_music():
    global current_song #setting current song as a global variable
    root.directory = filedialog.askdirectory()
    
    #interating over files in our directiory, chosen by us and splitting file name into file name and its extension, if its mp3 then song is added to the list
    for song in os.listdir(root.directory):
        name,ext = os.path.splitext(song)
        if ext == '.mp3' :
            songs.append(song)
    #showcasing songs from playlist in our software under song list
    for song in songs:
        songlist.insert('end',song)
        
    songlist.selection_set(0) #selects the fist song from the list
    current_song = songs[songlist.curselection()[0]] #sets the selected song to be current song

#Giving player's buttons functionality    
def play_music():
    global current_song, paused
    
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory,current_song)) #join the current song name and the directory chosen and load them 
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused
    #using try and except so that if their is no next song then it do not give us any error
    try:
        songlist.select_clear(0,END)  #removing any selected music from 0 to the end of the songlist
        songlist.selection_set(songs.index(current_song)+1) #moving selection by 1 in the song list
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass
    
def prev_music(): #opposite of play function
    global current_song, paused
    
    try:
        songlist.selection_clear(0,END)
        songlist.selection_set(songs.index(current_song)-1) 
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

songlist = Listbox(root, bg='black', fg='green', height=45, width=240)
songlist.pack() #pack.() adds songlist to the window

#creating a menubar
menubar = Menu(root)
root.config(menu=menubar) #sets root window's menu bar equal to our menu bar(mentioned above)

#organizing our menubar
organise_menu = Menu(menubar,tearoff=False)
organise_menu.add_command(label='Open a Playlist',command=load_music)
menubar.add_cascade(label='File',menu=organise_menu)

#"PhotoImage()" function returns the image object
play_img = ImageTk.PhotoImage(file ='play.jpg')
pause_img = ImageTk.PhotoImage(file ='pause.jpg')
back_img = ImageTk.PhotoImage(file ='back.jpg')
forward_img = ImageTk.PhotoImage(file ='forward.jpg')
repeat_img = ImageTk.PhotoImage(file ='repeat.jpg')

#Creating space for to add widgets
control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image = play_img, borderwidth=0,command=play_music )
pause_btn = Button(control_frame, image = pause_img, borderwidth=0,command=pause_music)
back_btn = Button(control_frame, image = back_img, borderwidth=0,command=prev_music)
forward_btn = Button(control_frame, image = forward_img, borderwidth=0,command=next_music)
repeat_btn = Button(control_frame, image = repeat_img, borderwidth=0,)

# grid() method allows you to indicate the row and column positioning in its parameter list. Both row and column start from index 0.
play_btn.grid(row=0,column=1,padx=7,pady=10)
pause_btn.grid(row=0,column=2,padx=7,pady=10)
back_btn.grid(row=0,column=0,padx=7,pady=10)
forward_btn.grid(row=0,column=3,padx=7,pady=10)
repeat_btn.grid(row=0,column=4,padx=7,pady=10)

root.mainloop() #runs our code