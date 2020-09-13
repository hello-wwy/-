import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
import spider
from tkinter import filedialog

class App:
    def __init__(self):
        window.title('音乐下载器')
        window.geometry('800x600')
        window.resizable(0, 0)
        window.mainloop()

window = tk.Tk()
canvas = tk.Canvas(window,height=150,width=700)
img_file = ImageTk.PhotoImage(file='./image/11.jpg')
img = canvas.create_image(15,0,anchor='nw',image=img_file)
canvas.pack()

def get_song():
    text_number.delete(0.0,tk.END)   # text.delete(index1, index2)删除text内容，index1，index2必须为n.n的形式，n.n表示第n行的第n个下标
    text_singers.delete(0.0,tk.END)
    text_songnames.delete(0.0,tk.END)
    song_name = e.get()
    global name_list,singers,id_list
    name_list, singers, id_list = spider.WyyMusic(song_name).get_info()
    i = 1
    for name,singer in zip(name_list,singers):
        text_number.insert('end',i)
        i += 1
        text_number.insert('end','\n')
        text_songnames.insert('end',name)
        text_songnames.insert('end','\n')
        text_singers.insert('end',singer)
        text_singers.insert('end','\n')

def keep_lyrics():
    global id_list
    lrc =  spider.WyyMusic(song_name=e.get()).get_lyrics(id=id_list[int(download_e.get())-1])
    file_path = filedialog.asksaveasfilename(filetype=[('TXT', '.txt')],
                                             initialdir='./lyrics')
    with open(file_path,'w',encoding='utf-8') as f:
        for x in lrc:
            if x != '':
                f.write(x)
                f.write('\n')

def keep_song():
    global name_list,id_list
    song = spider.WyyMusic(song_name=e.get()).get_song(id=id_list[int(download_e.get())-1])
    file_path = filedialog.asksaveasfilename(title='11',filetype=[('MP3','.mp3'),('M4A','.m4a')],initialdir='./songs')   # 初始保存目录
    try:
        with open(file_path,'wb') as f:
            f.write(song)
    except:
        pass
    print(file_path)

'''搜索部分'''
e = tk.Entry(window)
e.place(x=320,y=180)
l_search = tk.Label(window,text='搜索：',bg='yellow',font = ("楷体",15))
l_search.place(x=220,y=180)
confirm = tk.Button(window,text='确定',height=1,command=get_song).place(x=480,y=180)

'''结果栏部分'''
text_number = tk.Text(window,height=15,width=10)
text_number.place(x=10,y=250)

text_songnames = tk.Text(window,height=15,width=60)
text_songnames.place(x=60,y=250)
# sb = tk.Scrollbar(text_songnames,orient='h')
# sb.pack(side=tk.BOTTOM,fill=tk.X)
# sb.config(command=text_songnames.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
# text_songnames.config(yscrollcommand=sb.set)

text_singers = tk.Text(window,height=15,width=40)
text_singers.place(x=400,y=250)

'''选择下载部分'''
download_l = tk.Label(window,text='请选择下载的序号:',bg='yellow',font = ("楷体",12)).place(x=200,y=470)
download_e = tk.Entry(window)
download_e.place(x=350,y=470,width=25)
select_b = tk.Label(window,text='下载',bg='yellow',font = ("楷体",12)).place(x=300,y=520)

b1 = tk.Button(window,text='歌曲',command=keep_song)
b2 = tk.Button(window,text='歌词',command=keep_lyrics)
b1.place(x=350,y=520)
b2.place(x=400,y=520)

App()
