"""The Wikipedia Game

How many clicks to Hitler?
https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game

Still totally broken."""

import tkinter as tk
import tkinter.messagebox as tkmb
import wikipedia as wp
import random

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.current_page = None
        self.num_of_clicks = 0

    def createWidgets(self):
        """Create all essential widgets."""
        self.control_group = tk.Frame(self)
        
        self.start_button = tk.Button(self.control_group)
        self.start_button['text'] = 'New Game'
        self.start_button['command'] = self.newGame
        self.start_button.pack(side='top')

        self.links_button = tk.Button(self.control_group)
        self.links_button['text'] = 'Print Links'
        self.links_button['command'] = self.printLinks
        self.links_button.pack(side='top')

        self.QUIT = tk.Button(self.control_group, text='QUIT', fg='red',
                              command=root.destroy)
        self.QUIT.pack(side='bottom')
        
        self.control_group.pack(side='right')

        self.link_group = tk.Frame(self)
        self.link_group.pack(side='right')

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill=tk.Y)
        self.scrollbar.config(command=self.link_group.yview)

        self.link_group.config(yscrollcommand=self.scrollbar.set)

    def newGame(self):
        """Start a new game"""

        random_title = wp.random()

        self.followLink(random_title)

        

    def printLinks(self):
        for link in self.current_page.links:
            print(link)

    def followLink(self, title):
        for i in range(100):
            try:
                self.current_page = wp.page(title=title)
                break
            except wp.exceptions.DisambiguationError as e:
                tkmb.showerror(str(type(e)), str(e))
                title = random.choice(e.options)
                self.current_page = wp.page(title)
                print('DisambiguationError handled')
                break
            except Exception as e:
                tkmb.showerror(str(type(e)), str(e))

        print(self.current_page.title)

        self.createLinkButtons()
        
    def createLinkButtons(self):
        for slave in self.link_group.slaves():
            slave.destroy()
        for link in self.current_page.links:
            print(link)
            new_button = tk.Button(self.link_group, text=link,
                                   command=(lambda: self.followLink(link)))
            new_button.pack()
        self.link_group.pack(fill=tk.BOTH, expand=1)


def main():
    global root
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
