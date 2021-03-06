# MIPT_Plot
- Simple script for **quick** plots creation
- Automatic calculations of coefficients by **least squares** with errors 
![LaTeX](https://github.com/gkorepanov/MIPT_Plot/blob/master/screenshots/LaTeX.png)
- It's a **beta** version now, need to be improved
- Gives an excellent result in LaTeX, other terminals are to be developed further

Look examples for settings description.
Running:
> python MIPT_Plot.py [myfile.dat]

###Instruction (in Russian):
1) Создаём файл произвольного формата следующего содержания (назначения настроек понятны из комментариев, обязательно указывать только output):
```Python
# Это комментарий

# Требуются ли погрешности по Ox, Oy
x_error: 0
y_error: 1

# Границы осей (опционально)
x_limits: 0 15
y_limits: 0 70

# Имя выходного файла
output: plot1.tex

# Подписи осей
x_title: $I,$ А
y_title: $B$, мТл

# При значении label=1 на графике отображается подпись с угловым коэффициентом
label: 1

# Координаты подписи на графике
label_x: 1
label_y: 60

# Единицы измерения
label_text: " $\\frac{\\text{мТл}}{\\text{А}}$"
label_size: 15

# Выбор терминала для gnuplot, поддерживает опции
term: epslatex

# Данные по колонкам
data:
### |x|y|xerr|yerr| ###

# В данных поддерживаются как запятые:
1   5  1,4
# Так и точки:
2   7  1.6
3  11  3
4  15  4
5  16  5
6  18  6
7  23  6
8  27  7
9  33  8
10 38  8
11 48  9
12 58  9
13 67 10
```
2) Запускаем командой вида 
> python MIPT_Plot.py [myfile.dat]

3) Получаем предпросмотр картинки, после нажатия Enter в терминале всё закрывается, создаётся файл выбранного формата.
4) Profit!
5) Tex Users: по-умолчанию терминал epslatex, выходной файл указываем [smth].tex, два выходных файла [smth].tex и [smth].eps кидаем в папку с документом, подключаем командой вида
```tex
\begin {figure}[H]
\begin{center}
\input{[smth]}
\caption{Пробный график}
\end{center}
```
