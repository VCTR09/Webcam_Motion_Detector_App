<a id="anchor"></a>
# Приложение детектор движения, управляющее веб-камерой для обнаружения объектов в кадре.


* Программа обнаруживает движущиеся в кадре объекты. Программа записывает время когда объект появляется в поле зрения камеры и время когда объект покидает кадр. По завершении записи, предоставляется интерактивная диаграмма со временем всех вхождений объекта в кадр и временем нахождения перед камерой.

* Данная программа может быть использована для наблюдения за животными, а так же людьми.

* Программа создана на языке _Python_ с использованием библиотеки _OpenCV_. Также используется библиотека _Bokeh_ для визуализации конечных данных. 


### Принцип работы программы:
** Программа получает доступ к веб-камере. Первый кадр видео будет играть роль неподвижного фона. Все последующие кадры видео будут сравниваться с первым, чтобы установить есть ли между ними разница. 

** Далее в скрипте, сделаем неподвижный фон, а также текущий кадр видео _(Gray Frame)_ черно-белымы. Сохраним неподвижный фон (первый кадр) в переменной, конвертируем его в черно-белое изображение, и циклом _while_ пройдем по текущим кадрам, конвертируя их в черно-белые изображения. 

** Далее установим разницу между двумя черно-белыми изображениями: неподвижным фоном и текущим кадром. Это будет _(Delta Frame)_. Светлые пиксели в _Delta Frame_ указывают на обнаружение движения, темные пиксели на отсутствие движения. 

* __Текущий черно-белый кадр Gray Frame слева и Delta Frame справа.__
<img width="1430" alt="Gray DeltaFrames" src="https://user-images.githubusercontent.com/97599612/168471097-e979f6d3-e68a-49b1-8401-0e612b8fb9fc.png">

** Далее в _Threshold Frame_ установим, что если в _Delta Frame_ замечена разница интенсивностью более 100, данные пиксели будут конвертированы в белые пиксели, пиксели ниже порога 100 будут конвертированы в черные пиксели. Так мы получим контуры движущегося объекта.

* __Threshold Frame.__
<img width="1393" alt="ThreshholdFrame" src="https://user-images.githubusercontent.com/97599612/168471102-86470e9e-17d0-4d77-9adf-579f7579480d.png">

** После расчета _Threshold Frame_ в цикле, будем искать контуры белого объекта в текущем фрейме. Циклом _for_ пройдем по всем контурам текущего фрейма, и проверим если площадь обхватываемого контурами объекта больше определенной величины (например, 50 000 пикселей). При соблюдении условия, объект будет считаться движущимся объектом. 

** Далее нарисуем прямоугольник вокруг контуров охватывающих объект нужного размера. Прямоугольник будет виден в _Color Frame_ - это цветная версия текущего фрейма.

* __Color Frame.__
<img width="1279" alt="ColorFrame" src="https://user-images.githubusercontent.com/97599612/168471089-ebe89fae-3609-49c8-b699-c96cd8c0562a.png">

** Далее установим время когда движущийся объект попадал в кадр _(Background Frame)_ и выходил из кадра. Визуализуруем данные, чтобы получить интерактивную диаграмму.

* __Интерактивная диаграмма со временем всех вхождений объекта в кадр и временем нахождения перед камерой.__
<img width="1434" alt="MotionGraph" src="https://user-images.githubusercontent.com/97599612/168471100-e1ee220a-cffb-4f91-80e6-637c54419521.png">

* __Всплывающее окно со временем одного вхождения в кадр и продолжительностью нахождения в кадре.__
<img width="1432" alt="PopupWindow" src="https://user-images.githubusercontent.com/97599612/168471101-9b5ff8df-f75f-46e1-92d7-dadd630d2fe9.png">

### Создание:

#### 1. Создание _VideoCapture_ объекта
```
# Метод VideoCapture принимает в качестве аргумента индекс веб-камеры, либо путь до видеофайла.
# VideoCapture(0) аргумент (0) - используется только одна веб-камера.
video = cv2.VideoCapture(0)
```

```
# release метод для получения доступа к объекту video.
video.release()
```


#### 2. Создание _frame_ объекта для чтения изображений из _VideoCapture_ объекта

```
# check - True или False нужен для проверки записи видео.
# frame - первый кадр, заснятый нашей камерой.
check, frame = video.read()
```

```
# Конвертация цветного изображения в черно-белое.
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

```
# Метод imshow библиотеки cv2 для показа frame объекта (рекурсивно показывает каждый кадр в видео).
# "Color Frame" - название окна.
cv2.imshow("Color Frame", gray)
```

```
cv2.waitKey(0)  # Окно закроется при нажатии на любую из клавиш.
video.release()
cv2.destroyAllWindows()
```

#### 3. Создание цикла _while_ для показа видео, вместо показа одного изображения
```
a = 1  # Подсчет количества сделанных кадров.
while True:
    a = a + 1
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    cv2.imshow("Color Frame", gray)

    key = cv2.waitKey(1)  # Ожидание 1 миллисекунда.

    if key == ord('q'):
        break

