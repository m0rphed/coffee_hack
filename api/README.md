# coffee_hack API

Хакатон по анализу данных backend часть

## Заметки по сборке

- это FastAPI проект на Python, он использует [пакетный менеджер PDM для Python](https://github.com/pdm-project/pdm) для сборки **ОДНАКО** любые другие проекты поддерживающие сборку через pyproject.toml (poetry например) - должны также работать
  - при сборке обратите внимание на *группы пакетов*
  - обратите внимание что используется т.н. ["src layout"](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html)
- подразумевается что у вас будет `.venv` в папке api (т.е. `<repo_root>/api/.venv`) и сам проект будет установлен как [editable](https://github.com/python-poetry/poetry/issues/34) пакет - иначе import-ы и модули могут не работать корректно
