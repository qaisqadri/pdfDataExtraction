from tkinter import *    
from tkinter import filedialog  
from tkinter import messagebox
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk
from pdf2image import convert_from_path
import json

imglist=list()

imcount=0
im_index=0
x1,y1,x2,y2=0,0,0,0

keys=list()
values=list()

k=False
v=False

kcnt=0
vcnt=0

h,w,z=0,0,0

last_tag=''
cur_tag=''

def process_pdf(filename,var=60):
	global imglist,imcount,h,w,z, im_index
	imglist=list()
	pages = convert_from_path(filename,dpi=var)
	imcount=0
	im_index=0
	for page in pages:
		imgg=np.array(page)
		imgg=cv2.cvtColor(imgg,cv2.COLOR_BGR2RGB)
		imglist.append(imgg)
		imcount+=1

	cv_img=imglist[0]
	h,w,z=cv_img.shape
	load_img(cv_img)

def key(event):
    # print("pressed",event.char)
    global root
    if ord(event.char)==27:
    	# process_output()
    	root.quit()
    elif event.char=='k' or event.char=='K':
    	key_fxn()
    elif event.char=='v' or event.char=='V':
    	value_fxn()
    else:
    	pass

def process_output():
	pass

def click_press(event):
	global x1,y1
	# print("press")
	# x1=event.x
	# y1=event.y
	x1, y1 = canvas.canvasx(event.x), canvas.canvasy(event.y)

def click_move(event):
	global x2,y2,k,v,canvas,x1,y1,cur_tag

	# x1, y1 = canvas.canvasx(event.x), canvas.canvasy(event.y)

	x2, y2 = canvas.canvasx(event.x), canvas.canvasy(event.y)

	if k is True:
		canvas.delete(cur_tag)
		cur_tag=canvas.create_rectangle(x1,y1,x2,y2,outline='red')
		# status_label.config(text= "status : Recieved Key "+ str(kcnt))

	elif v is True:
		canvas.delete(cur_tag)
		cur_tag=canvas.create_rectangle(x1,y1,x2,y2,outline='blue')

	cool_design(event)

    
def click_release(event):
	global x2,y2, keys,values,k,v,kcnt,vcnt,canvas,undobutton,last_tag,donebutton,x1,y1,cur_tag
	# print("release")
	# x2=event.x
	# y2=event.y
	x2, y2 = canvas.canvasx(event.x), canvas.canvasy(event.y)
	canvas.delete(cur_tag)
	x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
	if k is True:
		keys.append([im_index,x1,y1,x2-x1,y2-y1])
		kcnt+=1
		print("key",kcnt,"Recived")
		keybutton.config(state=DISABLED)
		valuebutton.config(state=ACTIVE)
		# color='red'
		last_tag=canvas.create_rectangle(x1,y1,x2,y2,outline='red',tags=str(kcnt))
		status_label.config(text= "status : Recieved Key "+ str(kcnt))

	elif v is True:
		# color='blue'
		vcnt+=1
		values.append([im_index,x1,y1,x2-x1,y2-y1])
		print("value",vcnt,"Recieved")
		keybutton.config(state=ACTIVE)
		valuebutton.config(state=DISABLED)
		status_label.config(text= "status : Recieved Value "+str(vcnt))
		last_tag=canvas.create_rectangle(x1,y1,x2,y2,outline='blue',tags=str(vcnt))

	if vcnt==2:
		donebutton.config(state=ACTIVE)
	elif vcnt<2:
		donebutton.config(state=DISABLED)

	if(k is True or v is True):
		undobutton.config(state=ACTIVE)
	k,v=False,False

def key_fxn():
	global k,v, keybutton,valuebutton
	# print('key')
	# keybutton.config(state=DISABLED)
	# valuebutton.config(state=ACTIVE)
	status_label.config(text= "status : Select Key ")
	keybutton.config(relief='sunken')
	valuebutton.config(relief='raised')
	k=True
	v=False

def value_fxn():
	global k,v, keybutton,valuebutton
	# print('value')
	# keybutton.config(state=ACTIVE)
	# valuebutton.config(state=DISABLED)
	status_label.config(text= "status : Select Value ")
	valuebutton.config(relief='sunken')
	keybutton.config(relief='raised')
	k=False
	v=True

def next_image():
	global im_index,imcount,photo, canvas
	if im_index==imcount-2:
		im_index+=1
		nextbutton.config(state=DISABLED)
		status_label.config(text= "status : End of Document " )
	elif im_index<imcount:
		im_index+=1
		# prevbutton.config(state=ACTIVE)
		status_label.config(text= "status : ")
	prevbutton.config(state=ACTIVE)
	# print(im_index)
	photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imglist[im_index]))

	canvas.create_image(0,0, anchor=NW, image=photo)


def prev_image():
	global im_index,imcount,photo, canvas
	if im_index==1:
		im_index-=1
		nextbutton.config(state=ACTIVE)
		prevbutton.config(state=DISABLED)
		status_label.config(text= "status : Begining of Document ")
	elif im_index<=imcount and im_index>0:
		im_index-=1
		nextbutton.config(state=ACTIVE)
		status_label.config(text= "status : ")

	photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imglist[im_index]))

	canvas.create_image(0,0, anchor=NW, image=photo)

