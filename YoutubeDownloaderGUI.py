"""
Name: Pavishanan Surenthiran 
Date: 2021-01-27 (Last Modified: 2021-02-01)
Description: Attempting to build a Youtube Video Downloader 
"""
# Various imports for this program to work 
import os # These modules allows us to manipulate files and directories.
import sys # Same as the os module import 
import tkinter as tk # Main tkinter import 
from io import BytesIO # This converts url images to a usuable image object 
from pytube import YouTube # main Youtube downloader module we'll be using 
from datetime import timedelta # Allows us to convert Youtube date format to a usuable string
from PIL import Image, ImageTk # Allows us to display the custom Youtube logo as well as the Youtube thumbnail
from urllib.request import urlopen # Opens the youtube thumbnail url and access it

# Main Youtube class we'll be using to create the GUI
class YoutubeGUI:
    """Youtube GUI Object Class"""

    def __init__(self):
        """Initializing the attributes"""
        # Styling the program 
        self.WIN_Size = "500x600" # I put the custom window size I wanted in a variable 
        self.BG_Colour = "#161616" # Custom background colour hex
        self.General_Colour = "White" # General colour for things like text
        self.Switch = False # This switch activates the corresponding youtube thumbnail if a link is entered, else my logo
        self.tk_window = tk.Tk() # Creating an instance of Tk()
        self.tk_canvas = tk.Canvas(self.tk_window, width=500, height=550, bg=self.BG_Colour, highlightthickness=0) # This canvas allows us to position the entry bar to where ever I like
        self.tk_window.title("Youtube Video Downloader") # Setting the title for the GUI bar (top bar) 
        self.tk_window.configure(background=self.BG_Colour) # Configuring the background colour with the custom colour I stored in the variable earlier 
        self.tk_canvas.configure(background=self.BG_Colour) # Configuring the canvas background colour with the custom colour I stored in the variable earlier

        # Making adjustments to the main window 
        self.tk_window.geometry(self.WIN_Size) # Custom window size 
        self.tk_window.resizable(width=False, height=False) # Locking the window's dimensions disabling users to resize it 
        
        # Creating the entry bar and whatnot
        self.tk_entry = tk.Entry(self.tk_window, bg="Red", font=("Arial", 20)) # Created the entry link with custom values
        self.tk_canvas.create_window(250,533,window=self.tk_entry, width="400", height="40") # Putting the entry bar on the canvas 

        # The bottom text below the entry bar promoting the user how to use the entry bar  
        self.label_TITLE = tk.Label(self.tk_window, text="Press enter to download", bg=self.BG_Colour, fg=self.General_Colour)
        self.label_TITLE.config(font=("Courier", 11))
        self.label_TITLE.place(x=47,y=555)

        # ---- Thumbnail ----
        logo = "logo.png" # File name that has my custom logo 
        img_path = os.path.join(os.path.join(sys.path[0], logo)) # Joining current directory with logo to create one whole path 
        pic = Image.open(img_path) # Using the combined path, I made an image object so it can be used in label
        pic = pic.resize((400,225), Image.ANTIALIAS) # Resizing the picture so it won't be overblow and too small 
        picture = ImageTk.PhotoImage(pic) # Finally I can use the image. I've stored it into the 'picture' variable 

        # Making the the thumbnail 
        label_TL = tk.Label(self.tk_window, image=picture, bd=0) # Creating the thumbnail label 
        label_TL.place(x=50,y=20) # Position the label to where I want it to be 

        # ---- Description ----
        self.Display_Video_Description() # Displays 'offline' values in the description 
        self.tk_window.bind('<Return>',self.Update_Events) # This listens for a key press, specifically     
                                                           # the enter key. When pressed, will activate 
                                                           # corresponding function which in this case is 'self.Update_Evenets'.
        # ---- Extras ----
        self.tk_canvas.pack() # Packing the canvas
        tk.mainloop() # Starting the mainloop

    def Update_Events(self, event="None"):
        """Activates the functions housed inside this function when the enter key is pressed. 
           I did this because you can't activate more than one function at a time. I found a solution 
           by just creating one function, that activates the other functions."""
        # Updating Main GUI
        self.Update_Description() # Updates the description 
        self.Activate_Switch() # Switches the boolean value in self.Activate_Switch() from False to True 
        self.Update_Youtube_Thumbnail(switch=self.Switch) # Updates the thumbnail with the Youtube videos thumbnail 
    
    def Display_Video_Description(self):
        """This Function shows the description of the video. I put this into a function because the __init__
           would be too long.""" 
    
        # Top Breaker Line 
        self.Breaker_Bottom = tk.Label(self.tk_window, text="———————————————————", bg=self.BG_Colour, fg="Red")
        self.Breaker_Bottom.config(font=("Arial", 16))
        self.Breaker_Bottom.place(x=47,y=280)
        
        # Youtube Title Text
        self.YT_Title = tk.Label(self.tk_window, text="Welcome — enter the link to begin", bg=self.BG_Colour, fg=self.General_Colour)
        self.YT_Title.config(font=("Times New Roman", 18))
        self.YT_Title.place(x=47,y=253)

        # Youtube Creator Text
        self.YT_Creator = tk.Label(self.tk_window, text="The Creator: Offline", bg=self.BG_Colour, fg=self.General_Colour)
        self.YT_Creator.config(font=("Times New Roman", 18))
        self.YT_Creator.place(x=47,y=305)
       
        # Total Views Text
        self.YT_Views = tk.Label(self.tk_window, text="Total Views: Offline", bg=self.BG_Colour, fg=self.General_Colour)
        self.YT_Views.config(font=("Times New Roman", 18))
        self.YT_Views.place(x=47,y=347)

        # Video Length Text 
        self.YT_Length = tk.Label(self.tk_window, text="Video Length: Offline", bg=self.BG_Colour, fg=self.General_Colour)
        self.YT_Length.config(font=("Times New Roman", 18))
        self.YT_Length.place(x=47,y=387)

        # Published Date Text
        self.YT_Publish = tk.Label(self.tk_window, text="Published Date: Offline", bg=self.BG_Colour, fg=self.General_Colour)
        self.YT_Publish.config(font=("Times New Roman", 18))
        self.YT_Publish.place(x=47,y=430)

        # Bottom Breaker Line 
        self.Breaker_Bottom = tk.Label(self.tk_window, text="———————————————————", bg=self.BG_Colour, fg="Red")
        self.Breaker_Bottom.config(font=("Arial", 16))
        self.Breaker_Bottom.place(x=47,y=455)

        # Download Text 
        self.YT_Download = tk.Label(self.tk_window, text="Downloads — None", bg=self.BG_Colour, fg=self.General_Colour)
        self.YT_Download.config(font=("Times New Roman", 14))
        self.YT_Download.place(x=47,y=480)
        
    def Activate_Switch(self):
        """Changes self.Switch value to True"""
        # Prints this message in the command prompt 
        print("Switch Activated")

        # Assigning True boolean value 
        self.Switch = True 

    def Update_Description(self):
        """This function updates the description from the given link when the enter keys is pressed"""
        # Prints this message in the command prompt so I know it's been pressed
        print("Enter key registerd")

        # Getting the link from the user using .get()
        link = str(self.tk_entry.get()) 
        yt = YouTube(link) # Putting that link into the YouTube class for later use
        print(yt.title) # Prints the Youtube video in the command prompt so I know its working
        print("By:",yt.author)
        print("\n")
        
        # When the enter key is triggered, the corresponding information is gonna be updated
        # Title Text -- the if statement determines how long the string is, if longer than 25 characters, cut it off, else continue.
        if len(yt.title)>25:
            Cut_Title = yt.title[:35]+"..." # Using string manipulation techniques to cut it off and join it with the string '...' so the user knows its been cut off.
            self.YT_Title.config(text=Cut_Title) # Only way to dynamically update the text is by using the .config() method. 
            self.YT_Title.place(x=47,y=253) # placing the text in its original place 
        elif len(yt.title)<=25: # If less or equal, uses original string 
            self.YT_Title.config(text=yt.title) # Same process
            self.YT_Title.place(x=47,y=253) # Same process 

        # Creator Text -- for the most part, this is the same technique I used when updating the title, but now for the author.
        if len(yt.author)>10: 
            Cut_Creator = yt.author[:10]+"..."
            self.YT_Creator.config(text="The Creator: "+Cut_Creator)
            self.YT_Creator.place(x=47,y=307)
        elif len(yt.author)<=25:
            self.YT_Creator.config(text="The Creator: "+yt.author)
            self.YT_Creator.place(x=47,y=307)

        # Total Views Text
        self.YT_Views.config(text="Total Views: {:,}".format(yt.views)) # Easiest way to put a comma between every 3 numbers.
        self.YT_Views.place(x=47,y=347)

        # Video Length Text
        self.YT_Length.config(text="Video Length: "+str(timedelta(seconds=yt.length))) # Converting datetime format to a usuable string
        self.YT_Length.place(x=47,y=387)

        # Published Date Text
        self.YT_Publish.config(text="Published Date: {:%d %b, %Y}".format(yt.publish_date)) # Formatting the published date 
        self.YT_Publish.place(x=47,y=430)

    def Update_Youtube_Thumbnail(self, switch):
        """This function has a switch parameter. If false, won't change/update Youtube thumbnail, else will update it"""
        # Shows youtube thumbnail when link registered
        print("switch is",self.Switch) # Printing this in the command prompt so I know this function works 
        if self.Switch==True:
            # Getting the link from the user 
            link = str(self.tk_entry.get()) # Getting the link from entry bar
            yt = YouTube(link) # Creating a YouTube instance with link in it.

            # Going to thumbnail URL
            url = urlopen(yt.thumbnail_url) # I'm going to open the url to the image
            raw_data = url.read() # Read the data from the image I've got and store it into a variable for later use 
            url.close() # Then I'm going to close the process 
            
            # Forming the data into an image 
            img = Image.open(BytesIO(raw_data)) # Processing the raw data into an image type 
            img = img.resize((397,222), Image.ANTIALIAS) # Resizing the image 
            photo = ImageTk.PhotoImage(img) # Finalizing the image. It's now a usuable image object inside the photo object 

            # Creating it into a label
            label_TL = tk.Label(self.tk_window, image=photo, bd=0) 
            label_TL.image = photo  
            label_TL.place(x=52,y=22)
    
    def Download_Video(self, count):
        """Downloads the video from the link gathered from the user. Uses the Pytube library to accomplish this"""
        # Gets the link
        yt = YouTube(str(self.tk_entry.get()))

        # Downloads the video
        yt.streams.first().download() 
        # This is quite simple but it downloads the highest quality 'progessive' 
        # stream first, which is 720p or lower sometimes. Youtube uses 'dash' streams 
        # which in short is a combination of the highest quality audio file and the 
        # highest quality video file merged together. I could make the video quality higher, 
        # but I would have to code a lot more to to somehow combine two files together to 
        # create a singular file which during the process, involves file manipulation and researching a whole  
        # nother' module for this work. At that point, it isn't worth doing since this is already 
        # enough for this project and doing more won't provide any real benifts to my mark. 
        # Thus I ended up using a 'progressive' file download which gives me both audio and video
        # joined together ready for me to use without anything to add. 

# Creating the class instance 
yt_guiapp = YoutubeGUI()