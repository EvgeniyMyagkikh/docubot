# ML часть решения

## Подготовка данных

Мы парсим все сайты, указанные в https://www.rustore.ru/sitemap-help.xml/ для получения самой лучшей базы данных. \
Чтобы запустить парсер дастаточно просто запустить код:

```python
python3 parser_rustore.py
```

## Подготовка KNOWLEDGE_VECTOR_DATABASE

Чтобы наша система работала верно нам нужно иметь векторную базу данных с нашими данными \
Запустите rag_main.ipynb до ячейки

```
KNOWLEDGE_VECTOR_DATABASE.save_local("faiss_index")
```

включительно

## Инференс:

Запустить инференс системы можно двумя способами. \

1. Через Docker:\
   ```
   docker build -t cp_image .
   docker run -d --name cpcontainer -p 80:80 cp_image
   ```
2. Через Python:
   ```
   python3 app/main.py
   ```