def get_pdf():
	global imcount,filename,status_label,sizeval
	filename = filedialog.askopenfilename( title="Select file", filetypes=[("PDF", "*.pdf")])
	# print(type(filename))

	if filename is not None or filename != ():
		process_pdf(filename,sizeval.get())
		status_label.config(text= "status : Imported pdf")
	
def reload():
	global filename, sizeval
	# close()
	if filename is not None:
		process_pdf(filename,sizeval.get())
		status_label.config(text= "status : Reloaded with dpi value : "+sizeval.get())

def get_img():
	global prevbutton,nextbutton,im_index,imcount,pdfbutton,keybutton,imgbutton,canvas,status_label
	global img,photo
	filename = filedialog.askopenfilename( title="Select img", filetypes=[("PDF", "*.jpg")])
	if filename  is not None:
		img=cv2.imread(filename)
		print(type(img))
		h,w,z=img.shape

		canvas.configure(width=w,height=h)
		photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
		canvas.create_image((0,0), anchor=NW, image=photo)

		prevbutton.config(state=DISABLED)
		nextbutton.config(state=DISABLED)
		imgbutton.config(state=DISABLED)
		pdfbutton.config(state=DISABLED)
		keybutton.config(state=ACTIVE)	

		closebutton.config(state=ACTIVE)		
		donebutton.config(state=ACTIVE)

		im_index,imcount=1,1

		status_label.config(text= "status : Imported Image ")


def load_img(cv_img=None):
	global canvas,keybutton,im_index,prevbutton,nextbutton,imgbutton,pdfbutton,img,photo,sp2,reloadbutton
	if cv_img is not None:
		img=cv_img
		keybutton.config(state=ACTIVE)
		h,w,_=cv_img.shape
		canvas.configure(width=w,height=h)
		# canvas.configure(scrollregion=canvas.bbox("all"),width=w,height=h)
		photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
		canvas.create_image(0,0, anchor=NW, image=photo)
		# sp2.config(height=500)
		# sp2.grid_propagate(0)

		canvas.config(scrollregion=(0, 0, w,h))
		# canvas.config(scrollregion=canvas.bbox(ALL))
		# canvas.grid_propagate(0)
		
		imgbutton.config(state=DISABLED)
		pdfbutton.config(state=DISABLED)

		closebutton.config(state=ACTIVE)
		reloadbutton.config(state=ACTIVE)
		# donebutton.config(state=ACTIVE)

		# prevbutton.config(state=ACTIVE)
		nextbutton.config(state=ACTIVE)
		# parentframe2.pack(side=BOTTOM)
		# canvas.bind('<Motion>', cool_design, '+')

		if im_index== 0 and imcount==1:
			prevbutton.config(state=DISABLED)
			nextbutton.config(state=DISABLED)

		# canvas.update_idletasks()
		# next_image()
		# prev_image()


def close():
	global imglist, imcount, canvas, nextbutton,prevbutton,keybutton,valuebutton,pdfbutton,imgbutton,keys,values,root,reloadbutton
	global k,v,kcnt,vcnt,status_label
	if imcount==0:
		root.quit()
	else:
		imglist=list()
		imcount=0
		keys=list()
		values=list()

		k=False
		v=False

		kcnt=0
		vcnt=0

		canvas.delete('all')
		nextbutton.config(state=DISABLED)
		prevbutton.config(state=DISABLED)
		keybutton.config(state=DISABLED)
		valuebutton.config(state=DISABLED)
		undobutton.config(state=DISABLED)
		donebutton.config(state=DISABLED)
		reloadbutton.config(state=DISABLED)

		pdfbutton.config(state=ACTIVE)
		imgbutton.config(state=ACTIVE)

		status_label.config(text= "status : Cleared. Import new Document ")
		


def done():
	global keys,values,filename,status_label
	
	filename=filename.split('/')
	for name in filename:
		pass
	v1=[values[0][1],values[0][2],values[0][3],values[0][4]]
	v2=[values[1][1],values[1][2],values[1][3],values[1][4]]
	data={"File":str(name),"page"+str(values[0][0]) : {"name of Investigators":v1,"name of Sub Investigator":v2}}


	with open('data.json', 'w') as outfile:
		json.dump(data, outfile,indent=2)
	
	status_label.config(text= "status : Done ")
	print("keys",keys)
	print("values",values)

	close()

def undo():
	global keys,values,undobutton,k,v,kcnt,vcnt,canvas,keybutton,valuebutton,last_tag,donebutton
	if kcnt>vcnt:
		valuebutton.config(state=DISABLED)
		keys.pop()
		# canvas.delete(str(kcnt))

		kcnt-=1
		key_fxn()
		
	elif kcnt==vcnt:
		keybutton.config(state=DISABLED)
		# canvas.delete(str(vcnt))
		vcnt-=1
		values.pop()
		value_fxn()

	canvas.delete(last_tag)
	undobutton.config(state=DISABLED)

	if vcnt==2:
		donebutton.config(state=ACTIVE)
	elif vcnt<2:
		donebutton.config(state=DISABLED)
	#to do : clear previous rect


