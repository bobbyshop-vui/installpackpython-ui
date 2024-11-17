import tkinter as tk
from tkinter import messagebox
from tkinter import font
import subprocess
import threading
import os

# Hàm để kiểm tra Python đã cài đặt chưa
def check_python_installed():
    try:
        python_version = subprocess.check_output(['python', '--version'], stderr=subprocess.STDOUT, text=True)
        return python_version
    except:
        try:
            python_version = subprocess.check_output(['python3', '--version'], stderr=subprocess.STDOUT, text=True)
            return python_version
        except Exception as e:
            return None

# Hàm để chạy lệnh trong thư mục chỉ định và hiển thị đầu ra trong terminal
def run_command(command, terminal, working_dir):
    try:
        # Chuyển đến thư mục chỉ định
        os.chdir(working_dir)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            terminal.insert(tk.END, line)
            terminal.see(tk.END)  # Tự động cuộn xuống dòng mới nhất
        process.wait()
        if process.returncode == 0:
            terminal.insert(tk.END, f"\nLệnh {' '.join(command)} đã được thực thi thành công.\n")
        else:
            terminal.insert(tk.END, f"\nCó lỗi xảy ra khi thực thi lệnh {' '.join(command)}.\n")
    except Exception as e:
        terminal.insert(tk.END, f"\nLỗi: {str(e)}\n")
    
    terminal.config(state=tk.DISABLED)  # Vô hiệu hóa chỉnh sửa sau khi thực thi xong

# Hàm để xử lý các hành động cài đặt, cập nhật và lệnh tùy chỉnh
def handle_action(action, terminal):
    package_name = package_entry.get().strip()
    custom_command = command_entry.get().strip()
    target_dir = directory_entry.get().strip() or '.'  # Nếu không có nhập thư mục, dùng thư mục hiện tại

    if action in ['install', 'update']:
        if package_name == "":
            messagebox.showwarning("Cảnh báo", "Bạn phải nhập tên gói.")
            return
        
        terminal.config(state=tk.NORMAL)  # Cho phép thêm đầu ra vào terminal
        terminal.delete(1.0, tk.END)  # Xóa nội dung cũ
        action_text = "cài đặt" if action == 'install' else "cập nhật"
        terminal.insert(tk.END, f"Đang {action_text} gói: {package_name}\n")
        
        # Chạy pip install hoặc pip install --upgrade trong một thread riêng để không làm đơ giao diện
        update = action == 'update'
        threading.Thread(target=run_command, args=(['pip', 'install', '--upgrade', package_name] if update else ['pip', 'install', package_name], terminal, target_dir)).start()
    
    elif action == 'custom':
        if custom_command == "":
            messagebox.showwarning("Cảnh báo", "Bạn phải nhập lệnh tùy chỉnh.")
            return
        
        terminal.config(state=tk.NORMAL)  # Cho phép thêm đầu ra vào terminal
        terminal.delete(1.0, tk.END)  # Xóa nội dung cũ
        terminal.insert(tk.END, f"Đang chạy lệnh: {custom_command}\n")
        
        # Chạy lệnh tùy chỉnh trong một thread riêng để không làm đơ giao diện
        threading.Thread(target=run_command, args=(custom_command.split(), terminal, target_dir)).start()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Install library python tool")
root.geometry("600x600")
root.configure(bg="#2E3440")

# Tùy chỉnh font chữ
header_font = font.Font(family="Helvetica", size=16, weight="bold")
entry_font = font.Font(family="Helvetica", size=12)

# Kiểm tra Python có cài đặt không
python_version = check_python_installed()
if python_version is None:
    messagebox.showerror("Lỗi", "Python chưa được cài đặt trên hệ thống này. Vui lòng cài đặt Python trước khi sử dụng công cụ này.")
    root.destroy()
else:
    # Hiển thị thông tin phiên bản Python
    header_label = tk.Label(root, text=f"Cài đặt Gói Python\n(Phiên bản {python_version.strip()})", 
                            font=header_font, fg="#88C0D0", bg="#2E3440")
    header_label.pack(pady=10)

    # Tạo các widget
    label = tk.Label(root, text="Nhập tên gói cần cài đặt:", font=entry_font, fg="#ECEFF4", bg="#2E3440")
    label.pack(pady=10)

    package_entry = tk.Entry(root, width=40, font=entry_font)
    package_entry.pack(pady=5)

    install_button = tk.Button(root, text="Cài đặt", command=lambda: handle_action('install', terminal), 
                               bg="#5E81AC", fg="#ECEFF4", font=entry_font)
    install_button.pack(pady=5)

    update_button = tk.Button(root, text="Cập nhật", command=lambda: handle_action('update', terminal), 
                              bg="#88C0D0", fg="#ECEFF4", font=entry_font)
    update_button.pack(pady=5)

    command_label = tk.Label(root, text="Nhập lệnh tùy chỉnh:", font=entry_font, fg="#ECEFF4", bg="#2E3440")
    command_label.pack(pady=10)

    command_entry = tk.Entry(root, width=40, font=entry_font)
    command_entry.pack(pady=5)

    custom_command_button = tk.Button(root, text="Chạy lệnh tùy chỉnh", command=lambda: handle_action('custom', terminal),
                                      bg="#BF616A", fg="#ECEFF4", font=entry_font)
    custom_command_button.pack(pady=10)

    directory_label = tk.Label(root, text="Nhập thư mục làm việc (để trống cho thư mục hiện tại):", font=entry_font, fg="#ECEFF4", bg="#2E3440")
    directory_label.pack(pady=10)

    directory_entry = tk.Entry(root, width=40, font=entry_font)
    directory_entry.pack(pady=5)

    # Thêm Text widget làm terminal
    terminal = tk.Text(root, height=15, font=("Courier", 10), bg="#3B4252", fg="#ECEFF4")
    terminal.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    terminal.config(state=tk.DISABLED)  # Khóa terminal ban đầu

# Chạy ứng dụng
root.mainloop()
