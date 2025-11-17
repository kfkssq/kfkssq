import sqlite3

# 连接数据库（不存在则创建）
conn = sqlite3.connect('comments.db')
cursor = conn.cursor()

# 创建comments表
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class CommentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("评论管理系统")
        self.root.geometry("800x600")
        
        # 创建菜单
        menubar = tk.Menu(root)
        comment_menu = tk.Menu(menubar, tearoff=0)
        comment_menu.add_command(label="添加评论", command=self.show_add_comment)
        comment_menu.add_command(label="统计评论", command=self.show_stat_comment)
        menubar.add_cascade(label="评论管理", menu=comment_menu)
        root.config(menu=menubar)
        
        # 初始显示提示
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(self.frame, text="请从「评论管理」菜单中选择操作", font=("微软雅黑", 14)).pack(expand=True)
    
    def show_add_comment(self):
        # 清空当前界面
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # 设计“添加评论”界面
        tk.Label(self.frame, text="添加评论", font=("微软雅黑", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.frame, text="用户名：").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        username = tk.Entry(self.frame, width=40)
        username.grid(row=1, column=1, pady=5)
        
        tk.Label(self.frame, text="评论内容：").grid(row=2, column=0, sticky="nw", pady=5, padx=10)
        content = tk.Text(self.frame, width=40, height=10)
        content.grid(row=2, column=1, pady=5)
        
        # 提交按钮
        tk.Button(
            self.frame, 
            text="提交评论", 
            command=lambda: self.add_comment(username.get(), content.get("1.0", tk.END).strip())
        ).grid(row=3, column=0, columnspan=2, pady=10)
    
    def add_comment(self, username, content):
        if not username or not content:
            messagebox.showwarning("输入提示", "用户名和评论内容不能为空！")
            return
        
        # 插入数据库
        conn = sqlite3.connect('comments.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (username, content) VALUES (?, ?)",
            (username, content)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("操作成功", "评论添加成功！")
        
        # 清空输入框
        for widget in self.frame.winfo_children():
            widget.destroy()
        tk.Label(self.frame, text="评论添加成功，请继续操作", font=("微软雅黑", 14)).pack(expand=True)
    
    def show_stat_comment(self):
        # 清空当前界面
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # 统计评论（总数 + 按用户统计）
        conn = sqlite3.connect('comments.db')
        cursor = conn.cursor()
        
        # 统计总评论数
        total = cursor.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
        
        # 按用户统计评论数
        user_stats = cursor.execute(
            "SELECT username, COUNT(*) FROM comments GROUP BY username"
        ).fetchall()
        
        conn.close()
        
        # 显示统计结果
        tk.Label(self.frame, text="评论统计", font=("微软雅黑", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.frame, text=f"总评论数：{total}").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(self.frame, text="按用户统计：", font=("微软雅黑", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        stat_table = ttk.Treeview(self.frame, columns=("用户名", "评论数"), show="headings")
        stat_table.heading("用户名", text="用户名")
        stat_table.heading("评论数", text="评论数")
        for user, count in user_stats:
            stat_table.insert("", tk.END, values=(user, count))
        stat_table.grid(row=3, column=0, columnspan=2, pady=5, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CommentManager(root)
    root.mainloop()