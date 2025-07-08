# Путь к единственному репозиторию (передайте в скрипт или пропишите здесь)
REPO_PATH="./carboncrypt"

# Убедимся, что репо существует
if [ ! -d "$REPO_PATH/.git" ]; then
  echo "⛔ Ошибка: $REPO_PATH не является Git-репозиторием"
  exit 1
fi

# Функция генерации случайного сообщения остаётся без изменений
generate_commit_message() {
  …
}

# Запускаем цикл для 10 коммитов
for i in {1..10}; do
  # 1) Добавляем запись в локальный лог-файл внутри репо
  echo "entry $i" >> "$REPO_PATH/log.txt"

  # 2) Делаем add только внутри указанного репо
  git -C "$REPO_PATH" add log.txt

  # 3) Генерируем случайную дату
  export GIT_AUTHOR_DATE="$(date -d "$((RANDOM % 100 + 1)) days ago" '+%Y-%m-%dT12:00:00')"
  export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"

  # 4) Создаём коммит с рандомным сообщением
  git -C "$REPO_PATH" commit -m "$(generate_commit_message)"

  # 5) Пушим только в ветку main этого репо
  git -C "$REPO_PATH" push --force origin main

  # 6) Случайная задержка, чтобы не выглядеть как спам
  sleep $((RANDOM % 16 + 15))
done
