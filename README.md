
# Bot do Restaurante Universitário

Este projeto envolve um bot do Telegram e um script feito em Python para recuperar diariamente o cardápio do Restaurante Universitário da UFES, e notificar o cardápio do almoço e da janta via mensagem.


## Funcionalidades

- Recupera o cardápio do RU da UFES a partir do site oficial.
- Separa e formata o cardápio do almoço e da janta.
- Envia o cardápio formatado como mensagem em um grupo do Telegram.
## Pré Requisitos

- Python 3
- Biblioteca ```urllib3```
- Biblioteca ```beautifulsoup4```
- Biblioteca ```python-telegram-bot```
- Conta no Telegram
- Bot do Telegram
- ID do Grupo (opcional)
## Instalação

Neste projeto, não será abordado como criar e configurar um bot no Telegram.

Certifique-se de ter instalado a versão mais recente do Python. Instale as bibliotecas pelos comandos:

- ```pip install urllib3```

- ```pip install beautifulsoup4```

- ```pip install python-telegram-bot```


## Configuração

- Altere o valor de ```TOKEN``` para o token do seu bot.

- Altere o valor de ```BOT_USERNAME``` para o nome do bot.

- Altere o valor de ```CHAT_ID``` para o ID do chat em que o bot irá enviar a mensagem. Caso o ID seja para um grupo, certifique-se de que o bot tenha permissão para enviar mensagens.

A URL padrão para o cardápio diário do RU já está configurado.
## Utilização

Caso a configuração tenha sido feita corretamente, basta abrir o terminal no caminho onde está localizado o projeto, e executar o comando:

```python bot.py```
## Agendamento de mensagem

O bot está configurado para enviar automaticamente o cardápio do almoço às 9:00 e o cardápio da janta às 15:00, de segunda a sexta-feira.
## Licença

Este projeto utiliza a licença do MIT. Sinta-se livre para utilizar ou aprimorar o projeto.

