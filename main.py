from msilib.schema import ComboBox
from urllib.parse import ParseResultBytes
import requests as r
import math
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import threading
from moviepy.editor import *
import webbrowser
headers = {
    "user-agent":"BDownload.exe v1.0",
    "referer":"https://www.bilibili.com",
    }
def BvToAv(Bv):
    BvNo1 = Bv[2:]
    keys = {
        '1':'13', '2':'12', '3':'46', '4':'31', '5':'43', '6':'18', '7':'40', '8':'28', '9':'5',
        'A':'54', 'B':'20', 'C':'15', 'D':'8', 'E':'39', 'F':'57', 'G':'45', 'H':'36', 'J':'38', 'K':'51', 'L':'42', 'M':'49', 'N':'52', 'P':'53', 'Q':'7', 'R':'4', 'S':'9', 'T':'50', 'U':'10', 'V':'44', 'W':'34', 'X':'6', 'Y':'25', 'Z':'1',
        'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41', 'k': '16', 'm': '11', 'n': '37', 'o': '2',
        'p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14','z':'19'
    }
    BvNo2 = []
    for index, ch in enumerate(BvNo1):
        BvNo2.append(int(str(keys[ch])))
    BvNo2[0] = int(BvNo2[0] * math.pow(58, 6));
    BvNo2[1] = int(BvNo2[1] * math.pow(58, 2));
    BvNo2[2] = int(BvNo2[2] * math.pow(58, 4));
    BvNo2[3] = int(BvNo2[3] * math.pow(58, 8));
    BvNo2[4] = int(BvNo2[4] * math.pow(58, 5));
    BvNo2[5] = int(BvNo2[5] * math.pow(58, 9));
    BvNo2[6] = int(BvNo2[6] * math.pow(58, 3));
    BvNo2[7] = int(BvNo2[7] * math.pow(58, 7));
    BvNo2[8] = int(BvNo2[8] * math.pow(58, 1));
    BvNo2[9] = int(BvNo2[9] * math.pow(58, 0));
    sum = 0
    for i in BvNo2:
        sum += i
    sum -= 100618342136696320
    temp = 177451812

    return str(sum ^ temp)

def AvToCid(Av):
    try:
       r.get("https://www.bilibili.com",headers=headers)
    except:
        cid_list = "connection error"
    else:
        url = "https://api.bilibili.com/x/player/pagelist?aid="+Av+"&jsonp=jsonp"
        text = r.get(url,headers=headers).text
        list_ = eval(text)
        try:
            data_list = list_["data"]
            cid_list = []
        except:
            cid_list = "cannot get value"
        else:
            for i in data_list:
                cid = i["cid"]
                cid_list.append(str(cid))
    return cid_list

    
def download(Av,Cid,Dpi,Paths,P,L):
    try:
       r.get("https://www.bilibili.com",headers=headers)
    except:
        return_ = "connection error"
    else:
        url = "https://api.bilibili.com/x/player/playurl?fnval=80&avid="+Av+"&cid="+Cid
        text = r.get(url,headers=headers).text
        print(url)
        null = None
        dic = eval(text)
        data = dic['data']
        #print(data)
        dash = data['dash']
        video = dash['video']
        #print(video)
        for item in video:
            if item["id"] == Dpi:# and item["codecid"] == 7:
                base_url = item['base_url']
                print(base_url)
            if item["id"] != Dpi:
                pass
        audio = dash['audio']
        for item in audio:
            if item["id"] == 30232:
                base_url2 = item['base_url']
        
        exists = os.path.exists(Paths)
        try:
            print(base_url)
        except:
            return_ = "Dpi isnt exists"
        else:
            if exists:
                video_content = r.get(base_url,headers=headers).content
                audio_content = r.get(base_url2,headers=headers).content 
                #print(video_content)
                #print(audio_content)
                P = str(P)
                try:
                    with open(Paths+"Av"+Av+"Part"+P+".mp4","wb+") as file1,open(Paths+"AV"+Av+"Part"+P+".mp3","wb+") as file2:
                        file1.write(video_content)
                        file2.write(audio_content)
                    ButtomLabel['text'] = '正在合成中……（'+str(int(P))+'/'+str(L)+'）请耐心等待。'                   
                    #messagebox.showinfo('提示','正在合成中……（'+str(int(P))+'/'+str(L)+'）点击“确定”以继续。')                 
                    video_path = VideoFileClip(Paths+"Av"+Av+"Part"+P+".mp4")
                    audio_path = AudioFileClip(Paths+"AV"+Av+"Part"+P+".mp3")
                    video = video_path.set_audio(audio_path)
                    video.write_videofile(f''+Paths+"Downloaded_Av"+Av+"Part"+P+".mp4",audio_codec='aac')
                    
                except PermissionError:
                    return_ = "permission error"
                else:
                    os.remove(Paths+"Av"+Av+"Part"+P+".mp4")
                    os.remove(Paths+"AV"+Av+"Part"+P+".mp3")
                    return_ = "successfully download"

            if exists == False:
                return_ = "paths error"
    return return_
