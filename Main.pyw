# File: hello2.pyw

from Tkinter import *
import ttk
import sqlite3

class CDatabase():

    def __init__(self):

        try:
            self.connection=sqlite3.connect("AdminBookkeepingDB.db")
            self.cursor = self.connection.cursor()

        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            if self.connection:
                connection.close()

    def getMemberInformation(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM member")
            rows = self.cursor.fetchall()
            return rows


class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class App:

    def __init__(self, root):
        self.database=CDatabase()

        root.title("Tkinter Test Application")
        self.create_menu(root)

        self.create_toolbar(root)

        status = StatusBar(root)
        status.set("aaplication started")
        status.pack(side = BOTTOM, fill=X)
        
        middleFrame = Frame(root)
        middleFrame.pack(fill=BOTH, expand=1)

        self.create_treeview(middleFrame)

        self.CreateRightFrame(middleFrame)

        bottomFrame = Frame(root)
        bottomFrame.pack(side = BOTTOM, anchor=E)
        self.button = Button(bottomFrame, text = "Quit", fg = "red", command = root.destroy)
        self.button.pack(side = LEFT)

        self.hi_there = Button(bottomFrame, text="Hello", command = self.say_hi)
        self.hi_there.pack(side = LEFT)
        

    def create_menu(self, root):
        #create menu
        menu = Menu(root, tearoff=0)
        root.config(menu = menu)
        
        filemenu = Menu(root, tearoff=0)
        menu.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "New", command = self.callback)
        filemenu.add_command(label = "Open...", command = self.callback)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = self.callback)

        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label = "Help", menu = helpmenu)
        helpmenu.add_command(label = "About...", command = self.callback)

    def create_toolbar(self, root):
        # create a toolbar
        toolbar = Frame(root)

        b = Button(toolbar, text="new", width=6, command=self.callback)
        b.pack(side=LEFT, padx=2, pady=2)

        b = Button(toolbar, text="open", width=6, command=self.callback)
        b.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        print "you clicked on", self.tree.item(item,"text")

    def create_treeview(self, frame):
        innerFrame = Frame(frame)
        innerFrame.pack(side = LEFT, fill = BOTH, expand = 1)
        self.dd = Label(innerFrame, text = "Category");
        self.dd.pack(side = TOP)
        self.tree = ttk.Treeview(innerFrame, selectmode="browse")
        self.treeyscroll = ttk.Scrollbar(self.tree, orient = VERTICAL, command = self.tree.yview)
        self.treeyscroll.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = self.treeyscroll.set)
        self.tree.heading("#0", text="Directory Structure", anchor='w')
        self.populateTreeview()

        # Register event for treeview.
        #self.tree.bind("<Double-1>", self.OnDoubleClick)
        #<<TreeviewSelect>> 	Generated whenever the selection changes.
        self.tree.bind("<<TreeviewSelect>>", self.OnDoubleClick)

        #<<TreeviewOpen>> 	Generated just before settings the focus item to open=True.
        #self.tree.bind()

        #<<TreeviewClose>> 	Generated just after setting the focus item to open=False.
        #self.tree.bind()

        self.tree.pack(side = LEFT, fill=BOTH, expand=1)
##        # Inserted at the root, program chooses id:
##        self.tree.insert('', 'end', 'widgets', text='Widget Tour')
##
##        # Same thing, but inserted as first child:
##        self.tree.insert('', 0, 'gallery', text='Applications')
##
##        # Treeview chooses the id:
##        id = self.tree.insert('', 'end', text='Tutorial')
##
##        # Inserted underneath an existing node:
##        self.tree.insert('widgets', 'end', text='Canvas')
##        for i in range(1, 10, 1):
##            self.tree.insert('widgets', 'end', text='Canvas' + str(i))
##        self.tree.insert(id, 'end', text='Tree')

    def populateTreeview(self):
        records = self.getMembersInformationData()
        for record in records:
            name = record[1]
            leadName = record[2]
            if leadName == "No":
                self.tree.exists(name)
                self.tree.insert("", "end", name, text=name)
            else:
                self.tree.insert(leadName, "end", text=name)

    def getMembersInformationData(self):
        return self.database.getMemberInformation()

    def say_hi(self):
        print "hi there, everyone!"

    def callback(self):
        print "called the callback!"

    def CreateRightFrame(self, root):
        self.rightFrame = Frame(root, width = 400, height = 400)
        self.rightFrame.pack(side = LEFT, fill = BOTH, expand = 1)

root = Tk()

#"%dx%d%+d%+d" % (width, height, xoffset, yoffset)
width=210
height=300
xoffset=1
yoffset=1
root.geometry("%dx%d%+d%+d" % (width, height, xoffset, yoffset))

app = App(root)
root.mainloop()
