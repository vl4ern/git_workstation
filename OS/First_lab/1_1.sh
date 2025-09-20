#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Использование: $0 директория1 директория2"
    exit 1
fi
dir1="$1"
dir2="$2"
if [ ! -d "$dir1" ]; then
        echo "Ошибка: $dir1 не существует или не является директорией"
    exit 1
fi
if [ ! -d "$dir2" ]; then
    echo "Ошибка: $dir2 не существует или не является директорией"
    exit 1
fi
files_in_dir1=0
files_in_dir2=0
matches = 0
echo "Сравнение файлов в $dir1 и $dir2..."
echo "--------------------------------------"
for file1 in "$dir1"/*; do
    [ -f "$file1" ] || continue
    ((files_in_dir1++))
    found_match=0
    for file2 in "$dir2"/*; do
        [ -f "$file2" ] || continue
        if [ $found_match -eq 0 ]; then
            ((files_in_dir2++))
        fi
        if cmp -s "$file1" "$file2"; then
            echo "Совпадение: $(basename "$file1") == $(basename "$file2")"
            ((matches++))
            found_match=1
            break
        fi
    done
done

echo "--------------------------------------"
echo "Просмотрено файлов в $dir1: $files_in_dir1"
echo "Просмотрено файлов в $dir2: $files_in_dir2"
echo "Найдено совпадений: $matches"