#print(BvToAv("BV1dY411s7Vd"))
#print(AvToCid("252099419"))
#download("252099419",'453665612',64,"E:/","1")
                
pink = "#FB7299"   
pink2 = "#C7425D"
root = Tk()
root.geometry("310x282")  
root.title("BDownloder 必下载 v1.0")
Frame0 = Frame(root,bg="white")
Frame0.pack(fill=BOTH,expand=True)
Label1 = Label(root,text="视频Bv号：",bg="white")
Label1.place(x=20,y=15)
Entry1 = ttk.Entry(root,width=20)
Entry1.place(x=90,y=15)
def Question():
    messagebox.showinfo('说明','''关于Bv号的说明：
    例：https://www.bilibili.com/video/BV1GW411g7mc?spm_id_from=333.337.search-card.all.click
    其中www.bilibili.com/video/后BV**********就是BV号（*有十位）''')
def ChangeColor(event):
    Button0['image'] = Photo12
def ChangeColor2(event):
    Button0['image'] = Photo11
Photo11 = PhotoImage(file="Img/b1-1.gif")
Photo12 = PhotoImage(file="Img/b1-2.gif")            
Button0 = Button(root,image=Photo11,bd=0,bg="white",command=Question)
Button0.place(x=250,y=13)
Button0.bind("<Enter>",ChangeColor)
Button0.bind("<Leave>",ChangeColor2)
Label2 = Label(root,text="下载路径：",bg="white",)
Label2.place(x=20,y=55)
Entry2 = ttk.Entry(root,width=20)
Entry2.place(x=90,y=55)
#Entry2.insert(END,"")
Entry2["state"] = "readonly"
def ViewFolder():
    #tf = True
    path = filedialog.askdirectory()
    if path == '':
        pass
    if path != '':
        Entry2['state'] = 'normal'
        Entry2.delete(0,END)
        if len(path) == 3:
            Entry2.insert(END,path)
        if len(path) != 3:
            Entry2.insert(END,path+'/')
        Entry2['state'] = 'readonly'
def ChangeColor11(event):
    Button1['image'] = Photo22
def ChangeColor12(event):
    Button1['image'] = Photo21
Photo21 = PhotoImage(file="Img/b2-1.gif")
Photo22 = PhotoImage(file="Img/b2-2.gif")
Button1 = Button(root,bd=0,image=Photo21,bg="white",command=ViewFolder)
Button1.place(x=250,y=53)
Button1.bind("<Enter>",ChangeColor11)
Button1.bind("<Leave>",ChangeColor12)
Label3 = Label(root,text="选择画质：",bg="white")
Label3.place(x=20,y=95)
Combobox0 = ttk.Combobox(root,width=18,values=("高清 1080P","高清 720P","清晰 480P","流畅 360P"),state="readonly")
Combobox0.place(x=90,y=95)
Combobox0.current(3)
def thread_it(func, *args):
    '''将函数打包进线程'''
    t = threading.Thread(target=func, args=args) 
    t.setDaemon(True) 
    t.start()
def none():
    messagebox.showerror('错误','正在下载中，请不要操作。')
def download_command():
    global success
    Button2['command'] = none
    Bv = Entry1.get()
    Path = Entry2.get()
    Dpi_ =Combobox0.get()
    if Dpi_ == "高清 1080P":
        Dpi = 80
    elif Dpi_ == "高清 720P":
        Dpi = 64
    elif Dpi_ == "清晰 480P":
        Dpi = 32
    elif Dpi_ == "流畅 360P":
        Dpi = 16
    try:
        Av = BvToAv(Bv)
    except:
        messagebox.showerror('错误','Bv号参数错误。')
    else:
        Cid = AvToCid(Av)
        if Cid =="connection error":
            messagebox.showerror('错误','连接错误。')
        elif Cid == "cannot get value":
            messagebox.showerror('错误','Bv号参数错误。')
        elif Cid != "connection error" and Cid != "cannot get value":
            j = 0
            len_ = len(Cid)
            ButtomLabel['text'] = '状态：正在下载中……（'+str(j+1)+'/'+str(len_)+'）'
            #messagebox.showinfo('提示','开始下载，请点击“确定”继续。')
            for i in Cid:
                j = j + 1
                download_ = download(Av,i,Dpi,Path,j,len_)
                if download_ == "Dpi isnt exists":
                    messagebox.showerror('错误','该视频不支持该清晰度。')
                    success = False
                    break                                                              
                elif download_ == "paths error":
                    messagebox.showerror('错误','该路径不存在。')
                    success = False
                    break
                elif download_ == "permission error":
                    messagebox.showerror('错误','本应用程序无权限访问此目录，请以管理员身份运行本应用。')
                    success = False
                    break
                elif download_ != "Dpi isnt exists" and download_ != "paths error" and download_ != "permission error":
                    if j == len_:
                        pass 
                    else:
                        ButtomLabel['text'] = '状态：正在下载中……（'+str(j+1)+'/'+str(len_)+'）'
                        #messagebox.showinfo('提示','已下载'+str(j)+'/'+str(len_)+'，请点击“确定”继续。')
                    success = True
            if success == True:
                messagebox.showinfo('提示','下载成功。')
        ButtomLabel['text'] = '状态：等待中……'
        Entry1.delete(0,END)
    Button2['command'] = download_command
