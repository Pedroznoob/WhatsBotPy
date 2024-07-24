import pyautogui
import pyperclip
import time
import csv
import os

# Abrir o WhatsApp Desktop
pyautogui.hotkey('win', 's')
time.sleep(0.5)
pyautogui.write('WhatsApp', interval=0.1)
pyautogui.press('enter')
time.sleep(1)  # Ajuste o tempo conforme necessário para abrir o WhatsApp

# Caminhos dos arquivos CSV
pasta = r'C:\Users\usuario\PycharmProjects\WhatsBotComImagem'
numeros_a_enviar_file = os.path.join(pasta, 'numeros_a_enviar.csv')
numeros_enviados_file = os.path.join(pasta, 'numeros_enviados.csv')
numeros_nao_encontrados_file = os.path.join(pasta, 'numeros_nao_encontrados.csv')


# Função para ler números do arquivo CSV
def ler_numeros_enviados(file):
    numeros_enviados = set()
    try:
        with open(file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Pular o cabeçalho
            for row in reader:
                if row:
                    numeros_enviados.add(row[0].strip())  # Adiciona o número limpo (sem espaços extras)
    except FileNotFoundError:
        print(f"Arquivo {file} não encontrado.")
    return numeros_enviados


# Função para ler números não encontrados do arquivo CSV
def ler_numeros_nao_encontrados(file):
    numeros_nao_encontrados = set()
    try:
        with open(file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Pular o cabeçalho
            for row in reader:
                if row:
                    numeros_nao_encontrados.add(row[0].strip())  # Adiciona o número limpo (sem espaços extras)
    except FileNotFoundError:
        print(f"Arquivo {file} não encontrado.")
    return numeros_nao_encontrados


# Função para salvar números não encontrados no arquivo CSV
def salvar_numeros_nao_encontrados(file, numeros_nao_encontrados):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Números Não Encontrados"])
        for numero in numeros_nao_encontrados:
            writer.writerow([numero])


# Função para enviar imagem
def enviar_imagem():
    # Abrir a aba de imagens
    pyautogui.click(x=500, y=700)
    time.sleep(0.5)

    # Localizar o botão de Imagens e Videos
    try:
        botao_imagem = pyautogui.locateCenterOnScreen("button_images.png", confidence=0.5)
        if botao_imagem is None:
            raise pyautogui.ImageNotFoundException
    except pyautogui.ImageNotFoundException:
        print("Botão de imagem não encontrado, indo para o próximo número")
        pyautogui.hotkey('esc')
        time.sleep(0.5)
        pyautogui.hotkey('esc')
        return False

    # Copiar o nome da imagem para o clipboard
    pyperclip.copy(imagem)
    time.sleep(1)

    # Clicar no botão de Imagens e Videos
    pyautogui.click(botao_imagem)
    time.sleep(0.5)
    pyautogui.click(botao_imagem)
    time.sleep(0.5)

    # Colar o nome da imagem no explorador de arquivos e enviar no WhatsApp Desktop
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    return True


# Função para enviar mensagem para um número específico
def enviar_mensagem_para_numero(numero, mensagem, numeros_enviados, numeros_nao_encontrados):
    # Verificar se o número já foi enviado
    if numero in numeros_enviados:
        print(f"Número {numero} já foi enviado. Pulando para o próximo número.")
        return False

    # Verificar se o número já foi marcado como não encontrado anteriormente
    if numero in numeros_nao_encontrados:
        print(f"Número {numero} não encontrado anteriormente. Pulando para o próximo número.")
        return False

    # Localizar o campo de busca e enviar o número
    pyautogui.hotkey('esc')
    time.sleep(0.5)
    pyautogui.hotkey('esc')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(1)
    pyautogui.click(x=380, y=285)  # Ajuste as coordenadas conforme necessário
    time.sleep(1)
    pyautogui.write(numero)
    time.sleep(1)

    # Tentar localizar o botão de conversar
    try:
        botao_conversar = pyautogui.locateCenterOnScreen("button_conversar.jpg", confidence=0.7)
        if botao_conversar is None:
            raise pyautogui.ImageNotFoundException
    except pyautogui.ImageNotFoundException:
        print(f"Número {numero} não encontrado no WhatsApp. Registrando como não encontrado...")
        numeros_nao_encontrados.add(numero)
        salvar_numeros_nao_encontrados(numeros_nao_encontrados_file, numeros_nao_encontrados)
        pyautogui.hotkey('esc')
        time.sleep(0.5)
        pyautogui.hotkey('esc')
        return False

    # Clicar no botão de conversar
    pyautogui.click(botao_conversar)
    pyautogui.click(botao_conversar)
    time.sleep(1.5)

    # Verificar se já foi enviada mensagem (verificando se a imagem da rosana está visível)
    try:
        foto_rosana = pyautogui.locateCenterOnScreen("foto_rosana.jpg", confidence=0.5)
        if foto_rosana is not None:
            print(f"Número {numero} já recebeu mensagem. Pulando para o próximo número...")
            numeros_enviados.add(numero)
            salvar_numeros_nao_encontrados(numeros_enviados_file, numeros_enviados)
            pyautogui.hotkey('esc')
            time.sleep(0.5)
            pyautogui.hotkey('esc')
            return False
    except pyautogui.ImageNotFoundException:
        pass

    # Clicar no campo de texto da mensagem
    pyautogui.click(x=600, y=700)
    time.sleep(0.5)

    # Copiar a mensagem para o clipboard
    pyperclip.copy(mensagem)

    # Colar a mensagem no campo de texto do WhatsApp Desktop
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)

    # Enviar imagem
    if not enviar_imagem():
        return False

    # Adicionar o número à lista de números enviados
    numeros_enviados.add(numero)
    salvar_numeros_nao_encontrados(numeros_enviados_file, numeros_enviados)

    return True


# Mensagem a ser enviada e nome da imagem a ser enviada
imagem = "Semana_Do_Gestor.jpg"
mensagem = ("🚨 SEMANA DO GESTOR: O EVENTO COMEÇA HOJE AS 18:00! 🚨\n"
            "Prepare-se para aprender metodologias avançadas para dominar o financeiro do seu E-commerce e se tornar um Gestor Profissional.\n"
            "É chegada a hora de colocar a casa em ordem e ter clareza dos números. Marque na agenda e não perca!\n"
            "📆 Data: 16/07\n"
            "🕕 Horário: 18:00\n"
            "💻 Local: Google Meet\n"
            "📌 Entre no grupo para receber o link da sala do Meet\n"
            "https://chat.whatsapp.com/Jqx1FGuzb0Y8a0DltjH2JK")

# Ler números já enviados do arquivo CSV
numeros_enviados = ler_numeros_enviados(numeros_enviados_file)

# Ler números não encontrados do arquivo CSV
numeros_nao_encontrados = ler_numeros_nao_encontrados(numeros_nao_encontrados_file)

# Iterar sobre cada número no arquivo CSV de números a enviar
with open(numeros_a_enviar_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Pular o cabeçalho
    for row in reader:
        if row and len(row) > 0:  # Verifica se a linha não está vazia e tem pelo menos um elemento
            numero = row[0].strip()
            if numero:
                sucesso = enviar_mensagem_para_numero(numero, mensagem, numeros_enviados, numeros_nao_encontrados)
                if sucesso:
                    time.sleep(1)  # Ajuste o tempo conforme necessário entre cada envio
        else:
            print("Linha vazia encontrada no arquivo CSV. Pulando para a próxima linha.")

print("Processo de envio de mensagens concluído.")
