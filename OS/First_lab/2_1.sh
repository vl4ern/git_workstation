#!/bin/bash

echo "Все аргументы командной строки: "
for i in $(seq 1 $#); do
    echo "Аргумент $i : ${!i}"
done

output_file="arguments.txt"
echo "Все аргументы командной строки: " > "$output_file"
for i in $(seq 1 $#); do
    echo "Аргуммент $i: ${!i}" >> "$output_file"
done
echo "Аргументы сохранены в файл 'argument.txt'"