photo31 = PhotoImage(file="Img/b3-1.gif")
photo32 = PhotoImage(file="Img/b3-2.gif")
def ChangeColor21(event):
    Button2['image'] = photo32
def ChangeColor22(event):
    Button2['image'] = photo31
Button2 = Button(root,image=photo31,bg="white",bd=0,command=lambda :thread_it(download_command))
Button2.bind("<Enter>",ChangeColor21)
Button2.bind("<Leave>",ChangeColor22)
Button2.place(x=120,y=150)
grey_ = "#F5F5F5"
ButtomLabel = Label(root,text="    状态：等待中……", bd=0, relief=SUNKEN,anchor=W,height=2,bg=grey_)
ButtomLabel.pack(side=BOTTOM, fill=X)
about_ = '''【关于】
应用名称：BDownloder必下载.exe （bilibili站视频下载工具）
应用版本：v1.0
开发者：SbyYz-x00（伞兵营营长）
时间：2022.6
开发者邮箱：stoneyueryouyou@outlook.com
开发者QQ：1932972859

【用户许可协议】
在安装、使用本应用之前，为了保障您和他人的权利，请务必仔细阅读本《用户许可协议》。
1. 本应用为开源、免费软件，
（1） 开发者不接受任何形式对本应用的售卖；
（2） 源码已在Github公布，开发者谢绝任何反编译、反破解以及对应用的注入、篡改的行为；
（3） 欢迎交流，转载，版权归开发者所有，请标明来源。
2. 本应用的使用建立在遵守《中华人民共和国著作权法》的前提条件下，
（1） 请务必依照bilibili和作者对视频版权的说明使用以本应用下载的视频。未经作者允许，不得转载、篡改等操作；
（2） 本应用仅供交流娱乐，为了保护作者的著作权，请务必在24小时内删除本应用下载的视频；
（3） 严禁将由本应用下载的视频用于除娱乐以外的用途，尤其是盈利目的。
3. 本应用有权利对您的计算机作出更改。当涉及权限问题时，会自动请求管理员权限，当管理员同意后，才将继续操作。
如果同意本《用户许可协议》，请继续使用本应用；若不同意，请停止下载/将本应用从您的计算机中卸载。

【免责声明】
1. 本应用旨在倡导文明绿色上网，若用户将由本应用下载的视频用于非法用途，以及不当使用本应用导致的损失，均与开发者无关。
2. 若用户使用本应用下载的视频内容非法，与开发者无关。
3. 若有侵权，请事先协商解决。
开发者邮箱：stoneyueryouyou@outlook.com 开发者QQ：1932972859'''
photo41 = PhotoImage(file="Img/b4-1.gif")
photo42 = PhotoImage(file="Img/b4-2.gif")
def about():
    messagebox.showinfo("关于",about_)
def ChangeColor31(event):
    Button3['image'] = photo42
def ChangeColor32(event):
    Button3['image'] = photo41
Button3 = Button(root,image=photo41,bg=grey_,bd=0,command=about)
Button3.bind("<Enter>",ChangeColor31)
Button3.bind("<Leave>",ChangeColor32)
Button3.place(x=270,y=250)
def openweb():
    webbrowser.open("https://space.bilibili.com/1635778169",new=0,autoraise=True)
    webbrowser.open("https://github.com/SbyYz-x00",new=0,autoraise=True)
    webbrowser.open("https://blog.csdn.net/yueryouyou_sbyyz",new=0,autoraise=True)
def ChangeColor41(event):
    Button4['image'] = photo52
def ChangeColor42(event):
    Button4['image'] = photo51
photo51 = PhotoImage(file="Img/b5-1.gif")
photo52 = PhotoImage(file="Img/b5-2.gif")
Button4 = Button(root,image=photo51,bg=grey_,bd=0,command=openweb)
Button4.bind("<Enter>",ChangeColor41)
Button4.bind("<Leave>",ChangeColor42)
Button4.place(x=240,y=250)
root.mainloop()    
# TODO:
# 1. 关于
# 2. 删除源文件
# 3. 按钮效果
# 4. 加载效果
#。5. 标题
# 6 合并 √
# 7 权限 √
