import csv
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import font

from tkcalendar import DateEntry


# görev ekleme fonksiyonu
def add_tasklist(listbox, tasks):
    new_task = text_task.get("1.0", "end-1c")  # görevin yazılacağı textfield daki metni başından sonuna alır
    due_date = date_picker.get_date()  # tarih seçme widgetından seçilen tarihi get.date() metodu ile alırız
    task_info = [new_task, due_date.strftime(
        '%d-%m-%Y')]  # "strftime", date pickerden aldığımız tarih bilgisini string türde istediğimiz formata dönüştürmek için kullanılır
    tasks.append(task_info)
    save_to_csv(tasks, listbox)  # görev eklenmiş güncel listeyi csv dosyaya kaydeder
    update_task_list(listbox, tasks)  # dosyayı günceller


def del_all_tasks(listbox, tasks):
    listbox.delete(0, END)
    tasks.clear()
    save_to_csv(tasks, listbox)
    update_task_list(listbox, tasks)


def edit_task(listbox, tasks):
    selected_index = listbox.curselection()
    if selected_index:
        item = selected_index[0]
        edited_task = text_task.get("1.0", "end-1c").strip()  # Remove leading/trailing whitespace
        if not edited_task:
            tkinter.messagebox.showerror(title="Error", message="Please fill in the task field.")
            return  # Exit the function if the task field is empty

        due_date = date_picker.get_date()
        edited_info = [edited_task, due_date.strftime('%d-%m-%Y')]
        listbox.delete(item)
        listbox.insert(item, f"{edited_task}                    {due_date}")
        tasks[item] = edited_info
        save_to_csv(tasks, listbox)
        update_task_list(listbox, tasks)


def del_selected_task(listbox, tasks):
    for item in listbox.curselection():
        listbox.delete(item)
        del tasks[item]
        save_to_csv(tasks, listbox)
        update_task_list(listbox, tasks)


def completed_task(task_list, completed_tasks):
    selected_items = task_list.curselection()

    if selected_items:
        index = selected_items[0]

        display_text = f"{liste[index][0]}            {liste[index][1]}"
        completed_tasks.insert(END, display_text)
        completed_list.append(liste[index])

        task_list.delete(index)
        liste.pop(index)

        save_to_csv(liste, task_list)
        save_completed_to_csv(completed_list, completed_tasks)


def not_completed_task(task_list, completed_tasks):
    selected_items = completed_tasks.curselection()

    if selected_items:
        index = selected_items[0]

        display_text = f"{completed_list[index][0]}            {completed_list[index][1]}"
        task_list.insert(END, display_text)
        liste.append(completed_list[index])

        completed_tasks.delete(index)
        completed_list.pop(index)

        save_to_csv(liste, task_list)
        save_completed_to_csv(completed_list, completed_tasks)


def save_to_csv(data, listbox):
    try:
        filename = get_filename_for_listbox(listbox)
        with open(filename, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)
    except ValueError as e:
        tkinter.messagebox.showerror(title="Error", message=str(e))


def save_completed_to_csv(data, listbox):
    try:
        filename = get_filename_for_listbox(listbox)
        with open(filename, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)
    except ValueError as e:
        tkinter.messagebox.showerror(title="Error", message=str(e))


