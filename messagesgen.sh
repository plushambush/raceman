#!/bin/bash
IFS=',' 
while read phrase name; do
	./gensound.sh $phrase sounds_tts/ru/$name
done<<LISTEND
'Время',time
'Карт',kart
'Время соперника',rivaltime
'Установлено соединение.',connected
'Разорвано соединение',disconnected
'Картодром ',trackselected
'Слежение за картом',kartselected
'Соперник карт',rivalselected
'Ожидаем начала гонки.',racewaiting
'Гонка началась.',racestarted
'Гонка закончена.',racefinished
'Сейчас нет гонки.',norace
'Перестали поступать данные.',nodata
'Данные снова поступают.',dataagain
'Лучшее время гонки!',bestlap
'Потеряно лучшее время.',lostbestlap
'и',and
'ровно',zero
'forza',forza
LISTEND