print(a)
video.release()
cv2.destroyAllWindows()
```

#### 4. Создадие переменной для хранения первого кадра
> first_frame = None

```
# В цикле while создадим условие.
    if first_frame is None:
        first_frame = gray
        continue
```


#### 5. _GaussianBlur_ метод
```
# Применение _GaussianBlur_ для текущего изображения делает его размытым. Это уменьшает шумы и повышает 
точность вычисления разницы между изображениями.
gray = cv2.GaussianBlur(gray, (21, 21), 0)
```

```
# Установка разницу междву первым и текущим кадрами видео.
delta_frame = abs(first_frame - gray)

cv2.imshow("Delta Frame", delta_frame)
```


#### 6. Определение разницы между _Gray Frame_ и _Delta Frame_ для обнаружения объекта на видео
```
thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
```

```
# Сглаживание изображения, удаление черных просветов на белых полях.
thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

cv2.imshow("Threshold Frame", thresh_frame)
```


#### 7. Создание контуров белого объекта в _thresh_frame_
```
(cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

```
# Отфильтровка контуров. Сохраним лишь контуры обрисовывающие объекты свыше 90000 пикселей.
    for contour in cnts:
        if cv2.contourArea(contour) < 90000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)

cv2.imshow("Color Frame", frame)
```

** ___Необходимо поэкспериментировать с размером контурной области (contourArea). Значения могут разниться от 1 000 до 100 000 пикселей. Цифра зависит от экрана конкретного устройства и от того насколько большой объект мы хотим захватить.___
```
    if cv2.contourArea(contour) < 90000:
        continue
```

```
# На текущий момент скрипт выглядит так:
import cv2, time

first_frame = None

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue
   
    delta_frame = abs(first_frame - gray)
    thresh_frame = cv2.threshold(delta_frame, 150, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for contour in cnts:
        if cv2.contourArea(contour) < 90000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
   

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break


video.release()
cv2.destroyAllWindows()
```


### Хранение меток времени обнаружения объекта в CSV файле.

#### 8. Изменение статуса с "движется" на "не движется"

> status = 0

```
# Далее в цикле, при обнаружении объекта свыше 90000 пикселей статус изменится на 1.
for contour in cnts:
    if cv2.contourArea(contour) < 90000:
        continue
    status = 1
```

#### 9. Определение места в скрипте когда статус меняется с 0 на 1 (объект появляется в кадре) и с 1 на 0 (объект покидает кадр)
> status_list = [None, None]

```
# В конце цикла for.
status_list.append(status)
```

```
# После цикла while.
print(status_list)
# Соответсвенно, статус 0 означает что в камеру не попало движущихся объектов. Статус 1 означает обнаружение движущихся объектов.
```


#### 10. Установка точного времени когда статус меняется с 0 на 1 и обратно
```
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
```

```
# Исключаем ошибку list index out of range.
status_list = [None, None]
```

#### 11. Pandas и CSV
```
# Результаты записи будут сохранены в файл Times.csv
df = pandas.DataFrame(columns=["Start", "End"])


for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)


df.to_csv("Times.csv")
```

```
# В случае когда запись ведется длительное время, нужно избежать проблем с памятью из-за размеров списка.
# Для этого в цикле прежде чем проверить последний и предпоследний элементы списка, сделаем следующее:
status_list = status_list[-2:]
# Это сохранит лишь 2 последних элемента списка.
```


#### 12. Визуализация данных с _Bokeh_ (см. файл plotting.py)

```
from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
import pandas
 
cds = ColumnDataSource(df)
 
p = figure(
    x_axis_type = "datetime",
    height = 100,
    width = 500,
    sizing_mode = "scale_both",
    title = "Motion graph"
)

# убрать отметки на вертикальной оси
p.yaxis.minor_tick_line_color = None
# убрать горизонтальную сетку
p.yaxis[0].ticker.desired_num_ticks = 1
 
hover = HoverTool(
    tooltips = [
        ("Start", "@Start{%d/%m/%Y %H:%M:%S}"), 
        ("End", "@End{%d/%m/%Y %H:%M:%S}")
    ],
    formatters = {
        "@Start" : "datetime",
        "@End" : "datetime"
    }
)
p.add_tools(hover)
 
q = p.quad(
    left = "Start", 
    right = "End", 
    bottom = 0, 
    top = 1,
    color = "green",
    source = cds
)
 
output_file("Graph.html")
show(p)
```

[Вверх](#anchor)