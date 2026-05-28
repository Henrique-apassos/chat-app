### O que escrever no terminal para executar o servidor?

Iniciar o servidor

```uvicorn main:app --host 0.0.0.0 --port 8000 --reload```

limpar pycache:

```find . -type d -name "__pycache__" -exec rm -rf {} + ```