# def myfunction(event):
# # 	# canvas.configure(scrollregion=canvas.bbox("all"),width=w,height=h)
# # 	# cool_design(event)
# 	pass


def cool_design(event):
	global x, y,canvas,w,h
	kill_xy()
	
	dashes = [3, 2]
	# x = canvas.create_line(event.x, 0, event.x, h, dash=dashes, tags='no')
	# y = canvas.create_line(0, event.y, w, event.y, dash=dashes, tags='no')
	# x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
	x=canvas.create_line(canvas.canvasx(event.x), 0, canvas.canvasx(event.x), h, dash=dashes, tags='no')
	y=canvas.create_line(0, canvas.canvasy(event.y), w, canvas.canvasy(event.y), dash=dashes, tags='no')

def kill_xy(event=None):
	global canvas
	canvas.delete('no')

OPTIONS = [
    "egg",
    "bunny",
    "chicken"
]

root = Tk()    
root.title("Select segments in key value pairs")  
x, y = None, None
parentframe=Frame(root)
parentframe.pack(side=TOP)

parentframe2=Frame(root)
parentframe2.pack(side=BOTTOM,fill=X)

status_label=Label(parentframe2,text="status : Started",borderwidth=2,relief='sunken',anchor=W)
status_label.pack(fill=X)

sp1=Frame(parentframe,bd=1)
sp1.pack(side=LEFT)

sp2=Frame(parentframe,bd=2,relief=SUNKEN)
sp2.pack(side=TOP)

sp2.grid_rowconfigure(0, weight=1)
sp2.grid_columnconfigure(0, weight=1)
# s=np.ones((200,200,3),dtype=np.uint8)*255
# h,w,z=s.shape

# canvas = Canvas(sp2, width = w, height = h)

yscrollbar=Scrollbar(sp2,orient="vertical")
yscrollbar.grid(row=0, column=1, sticky=N+S)
# yscrollbar.pack(side=RIGHT)
# canvas.configure(yscrollcommand=myscrollbar.set)

xscrollbar = Scrollbar(sp2, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)
# xscrollbar.pack(side=BOTTOM)

canvas = Canvas(sp2,bd=0,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)

# photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(s))
# canvas.create_image((0,0), anchor=NW,image=photo)

# fr=Frame(canvas)
xscrollbar.config(command=canvas.xview)
yscrollbar.config(command=canvas.yview)

# myscrollbar.pack(side="right",fill=Y,pady=40)

canvas.grid(row=0, column=0, sticky=N+S+E+W)
# canvas.pack(side="left",expand=YES)
# canvas.create_window((0,0),window=fr,anchor='nw')
canvas.bind('<Motion>', cool_design, '+')
canvas.bind('<B1-Motion>', click_move)

# fr.bind("<Configure>",myfunction)

keybutton=Button(sp1,text="Key",command=key_fxn)
valuebutton=Button(sp1,text="Value",command=value_fxn)

nextbutton=Button(sp1,text="Next",command=next_image)
prevbutton=Button(sp1,text="Prev",command=prev_image)

pdfbutton=Button(sp1,text='import\nPDF',command=get_pdf)
imgbutton=Button(sp1,text='import\nImage',command=get_img)

closebutton=Button(sp1,text='Close',command=close)
donebutton=Button(sp1,text="Done",command=done)

undobutton=Button(sp1,text="Undo",command=undo)
reloadbutton=Button(sp1,text="Reload",command=reload,state=DISABLED)

sizeval = StringVar(root)
sizeval.set("60") # initial value

option = OptionMenu(sp1, sizeval, "60", "80", "100", "150","300")
sizelabel=Label(sp1,text='Document\nSize')




root.bind("<Key>", key)
canvas.bind("<Button-1>", click_press)
canvas.bind("<ButtonRelease-1>", click_release)

option.grid(row=0,column=1)
sizelabel.grid(row=0,column=0)

keybutton.grid(row=6,column=0)
valuebutton.grid(row=6,column=1)

prevbutton.grid(row=4,column=0)
nextbutton.grid(row=4,column=1)

pdfbutton.grid(row=2,column=0)
imgbutton.grid(row=2,column=1)

closebutton.grid(row=3,column=0)
donebutton.grid(row=3,column=1)

undobutton.grid(row=5,column=0)
reloadbutton.grid(row=1,column=0)

prevbutton.config(state=DISABLED)
nextbutton.config(state=DISABLED)

valuebutton.config(state=DISABLED)
keybutton.config(state=DISABLED)

donebutton.config(state=DISABLED)
closebutton.config(state=DISABLED)

undobutton.config(state=DISABLED)
donebutton.config(state=DISABLED)


# canvas.pack(side=TOP, fill=BOTH)


mainloop()

print("keys",keys)
print("values",values)