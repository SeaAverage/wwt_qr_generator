# this imports everything from the tkinter module
from asyncio.windows_events import NULL
from tkinter import *
# importing the ttk module from tkinter that's for styling widgets
from tkinter import ttk
# importing message boxes like showinfo, showerror, askyesno from tkinter.messagebox
from tkinter.messagebox import showinfo, showerror, askyesno
# importing filedialog from tkinter
from tkinter import filedialog
from turtle import color, fillcolor 
# this imports the qrcode module
import qrcode
import os
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.colormasks import VerticalGradiantColorMask

base_dir = os.path.dirname(__file__)

logo = Image.open(os.path.join(base_dir, 'mark.png'))
basewidth = 40
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)



def color_picker():
   return str(radio_button_var.get())
   
   

def utm_tracking():
    if checkbox_var.get() == 1:
        utm_campaign_field.config(state='enabled')
        utm_id_field.config(state='enabled')
    elif checkbox_var.get() == 0:
        utm_campaign_field.config(state='disabled')
        utm_id_field.config(state='disabled')
    return str(checkbox_var.get())
    
   

# this will ask the user whether to close or not
def close_window():
    if askyesno(title='Close QR Code Generator-Detector', message='Are you sure you want to close the application?'):
        window.destroy()

 # the function for generating the QR Code
def generate_qrcode():
    # Error Handling
    qrcode_data = str(qr_url_field.get())
    qrcode_utmcampaign = str(utm_campaign_field.get())
    qrcode_utmid = str(utm_id_field.get())
    if (checkbox_var.get() == 1 and qrcode_utmcampaign == ''):
        showerror(title='Error', message='An error occurred' \
                   '\nThe following is ' \
                    'the cause:\n->Empty UTM Campaign entry field\n' \
                    'Make sure the UTM Campaign entry field is filled when generating the QRCode')
    elif (checkbox_var.get() == 1 and qrcode_utmid == ''):
        showerror(title='Error', message='An error occurred' \
                   '\nThe following is ' \
                    'the cause:\n->Empty UTM Unique ID entry field\n' \
                    'Make sure the UTM Unique ID entry field is filled when generating the QRCode')
    # Generating and saving the QR code                
    else:
        if askyesno(title='Confirmation', message=f'Do you want to create a QRCode with the provided information?'):
            try:
                qr = qrcode.QRCode(version = 1, box_size = 6, border = 4)
                if checkbox_var.get() == 0:
                    qr.add_data(qrcode_data)
                else:
                    qr.add_data(qrcode_data+str('/?utm_source=qrcode&utm_campaign='+utm_campaign_field.get()+'&utm_id='+utm_id_field.get()))
                qr.make(fit = True)
                name = filedialog.asksaveasfilename(initialdir = "/",title = "Select file", defaultextension= '.png',filetypes = (("png files","*.png"),("all files","*.*")))
                if color_picker() == "blue":
                    qrcode_image = qr.make_image(image_factory=StyledPilImage, module_drawer=SquareModuleDrawer(), color_mask=SolidFillColorMask(back_color=(255,255,255,-255), front_color=(0,134,234,255)))
                elif color_picker() == "white":
                    qrcode_image = qr.make_image(image_factory=StyledPilImage, module_drawer=SquareModuleDrawer(), color_mask=SolidFillColorMask(back_color=(255,255,255,-255), front_color=(255,255,255,255)))
                elif color_picker() == "black":
                    qrcode_image = qr.make_image(image_factory=StyledPilImage, module_drawer=SquareModuleDrawer(), color_mask=SolidFillColorMask(back_color=(255,255,255,-255), front_color=(0,0,0,255)))
                elif color_picker() == "gradient":
                    qrcode_image = qr.make_image(image_factory=StyledPilImage, module_drawer=SquareModuleDrawer(), color_mask=VerticalGradiantColorMask(back_color=(255,255,255,-255), top_color=(238, 40, 42,255), bottom_color=(0,134,234,255)))
                pos = ((qrcode_image.size[0] - logo.size[0]) // 2, (qrcode_image.size[1] - logo.size[1]) // 2)
                qrcode_image.paste(logo, pos)
                qrcode_image.save(name)
                global Image
                Image = PhotoImage(file=f'{name}')
                image_label.config(image=Image)
                reset_button.config(state=NORMAL, command=reset)
            # this will catch all the errors that might occur
            except:
                showerror(title='Error', message='An unknown error has occurred')

# the function for resetting or clearing the image label
def reset():
    if askyesno(title='Reset', message='Are you sure you want to reset?'):
        image_label.config(image='')
        reset_button.config(state=DISABLED)


# creating the window using the Tk() class
window = Tk()
window.title('QR Code Generator')
window.iconbitmap(window, os.path.join(base_dir, 'icon.ico'))
window.geometry('500x480+440+180')
window.resizable(height=FALSE, width=FALSE)
window.protocol('WM_DELETE_WINDOW', close_window)

"""Styles for the widgets, labels, entries, and buttons"""
# style for the labels
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('Roobert', 11))
# style for the entries
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Roobert', 15))
# style for the buttons
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font=('Roobert', 10))

