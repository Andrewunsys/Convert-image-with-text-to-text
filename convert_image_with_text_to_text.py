import datetime
import os
import pytesseract 
from PIL import Image
from tkinter import Tk, Button, Label, Entry, Checkbutton, filedialog, IntVar, END, StringVar, OptionMenu, ttk

# В планах:
# проверка на дубликат информации в разных изображениях при распознании и их невключение в текст - только упомиание что и где дублировалось.

def ocr_core(filename, langv):
	""" Функция производит обработку изображений с помощью оптического распознавания текста.  
		На входе файл распознания и язык распознаваемого текста.
		Возвращается строка с распознаным текстом."""

	text = pytesseract.image_to_string(Image.open(filename),lang=langv) #lang='rus'
	# Defaults to eng if not specified! Example for multiple languages: lang='eng+fra'
	# Используется Pillow's Image class для открытия изображения с текстом  
	# И pytesseract для определения строки в изображении 
	return text 


def show_about():
	""" Краткая справка о программе	в отдельном окне"""

	window_about = Tk()
	window_about.geometry("500x380")
	window_about.title("About 'Convert image with text to text'")

	all_font='Arial 9'

	text1="\tПриложение 'Convert image with text to text'\n"
	text1+="Версия:\t\t\t1.0\n"
	text1+="Дата последнего изменения:\t22.11.2021\n"
	text1+="Дата создания:\t\t20.11.2021\n"
	text1+="Автор:\t\t\tА\n"

	text2="Приложение конвертирует текст в графических файлах в текст в текстовом файле.\n"
	text2+="В приложении применяется Google Tesseract-OCR и оболочка PyTesseract.\n"
	text2+="Качество конвертации зависит от исходных данных (четкости отделения текста\n" 
	text2+="от фона, использованных шрифтов, ...) и выбранного языка для распознания.\n\n"
	text2+="Пояснения по работе:\n"
	text2+="  - Переместить в определенную папку изображений с текстом.\n"
	text2+="  - Изображения должны быть в форматах: bmp, jpg, png.\n"
	text2+="  - В окне приложения:\n\t- Выбрать путь к этой папке.\n"	
	text2+="\t- Выбрать язык для распознания текста на изображениях.\n"
	text2+="\t- Нажать кнопку 'Конвертация'.\n"
	text2+="  - При выполнении программы отображается прогресс ее выполнения.\n"
	text2+="  - По запершании программы формируются два файла:\n"
	text2+="   'Scr_to_text_tmp_yymmdd_hhmmss.txt' и 'Scr_to_text_yymmdd_hhmmss.txt'.\n"
	text2+="   Где '_yymmdd_hhmmss' - дата и время нажатия кнопки 'Конвертация'.\n"
	text2+="   Файлы состоят из двух частей. Первая: список всех обработаных файлов\n"
	text2+="   построчно. Вторая: имя файла и распозннаный построчно текст.\n"
	text2+="   В файле с 'tmp' присутствует распозннаный текст, как он распознался.\n"
	text2+="   В файле без 'tmp' удалены пустые строки и строки из одного пробела.\n"
	
	lbl_about1=Label(window_about, text = text1, anchor='nw', justify='left', font=(all_font))
	lbl_about1.place(x = 10, y = 10, width = 480, height = 70)
	lbl_about2=Label(window_about, text = text2, anchor='nw', justify='left', font=(all_font))
	lbl_about2.place(x = 10, y = 90, width = 480, height = 310)

	window_about.mainloop()


def choose_dir():
	""" Получение пути к выбранному файлу в вызываемом диалоговом окне. 
	Возвращает путь."""
	
	# filetypes = ("Изображение", "*.bmp *.jpg *.gif *.png")
	initial_dir=os.getcwd()	# "/"
	directory_name = filedialog.askdirectory(initialdir=initial_dir, title="Select Directory")
	if directory_name:
		return(directory_name)


def choose_dir_to_show():
	""" Предварительно очищает, а затем заполняет Entry Box указания пути к выбранной папке """

	entry_dir_to_show.delete(0, END)
	dir_name = choose_dir()
	entry_dir_to_show.insert(0, dir_name)