def load_from_csv(listbox):
    filename = get_filename_for_listbox(listbox)
    try:
        with open(filename, newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            return [row for row in csvreader]
    except FileNotFoundError:
        tkinter.messagebox.showinfo(title="exception", message="dosya bulunamadı!")


def update_task_list(listbox, tasks):
    listbox.delete(0, END)
    for task_info in tasks:
        display_text = f"{task_info[0]}            {task_info[1]}"
        listbox.insert(END, display_text)


def get_filename_for_listbox(listbox):
    # Use different filenames for different listboxes
    if listbox == task_list:
        return "C:/Users/ramco/OneDrive/Masaüstü/tasks.csv"
    elif listbox == completed_tasks:
        return "C:/Users/ramco/OneDrive/Masaüstü/completed.csv"
    else:
        tkinter.messagebox.showinfo(title="exception", message="dosya bulunamadı!")
        return None  # Return None in case of an unknown listbox


root = Tk()
root.geometry("600x700")
root.title("my to-do list")
# root.iconbitmap(r"to-do-list.ico")
# root['background'] = "light blue" ikisi de olur
root.config(bg="light blue")
label_title = Label(root, text="TO-DO LİST", bg="light blue", fg="black", font="verdana 14 bold italic")
label_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

label2 = Label(root, text="Eklemek istediğiniz görevi yazınız: ", bg="light blue", fg="black", font="time 11 bold")
label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

text_task = Text(root, bg="white", font="time 10", height=2, width=40)
text_task.grid(row=2, column=0, padx=10, pady=10, sticky="w")

label_due_date = Label(root, text="bitiş tarihi seçiniz: ", bg="light blue", fg="black", font="time 11 bold")
label_due_date.grid(row=1, column=1, padx=10, pady=10, sticky="e")

date_picker = DateEntry(root, width=20, background="blue", foreground="white", borderwidth=2)
date_picker.grid(row=2, column=1, padx=10, pady=10, sticky="e")

label_tasks = Label(root, text="Tasks", font="verdana 11 bold", bg="light blue", fg="black")
label_tasks.grid(row=3, column=0, padx=10, pady=10, sticky="w")

frame_tasks = Frame(root, bg="#cdc9c9", height=350, width=550)
frame_tasks.grid(row=4, column=0, padx=10, pady=10, sticky="w", columnspan=4)

task_list = Listbox(frame_tasks, bg="#eee8aa", fg="black", font="verdana 10 bold", height=10, width=50,
                    selectbackground="#00868b", activestyle="none", selectmode=tkinter.SINGLE)
task_list.pack(side="left", fill="both")

label_completed_tasks = Label(root, text="Completed Tasks", font="verdana 11 bold", bg="light blue", fg="black")
label_completed_tasks.grid(row=6, column=0, padx=10, pady=10, sticky="w", columnspan=2)

frame_completed_tasks = Frame(root, bg="#cdc9c9", height=40, width=400)
frame_completed_tasks.grid(row=7, column=0, padx=10, pady=10, sticky="w", columnspan=4)

completed_font = font.Font(family='Tahoma', weight="bold", size=10, underline=TRUE, slant="italic")
completed_tasks = Listbox(frame_completed_tasks, bg="#9cff72", fg="black", font=completed_font, height=4, width=60,
                          selectbackground="#00868b", activestyle="none", selectmode=tkinter.SINGLE)
completed_tasks.pack(side="left", fill="both")

liste = []

add_button = Button(root, text="ekle", height=1, width=10, command=lambda: add_tasklist(task_list, liste))
add_button.grid(row=2, column=3, padx=10, pady=10, sticky="e")
print(liste)  # kontrol

scrollbar_vert = Scrollbar(frame_tasks)
scrollbar_vert.pack(side="right", fill="both")

task_list.config(yscrollcommand=scrollbar_vert.set)
scrollbar_vert.config(command=task_list.yview)

buttonfont = font.Font(family='helvetica', weight="bold", size=10)
deleteAll_button = Button(root, text="Delete All", bg="#890505", font=buttonfont, fg="white", width=10, height=2,
                          command=lambda: del_all_tasks(task_list, liste))
deleteAll_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

edit_button = Button(root, text="Edit", bg="#700096", fg="white", font=buttonfont, width=10, height=2,
                     command=lambda: edit_task(task_list, liste))
edit_button.grid(row=5, column=0, padx=10, pady=10)

delete_button = Button(root, text="Delete", bg="#ff0022", fg="white", font=buttonfont, width=10, height=2,
                       command=lambda: del_selected_task(task_list, liste))
delete_button.grid(row=5, column=0, padx=10, pady=10, sticky="e")

complete_button = Button(root, text="Completed", bg="#024f00", fg="white", font=buttonfont, width=10, height=2,
                         command=lambda: completed_task(task_list, completed_tasks))
complete_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

uncomplete_button = Button(root, text="Uncompleted", bg="#ff430a", fg="white", font=buttonfont, width=10, height=2,
                           command=lambda: not_completed_task(task_list, completed_tasks))
uncomplete_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")

clear_button = Button(root, text="Clear", bg="#559606", fg="white", width=10, font=buttonfont, height=2,
                      command=lambda: del_all_tasks(completed_tasks, completed_list))
clear_button.grid(row=8, column=1, padx=10, pady=10, sticky="w")

liste = load_from_csv(task_list)
completed_list = []
completed_list = load_from_csv(completed_tasks)
print(completed_list)

update_task_list(task_list, liste)
update_task_list(completed_tasks, completed_list)

# root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, liste, completed_list))


root.mainloop()
