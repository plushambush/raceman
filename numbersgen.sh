#!/bin/bash
START=1
STOP=999
SOUND_DIR='sounds_tts/new/'
PAUSE=0.1
python ./numbersgen.py $SOUND_DIR $START $STOP
for file in $SOUND_DIR/*.raw; do
	./convert.sh $file $SOUND_DIR/$(basename $file .raw).wav
	rm $file
done
for file in $SOUND_DIR/*-preup.wav; do
	base=$SOUND_DIR/$(basename $file -preup.wav)
	sox $file ${base}-preup.wav silence 1 0 0 1 $PAUSE 0.1% : newfile : restart
	rm $file
	mv ${base}-preup001.wav $base-up.wav
	rm ${base}-preup*.wav
done

while read phrase name; do
	./gensound.sh $phrase $SOUND_DIR/$name
done<<LISTEND
'ТРИЛЛИОН', 	trillion0
'ТРИЛЛИОНА', 	trillion1
'ТРИЛЛИОНОВ',	trillion2
'ТРИЛЛИОНЫ', 	trillion3
'МИЛЛИАРД',		billion0
'МИЛЛИАРДА',	billion1
'МИЛЛИАРДОВ',	billion2
'МИЛЛИАРДЫ', 	billion3
'МИЛЛИОН',		million0
'МИЛЛИОНА',		million1
'МИЛЛИОНОВ',	million2
'МИЛЛИОНЫ',		million3
'ТЫСЯЧА',		thousand0
'ТЫСЯЧИ',		thousand1
'ТЫСЯЧ',		thousand2
'ТЫСЯЧИ',		thousand3
'СЕКУНДА',		second0
'СЕКУНДЫ',		second1
'СЕКУНД',		second2
'СЕКУНДЫ',		second3
'МИНУТА',		minute0
'МИНУТЫ',		minute1
'МИНУТ',		minute2
'МИНУТЫ',		minute3
'ЧАС',			hour0
'ЧАСА',			hour1
'ЧАСОВ',		hour2
'ЧАСЫ',			hour3
'ДЕСЯТАЯ',		tenth0
'ДЕСЯТОЙ',		tenth1
'ДЕСЯТЫХ',		tenth2
'ДЕСЯТЫЕ',		tenth3
'СОТАЯ',		hundredth0
'СОТОЙ',		hundredth1
'СОТЫХ',		hundredth2
'СОТЫЕ',		hundredth3
'ТЫСЯЧНАЯ',		thousandth0
'ТЫСЯЧНОЙ',		thousandth1
'ТЫСЯЧНЫХ',		thousandth2
'ТЫСЯЧНЫЕ',		thousandth3
'КРУГ',			lap0
'КРУГА',		lap1
'КРУГОВ',		lap2
'КРУГИ'			lap3
LISTEND