def convert():
	# Обновление информационных сообщений
	lbl_progress['text']= ""
	lbl_progress_count['text']= f"Составление списка файлов"
	lbl_progress_time['text']= ""
	window.update()

	# Получение дирректории расположения файлов для извлечения такста и выбор языка распознания
	dir_with_image =entry_dir_to_show.get()
	langv=selectName.get()

	# Получаем список всех файлов в выбранной папке
	files_with_image_tmp = os.listdir(dir_with_image)
	files_with_image_tmp.sort()
	files_with_image=[]
	# в итоговом списке осталяем только изображения
	for i in files_with_image_tmp:
		i_type=i[-4:]
		if i_type==".jpg" or i_type==".bmp" or i_type==".png" :
			files_with_image.append(i)

	count_f=len(files_with_image)
	count=1

	# Создаем txt файлы для сохранения распознанного текста
	datetime_object = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
	f_to_save_name = f"Scr_to_text_{datetime_object}.txt"
	f_to_save_tmp_name = f"Scr_to_text_tmp_{datetime_object}.txt"

	f_to_save_tmp_name_total=f"{dir_with_image}/{f_to_save_tmp_name}"
	f_to_save_name_total=f"{dir_with_image}/{f_to_save_name}"

	file=open(f_to_save_name_total,'w')
	file.close()
	file=open(f_to_save_tmp_name_total,'w')
	file.write(f"Список файлов к обработке:\n")
	file.close()	

	# Запись в файл информации по файлам для обработки
	for f in files_with_image:
		file=open(f_to_save_tmp_name_total,'a')
		file.write(f"{f}\n")
		file.close()
	
	# Запись в файл разделителя перед распознаным текстом
	file=open(f_to_save_tmp_name_total,'a')
	file.write(f"############################################\nРаспознанная информация:\n")
	file.close()

	# Запись в файл роспознанного текста и обновление информации о прогрессе
	datetime_object_start_convert = datetime.datetime.now()
	for f in files_with_image:
		# Запись в файл роспознанного текста
		f_name=f"{dir_with_image}/{f}"
		text1=ocr_core(f_name, langv)
		file=open(f_to_save_tmp_name_total,'a')
		file.write(f"{f}\n")
		file.write(f"{text1}\n")
		file.close()

		# Обновление информации о прогрессе
		datetime_object_i = datetime.datetime.now()
		progress=int(round(100*count/(count_f+0.01)))
		delta_time= datetime_object_i - datetime_object_start_convert
		seconds=delta_time.total_seconds()
		seconds_to_end=int(seconds * (count_f/count - 1))
		time_to_end=seconds_to_end
		if time_to_end < 60:
			time_to_end_out= f"{time_to_end} сек"
		else:
			time_to_end_out= f"{round(time_to_end/60)} мин"

		p1["value"] = progress
		lbl_progress['text']= f"Current Progress: {progress}%"
		lbl_progress_count['text']= f"Конвертированно: {count} из {count_f} файлов"
		lbl_progress_time['text']= f"Время до окончания: {time_to_end_out}"
		count+=1
		window.update()

	p1["value"] = 0
	lbl_progress['text']= f"Удаление пустых строк в файле"
	lbl_progress_count['text']= ""
	lbl_progress_time['text']= ""
	
	# Удаление пустых строк в файле f_to_save_name_total
	file=open(f_to_save_tmp_name_total,'r')
	file1=open(f_to_save_name_total,'a')
	for line in file:
		len_line=len(line)
		record=True
		if len_line==1:
			record=False
		if len_line==2 and (ord(line[-1])==32 or ord(line[-1])==10 or ord(line[-1])==12) :
			record=False
		if record:
			file1.write(line)
	file.close()
	file1.close()

	lbl_progress['text']= f"Конвертация завершена"
	lbl_progress_count['text']= f"Обработано {count_f} файлов"
	window.update()


################################### Main part ########################################
window = Tk()
window.geometry("550x150")
window.title("Convert image with text to text")
window.resizable(width=0, height=0)	# не позволяет изменять размер как ширину, так и высоту

all_font='Arial 9'

# Block 'chose directory'
lbl_dir_to_show=Label(window, text = "Выберите каталог:", anchor='e',justify='left', font=(all_font))
lbl_dir_to_show.place(x = 10, y = 10, width = 110, height = 25)

entry_dir_to_show = Entry (window, text = "")
entry_dir_to_show.place(x = 120 , y = 10, width = 300, height = 25)
# dir_name = choose_dir()
# entry_dir_to_show.insert(0, dir_name)

but_dir_to_show = Button(window, text = "Выбрать папку...", background="gray90", font=(all_font), command = choose_dir_to_show)
but_dir_to_show.place(x = 435, y = 10, width = 110, height = 25)

# Block 'choose language and convert'
lbl_dir_to_show=Label(window, text = "Выберите язык распознания:", anchor='e',justify='left', font=(all_font))
lbl_dir_to_show.place(x = 10, y = 50, width = 172, height = 25)

selectName = StringVar(window)
selectName.set("rus")

namesList = OptionMenu(window, selectName, "rus", "eng", "eng+rus","spa", "deu", "fra", "ita") # eng+deu+fra+ita+spa+por
namesList['menu'].configure(font=(all_font))
namesList.place(x = 200, y = 50, width = 100, height = 25)

but_convert = Button(window, text = "Конвертация", background="gray90", font=(all_font), command = convert)
but_convert.place(x = 435, y = 50, width = 110, height = 25)

# Block 'Progressbar'
p1 = ttk.Progressbar(window, length=200, mode ="determinate", maximum=100, orient='horizontal')
p1.place(x = 10, y = 90, width = 200, height = 25)

lbl_progress=Label(window, text = "___", anchor='n',justify='center', font=(all_font))
lbl_progress.place(x = 10, y = 120, width = 200, height = 25)

lbl_progress_count=Label(window, text = "", anchor='n',justify='center', font=(all_font))
lbl_progress_count.place(x = 220, y = 90, width = 210, height = 25)

lbl_progress_time=Label(window, text = "", anchor='n',justify='center', font=(all_font))
lbl_progress_time.place(x = 220, y = 120, width = 210, height = 25)

# Block 'О программе ...'
but_about = Button(window, text = "О программе ...", background="gray90", font=(all_font), command = show_about)
but_about.place(x = 435, y = 90, width = 110, height = 25)

window.mainloop()