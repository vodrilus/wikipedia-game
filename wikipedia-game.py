"""The Wikipedia Game

How many clicks to Hitler?
https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game"""

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
        self.start_button = tk.Button(self)
        self.start_button['text'] = 'New Game'
        self.start_button['command'] = self.newGame
        self.start_button.pack(side='top')

        self.links_button = tk.Button(self)
        self.links_button['text'] = 'Print Links'
        self.links_button['command'] = self.printLinks
        self.links_button.pack(side='top')

        self.QUIT = tk.Button(self, text='QUIT', fg='red',
                              command=root.destroy)
        self.QUIT.pack(side='bottom')

    def newGame(self):
        for i in range(100):
            try:
                #title = wp.random()
                title = 'JMF'
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

    def printLinks(self):
        for link in self.current_page.links:
            print(link)
        
    def createLinkButtons(self, links):
        for l in links:
            tk.Button()


def main():
    global root
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
