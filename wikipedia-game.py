"""The Wikipedia Game

How many clicks to Hitler?
https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game

No win condition yet."""

import tkinter as tk
import tkinter.messagebox as tkmb
import wikipedia as wp
import random

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.current_page = None
        self.pack()
        self.createWidgets()
        
        self.num_of_clicks = 0

    def createWidgets(self):
        """Create all essential widgets."""

        self.control_group = tk.Frame(self)
        
        self.start_button = tk.Button(self.control_group)
        self.start_button['text'] = 'New Game'
        self.start_button['command'] = self.newGame     

        self.QUIT = tk.Button(self.control_group, text='QUIT', fg='red',
                              command=root.destroy)
        
        self.current_page_label = tk.Label(self.control_group)
        self.current_page_label['text'] = 'Current Page'

        self.current_clicks_label = tk.Label(self.control_group)
        self.current_clicks_label['text'] = 'Clicks: 0'
        
        self.current_page_label.pack(side='bottom')
        self.current_clicks_label.pack(side='bottom')
        self.start_button.pack(side='bottom')
        
        
        self.control_group.pack(side='top', fill='x', expand=True)

        self.canvas = tk.Canvas(root, borderwidth=0, bg='#ffffff')
        
        self.scrollbar = tk.Scrollbar(root, orient='vertical',
                                      command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        
        

    def createLinkButtons(self):
        print('Creating link buttons.')
        if self.current_page is None:
            print('-Current page is None.')
            return
        print('-Destroying children.')
        for child in self.frame.winfo_children():
            child.destroy()
            print('-- Child destroyed.')
        print('-Creating new buttons.')
        for i in range(len(self.current_page.links)):
            link = self.current_page.links[i]
            #print(link)
            button= tk.Button(self.frame, text=link,
                              command=(lambda l=link: self.followLink(l)))
            button.grid(row=i//4, column=i%4)
            print('--Button created.')
        print('-DONE Creating link buttons.')

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def newGame(self):
        """Start a new game"""
        self.num_of_clicks = 0
        self.current_page_label['text'] = 'Clicks: 0'

        self.canvas.delete('all')

        self.frame = tk.Frame(self.canvas, bg='#ffffff')
        self.canvas.create_window((0,0), window=self.frame, anchor='nw',
                                  tags='self.frame')

        self.frame.bind('<Configure>', self.onFrameConfigure)

        self.createLinkButtons()

        random_title = wp.random()

        self.followLink(random_title, counts=False)

    def followLink(self, title, counts=True):
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

        self.current_page_label['text'] = self.current_page.title

        if self.current_page.title == 'Adolf Hitler':
            self.winGame()
        else:
            self.createLinkButtons()
            if counts:
                self.num_of_clicks += 1
                new_clicks_text = 'Clicks: {!s}'.format(self.num_of_clicks)
                self.current_clicks_label['text'] = new_clicks_text

    def winGame(self):
        self.canvas.delete('all')
        self.hitler_image=tk.PhotoImage('images/smilinghitler.png')
        self.canvas.create_image((0,0), image=self.hitler_image)


def main():
    global root
    root = tk.Tk()
    app = Application(master=root)
    app.pack(side='top', fill='both')
    app.mainloop()

if __name__ == "__main__":
    main()
