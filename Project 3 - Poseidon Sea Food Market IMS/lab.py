import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database

app = customtkinter.CTk()
app.title('Poseidon Sea Food IMS')
app.geometry('650x750')
app.config(bg='DeepSkyBlue3')
app.resizable(False, False)

font1 = ('Arial', 25, 'bold')
font2 = ('Arial', 18, 'bold')
font3 = ('Arial', 13, 'bold')

def create_chart():
    product_details = database.fetch_products()
    product_names = [product[1] for product in product_details]
    stock_values = [product[2] for product in product_details]

    figure = Figure(figsize=(10, 5), dpi=80, facecolor='#009ACD')
    ax = figure.add_subplot(111)
    ax.bar(product_names, stock_values, width=0.4, color='#00C2F9')

    for product in product_details:
        if product[2] < 10:
            ax.bar(product[1], product[2], width=0.4, color='red')
        else:
            ax.bar(product[1], product[2], width=0.4, color='#00C2F9')
    
    ax.set_xlabel("Product Name", color='#fff', fontsize=12)
    ax.set_ylabel("Stock Values", color='#fff', fontsize=12)
    ax.set_title("Product Stock Levels", color='#fff', fontsize=14)
    ax.tick_params(axis='y', labelcolor='#fff', labelsize=11)
    ax.tick_params(axis='x', labelcolor='#fff', labelsize=11)#rotation=-30)
    ax.set_facecolor('#00688B')

    canvas = FigureCanvasTkAgg(figure)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=520)

def add_to_treeview():
    products = database.fetch_products()
    tree.delete(*tree.get_children())
    for product in products:
        tree.insert('', END, values=product)

def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        stock_entry.insert(0, row[2])
    else:
        pass

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    stock_entry.delete(0, END)

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to update!')
    else:
        id = id_entry.get()
        name = name_entry.get()
        stock = stock_entry.get()
        database.update_product(name, stock, id)
        add_to_treeview()
        clear()
        create_chart()
        messagebox.showinfo('Success', 'Data has been updated!')

def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to delete!')
    else:
        id = id_entry.get()
        database.delete_product(id)
        add_to_treeview()
        clear()
        create_chart()
        messagebox.showinfo('Success', 'Data has been deleted!')

def insert():
    id = id_entry.get()
    name = name_entry.get()
    stock = stock_entry.get()
    if not (id and name and stock):
        messagebox.showerror('Error', 'Please fill all fields!')
    elif database.id_exists(id):
        messagebox.showerror('Error', 'ID already exists!')
    else:
        try:
            stock_value = int(stock)
            database.insert_product(id, name, stock_value)
            add_to_treeview()
            clear()
            create_chart()
            messagebox.showinfo('Success', 'Data has been inserted!')
        except ValueError:
            messagebox.showerror('Error', 'Stock should be an integer!')



title_label = customtkinter.CTkLabel(app, font=font1, text='Product Details', text_color='snow', bg_color='DeepSkyBlue3')
title_label.place(x=35, y=15)

frame = customtkinter.CTkFrame(app, bg_color='DeepSkyBlue3', fg_color='DeepSkyBlue4', corner_radius=10, border_width=2, border_color='snow', width=200, height=370)
frame.place(x=25, y=45)

image1 = PhotoImage(file='fish.png')
image1_label = Label(frame, image=image1, bg='DeepSkyBlue4')
image1_label.place(x=90, y=5)

id_label = customtkinter.CTkLabel(frame, font=font2, text='Species ID:', text_color='snow', bg_color='DeepSkyBlue4')
id_label.place(x=20, y=75)
id_entry = customtkinter.CTkEntry(frame, font=font2, text_color='grey7', fg_color='snow', border_color='DeepSkyBlue3', border_width=2, width=160)
id_entry.place(x=20, y=105)

name_label = customtkinter.CTkLabel(frame, font=font2, text='Species Name:', text_color='snow', bg_color='DeepSkyBlue4')
name_label.place(x=20, y=140)
name_entry = customtkinter.CTkEntry(frame, font=font2, text_color='grey7', fg_color='snow', border_color='DeepSkyBlue3', border_width=2, width=160)
name_entry.place(x=20, y=170)

stock_label = customtkinter.CTkLabel(frame, font=font2, text='In Stock (kg):', text_color='snow', bg_color='DeepSkyBlue4')
stock_label.place(x=20, y=205)
stock_entry = customtkinter.CTkEntry(frame, font=font2, text_color='grey7', fg_color='snow', border_color='DeepSkyBlue3', border_width=2, width=160)
stock_entry.place(x=20, y=235)

add_button = customtkinter.CTkButton(frame, command=insert, font=font2, text_color='snow', text='ADD', fg_color='green3', hover_color='green4', bg_color='DeepSkyBlue4', cursor='hand2', corner_radius=8, width=80)
add_button.place(x=20, y=280)

clear_button = customtkinter.CTkButton(frame, command=lambda:clear(True), font=font2, text_color='snow', text='NEW', fg_color='blue', hover_color='blue4', bg_color='DeepSkyBlue4', cursor='hand2', corner_radius=8, width=80)
clear_button.place(x=108, y=280)

update_button = customtkinter.CTkButton(frame, command=update, font=font2, text_color='snow', text='UPD', fg_color='orange3', hover_color='orange4', bg_color='DeepSkyBlue4', cursor='hand2', corner_radius=8, width=80)
update_button.place(x=20, y=320)

delete_button = customtkinter.CTkButton(frame, command=delete, font=font2, text_color='snow', text='DEL', fg_color='red3', hover_color='red4', bg_color='DeepSkyBlue4', cursor='hand2', corner_radius=8, width=80)
delete_button.place(x=108, y=320)

style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview', font=font3, foreground='snow', background='DeepSkyBlue4', fieldbackground='DeepSkyBlue4')
style.map('Treeview', background=[('selected', 'DeepSkyBlue3')])

tree = ttk.Treeview(app, height=17)

tree['columns']=['ID', 'Name', 'In Stock']

tree.column('#0', width=0, stretch=tk.NO) #this is to hide the 1st column
tree.column('ID', anchor=tk.CENTER, width=150)
tree.column('Name', anchor=tk.CENTER, width=150)
tree.column('In Stock', anchor=tk.CENTER, width=150)

tree.heading('ID', text='ID')
tree.heading('Name', text='Species Name')
tree.heading('In Stock', text='In Stock (kg)')
tree.place(x=320, y=45)
tree.bind('<ButtonRelease>', display_data)

add_to_treeview()
create_chart()
app.mainloop()