# creating the Notebook widget
tab_control = ttk.Notebook(window)
tab = ttk.Frame(tab_control)
tab_control.add(tab, text='QR Code Generator')
tab_control.pack(expand=1, fill="both")

canvas = Canvas(tab, width=500, height=530)
canvas.pack()

"""Widgets for the first tab"""
radio_button_var = StringVar(value="blue")
checkbox_var = IntVar()
image_label = Label(window)
canvas.create_window(250, 120, window=image_label)
radio_label = ttk.Label(window, text='QRcode Color', style='TLabel')
canvas.create_window(70, 270, window=radio_label)
radio_button_one = Radiobutton(window, text="Blue", variable=radio_button_var, value='blue',
                  command=color_picker)
radio_button_two = Radiobutton(window, text="White", variable=radio_button_var, value='white',
                  command=color_picker)
radio_button_three = Radiobutton(window, text="Black", variable=radio_button_var, value='black',
                  command=color_picker)
radio_button_four = Radiobutton(window, text="Gradient", variable=radio_button_var, value='gradient',
                  command=color_picker)
canvas.create_window(155, 270, window=radio_button_one)
canvas.create_window(235, 270, window=radio_button_two)
canvas.create_window(315, 270, window=radio_button_three)
canvas.create_window(395, 270, window=radio_button_four)
qr_url_label = ttk.Label(window, text='QRcode URL', style='TLabel')
qr_url_field = ttk.Entry(window, width=55, style='TEntry')
canvas.create_window(75, 300, window=qr_url_label)
canvas.create_window(300, 300, window=qr_url_field)
checkbox = Checkbutton(window, text = "Track QR Code with WWT\'s analytics tools", variable=checkbox_var, onvalue=1, offvalue=0, command=utm_tracking)
canvas.create_window(253, 330, window=checkbox)
utm_campaign_label = ttk.Label(window, text='UTM Campaign', style='TLabel')
utm_campaign_field = ttk.Entry(window, width=55, state = 'disabled', style='TEntry')
canvas.create_window(70, 360, window=utm_campaign_label)
canvas.create_window(300, 360, window=utm_campaign_field)
utm_id_label = ttk.Label(window, text='UTM Unique ID', style='TLabel')
utm_id_field = ttk.Entry(window, width=55, state = 'disabled', style='TEntry')
canvas.create_window(73, 390, window=utm_id_label)
canvas.create_window(300, 390, window=utm_id_field)
reset_button = ttk.Button(window, text='Reset', style='TButton', state=DISABLED)
generate_button = ttk.Button(window, text='Generate QRCode', style='TButton',  command=generate_qrcode)
canvas.create_window(300, 430, window=reset_button)
canvas.create_window(410, 430, window=generate_button)



# run the main window infinitely
window.mainloop()