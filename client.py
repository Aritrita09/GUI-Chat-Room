#Client Side GUI Chat Room
import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, END, NORMAL #Makes the buttons active

#Define window
root=tkinter.Tk()
root.title("Chat Client")
#root.iconbitmap("Network.ico")
root.geometry("650x650")
root.resizable(1,1)

#Define fonts and colours
my_font=('Courier', 14)
black="#010101"
pink="#FFC0CB"
root.config(bg=black)

#Define socket constants
ENCODER='utf-8'
BYTESIZE=1024
global client_socket


#Define Functions
def connect():
    '''Connect to a server at a given port/ip address'''
    global client_socket

    #Clear my previous chats
    my_listbox.delete(0,END)

    #Get the required connection information
    name=name_entry.get()
    ip=ip_entry.get()
    port=port_entry.get()

    #Only try to make a connection if all three frields are filled in
    if name and ip and port:
        #Conditions for connection are met, try for connection
        my_listbox.insert(0, f"{name} is waiting to connect to {ip} at {port}...")

        #Create a client socket to connect to the server
        client_socket=socket.socket((ip, int(port)))

        #Verify that the connection is valid
        verify_connection(name)
    else:
        #Conditions for connection were not met
        my_listbox.insert(0, "Insufficient information for connection...")


def verify_connection(name):
    '''Verify that the server connection is valid and pass required info'''
    global client_socket

    #The server will send a NAME flag if a valid connection is made
    flag=client_socket.recv(BYTESIZE).decode(ENCODER)

    if flag=='NAME':
        #The connection was made, send client name and await verification
        client_socket.send(name.encode(ENCODER))
        message=client_socket.recv(BYTESIZE).decode(ENCODER)
        if message:
            #Server sent a verification, connection is valid!
            my_listbox.insert(0, message)

            #Change button/entry states
            connect_button.config(state=DISABLED)
            disconnect_button.config(state=NORMAL)
            send_button.config(state=NORMAL)

            name_entry.config(state=NORMAL)
            ip_entry.config(state=DISABLED)
            port_entry.config(state=DISABLED)

            #Create a thread to continuously recieve
            recieve_thread=threading.Thread(target=recieve_message)
            recieve_thread.start()

        else:
            #No verification message was recieved
            my_listbox.insert(END, "Connection not verified. Goodbye...")
            client_socket.close()

    else:
        #No name flag was sent, connection was refused
        my_listbox.insert(END, "Connection refused. Goodbye...")
        client_socket.close()







def disconnect():
    '''Disconnect from the server'''
    global client_socket

    #Close connection
    #Change button/entry states
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)
    send_button.config(state=DISABLED)

    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)
    

def send_message():
    '''Send a message to the server to be broadcast'''
    global client_socket

    #Send the message to the server
    message=input_entry.get()
    client_socket.send(message.encode(ENCODER))

    #Clear the input entry
    input_entry.delete(0, END)

def recieve_message():
    '''Recieve an incoming message from the server'''
    global client_socket

    while True:
        try:
            #Recieve an incoming message from the server
            message=client_socket.recv(BYTESIZE).decode(ENCODER)
            my_listbox.insert(0, message)
        except:
            #An error occured, disconnect from the server
            my_listbox.insert(0, "Closing the connection. Goodbye...")
            disconnect()
            break
        

#Define GUI Layout
#Create Frames
info_frame=tkinter.Frame(root, bg=black)    #Enter name, ip address, port and a button that will say connect
output_frame=tkinter.Frame(root, bg=black)  #Chat from others
input_frame=tkinter.Frame(root, bg=black)   #User types messages

info_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

#Info Frame Layout
info_frame = tkinter.Frame(root, bg=black)
output_frame = tkinter.Frame(root, bg=black)
input_frame = tkinter.Frame(root, bg=black)

info_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

#Info Frame Layout
name_label = tkinter.Label(info_frame, text="Client Name:", font=my_font, fg=pink, bg=black)
name_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
ip_label = tkinter.Label(info_frame, text="Host IP:", font=my_font, fg=pink, bg=black)
ip_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
port_label = tkinter.Label(info_frame, text="Port Num:", font=my_font, fg=pink, bg=black)
port_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font, width=10)
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=pink, borderwidth=5, width=10, command=connect)
disconnect_button = tkinter.Button(info_frame, text="Disconnect", font=my_font, bg=pink, borderwidth=5, width=10, command=disconnect)

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

#Output frame layout
my_scrollbar=tkinter.Scrollbar(output_frame, orient=VERTICAL)   #Place the scrollbar in the output frame
my_listbox=tkinter.Listbox(output_frame, height=20, width=55, bg=black, fg=pink, font=my_font, yscrollcommand=my_scrollbar.set)  #Set the scroll bar 
my_scrollbar.config(command=my_listbox.yview)  #Sets the vertical view

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")  #Sticky command expands the scrollbar to north-south direction

#Input Frame Layout
input_entry=tkinter.Entry(input_frame, width=45, borderwidth=3, font=my_font)
send_button=tkinter.Button(input_frame, text="send", borderwidth=5, width=10, font=my_font, bg=pink, state=DISABLED, command=send_message)
input_entry.grid(row=0, column=0, padx=5, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)



#Run the root window's mainloop()
root.mainloop()
