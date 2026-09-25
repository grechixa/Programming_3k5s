# Лабораторная работа №1 — Реализация удаленного импорта

## Основное задание
Реализован механизм импорта Python-модулей по HTTP URL через `sys.path_hooks`.

Компоненты:
- `urlhook.py` — проверяет URL и получает HTML-каталог;
- `url_finder.py` — сообщает импорт-системе, существует ли модуль/пакет;
- `urlloader.py` — скачивает исходный код и выполняет его;
- `activation_script.py` — активирует hook.

## Запуск

Терминал 1:
```bash
cd rootserver
python3 -m http.server 8000
```

Терминал 2:
```bash
python3 -i activation_script.py
```

В Python:
```python
sys.path.append("http://localhost:8000")
import myremotemodule
myremotemodule.myfoo()
```

Ожидаемый результат:
```text
gr34a module is imported
```

## Проверка пакета (***)

```python
import remotepackage
remotepackage.package_info()

from remotepackage import tools
tools.hello()
```

Пакет определяется по ссылке на каталог, а `spec_from_loader(..., is_package=True)` сообщает импорт-системе, что это пакет. После этого URL пакета становится его `__path__`, поэтому вложенный `tools.py` также находится через тот же механизм.

## Вариант на requests

Установить:
```bash
python3 -m pip install -r requirements.txt
```

Запустить:
```bash
python3 -i activation_requests.py
```

Затем:
```python
sys.path.append("http://localhost:8000")
import myremotemodule
myremotemodule.myfoo()
```

В `urlhook_requests.py` и `urlloader_requests.py` вместо `urllib.request.urlopen` используется `requests.get`.

## Задание со звездочкой (*)

`url_hook` и `URLLoader` перехватывают `HTTPError`, `URLError`, таймауты и ошибки `requests`, после чего преобразуют их в понятный `ImportError`.

Проверка:
```bash
python3 demo_unavailable.py
```

Ожидается сообщение:
```text
Handled remote import error:
Remote host is unavailable: http://localhost:65500
```

## Дополнительное задание с другими хостингами

Механизм не привязан к `localhost`: в `sys.path` можно добавить URL каталога, доступного по HTTP/HTTPS, если сервер возвращает HTML directory listing с файлами `.py` и каталогами пакетов.

Например:
```python
sys.path.append("https://example.com/python-modules/")
```

Для публичного хостинга нужно учитывать HTTPS, CORS не требуется, поскольку HTTP-запрос выполняется самим Python-процессом, а не браузером.
