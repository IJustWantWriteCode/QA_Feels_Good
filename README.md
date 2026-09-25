# QA Feels Good

Инструкция по разворачиванию проекта и локальному запуску автотестов.

---

## 🛠 Предварительные требования

Перед началом работы убедитесь, что на вашей машине установлены:

- **Git** ([скачать](https://git-scm.com/))
- **Python** версии 3.10 или выше ([скачать](https://www.python.org/))
- **Poetry** ([инструкция по установке](https://python-poetry.org/docs/#installation))

> Проверить установку Poetry можно командой в терминале: `poetry --version`

---

## 🚀 Пошаговое разворачивание

### 1. Клонирование репозитория

```bash
git clone https://github.com/IJustWantWriteCode/QA_Feels_Good.git
cd QA_Feels_Good
```

### 2. Установка зависимостей

```bash
poetry install
```

### 3. Запуск автотестов

```bash
poetry run pytest
```
