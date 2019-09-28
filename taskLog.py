# coding: utf-8

import tkinter as tk
from tkinter import messagebox
import datetime
import pytz
import getpass

after_id = None


def startTimerTrig():

    # after_cancelを用いてcommand 実行待ちを取り消す。
    # これをしないと複数回STARTボタンを押すと、
    # 前回のcommand も重複して実行されるため、残り時間が狂う!!
    global after_id
    if after_id:
        root.after_cancel(after_id)
        after_id = None

    now_jp = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    date_jp_form = now_jp.strftime("%Y/%m/%d %H:%M:%S")
    user_id = getpass.getuser()

    with open(LOG_PATH, 'a') as f:
        print(date_jp_form + '  ' 'USER：' + user_id + '  ' + 'タスク名：' + entryTaskName.get(), file=f)

    buff.set(str(CNT_TIME))
    timer()


def timer():
    global after_id

    time = int(buff.get())
    if time > 0:
        after_id = root.after(1000, timer)
        time -= 1
        buff.set(str(time))
    else:
        messagebox.showinfo('経過報告', str(CNT_TIME) + '秒経過しました!!!!')


# 設定ファイルの読み込み
with open('./config.txt', 'r') as f:
    configList = f.readlines()
    # カウントダウン時間
    CNT_TIME = int(configList[0].rstrip().split(':')[1])
    # タスクログの出力場所
    LOG_PATH = configList[1].rstrip().split(':')[1]

# カウントダウン時間


root = tk.Tk()
root.title('タスクログ')

taskNameLabel = tk.Label(root, text = 'タスク名：')
taskNameLabel.grid(column=0, row=0)

entryTaskName = tk.Entry(root, width=50)
entryTaskName.grid(column=1, row=0)

button =tk.Button(root, text = 'START', command = startTimerTrig)
button.grid(column=2, row=0)

remainingTimeStr = tk.Label(root, text = '残り時間[秒]：')
remainingTimeStr.grid(column=0, row=1, sticky=tk.E)

buff = tk.StringVar()
buff.set(str(CNT_TIME))

remainingTime  = tk.Label(root, textvariable = buff)
remainingTime.grid(column=1, row=1,sticky=tk.W )

root.mainloop()