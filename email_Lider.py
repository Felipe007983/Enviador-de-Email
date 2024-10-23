import csv
import smtplib
import time
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Template
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import os

# Template HTML como uma string
html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notificação de Pagamento</title>
</head>
<body>
    <div>
        <img src="cid:naturagy_image" alt="Naturgy"> <!-- Referência CID -->
    </div>
    <p>Olá, {{ nome_do_cliente }}</p>
    <p>O corte do seu fornecimento de gás foi programado. Regularize o pagamento. Acesse 
    <a href="http://www.minhanaturgy.com.br">www.minhanaturgy.com.br</a> para emitir 2ª via ou parcelar o seu débito.</p>
    <p>Caso já tenha regularizado o pagamento, desconsidere.</p>
    <p>Continuamos à sua disposição.</p>
    <p>Atenciosamente,</p>
    <p><strong>Equipe de Serviço ao Cliente</strong></p>
    <p>Essa é uma mensagem automática. Se tiver dúvidas ou precisar de mais informações, entre em contato com a nossa equipe de atendimento através do <a href="http://www.minhanaturgy.com.br">Portal Minha Naturgy</a>.</p>
</body>
</html>
"""

# Função para renderizar o template HTML
def render_template(template_content, context):
    template = Template(template_content)
    return template.render(context)

# Função para enviar um e-mail com imagem incorporada
def send_email_with_image(smtp_server, smtp_port, login, password, subject, from_email, to_email, html_content,
                          image_path):
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Anexar a imagem
    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<naturagy_image>')  # Defina um Content-ID
        msg.attach(img)

    # Anexar o corpo HTML
    msg.attach(MIMEText(html_content, 'html'))

    # Usar SMTP_SSL para conexões seguras
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(login, password)
        server.sendmail(from_email, to_email, msg.as_string())

# Função para enviar e-mails em massa
def enviar_emails(csv_path, output_directory, image_path, logs, envio_por_segundo):
    try:
        # Configuração do servidor SMTP
        smtp_server = 'servidor ex: smtp.com.br'
        smtp_port = 465
        login = 'login'
        password = 'senha'
        subject = 'Titulo do email'
        from_email = 'teste@gmail.net.br'

        # Criação do arquivo de log
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_path = f"log_envios_{data_hora}.txt"

        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            # Lista para armazenar os resultados do envio
            resultados = []

            # Lendo o CSV
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                rows = list(reader)
                total = len(rows)

                # Lendo e enviando e-mails em massa
                for index, row in enumerate(rows):
                    if 'email' in row and 'nome_do_cliente' in row:
                        to_email = row['email']
                        context = {
                            'nome_do_cliente': row['nome_do_cliente']
                        }

                        # Renderizar o template com as variáveis preenchidas
                        html_content = render_template(html_template, context)

                        # Enviar o e-mail com a imagem
                        try:
                            send_email_with_image(smtp_server, smtp_port, login, password, subject, from_email,
                                                  to_email, html_content, image_path)
                            log_message = f'{datetime.datetime.now()} - {to_email} - Sucesso\n'
                            resultados.append({'email': to_email, 'status': 'Sucesso'})
                        except Exception as e:
                            log_message = f'{datetime.datetime.now()} - {to_email} - Falha: {e}\n'
                            resultados.append({'email': to_email, 'status': f'Falha: {e}'})

                        # Registrar no log
                        log_file.write(log_message)
                        logs.insert(tk.END, log_message)

                        # Atualizar porcentagem de conclusão
                        progress = (index + 1) / total * 100
                        progress_label.config(text=f'Progresso: {progress:.2f}%')

                        # Respeitar a quantidade de envios por segundo
                        time.sleep(1 / envio_por_segundo)

            # Criar o caminho para o arquivo de resultados
            result_filename = f"resultados_envios_{data_hora}.csv"
            result_path = os.path.join(output_directory, result_filename)

            # Salvar os resultados em um arquivo CSV
            with open(result_path, mode='w', newline='', encoding='utf-8') as result_file:
                fieldnames = ['email', 'status']
                writer = csv.DictWriter(result_file, fieldnames=fieldnames)
                writer.writeheader()
                for resultado in resultados:
                    writer.writerow(resultado)

            logs.insert(tk.END, f'Resultados salvos em: {result_path}\n')
            logs.insert(tk.END, f'Log salvo em: {log_file_path}\n')
    except Exception as e:
        logs.insert(tk.END, f'Erro ao enviar e-mails: {e}\n')

# Função para iniciar o processo em uma nova thread
def iniciar_envio():
    csv_path = csv_entry.get()
    output_directory = result_entry.get()  # Agora é um diretório
    image_path = image_entry.get()
    envio_por_segundo = float(envio_entry.get())

    threading.Thread(target=enviar_emails, args=(csv_path, output_directory, image_path, logs, envio_por_segundo)).start()

# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("Envio de E-mails em Massa")

# Entradas para caminhos
tk.Label(root, text="Caminho do CSV de entrada:").grid(row=0, column=0, sticky="w")
csv_entry = tk.Entry(root, width=50)
csv_entry.grid(row=0, column=1)

tk.Label(root, text="Diretório para salvar os resultados:").grid(row=1, column=0, sticky="w")
result_entry = tk.Entry(root, width=50)
result_entry.grid(row=1, column=1)

tk.Label(root, text="Caminho da imagem:").grid(row=2, column=0, sticky="w")
image_entry = tk.Entry(root, width=50)
image_entry.grid(row=2, column=1)

# Entrada para quantidade de envios por segundo
tk.Label(root, text="Envios por segundo:").grid(row=3, column=0, sticky="w")
envio_entry = tk.Entry(root, width=10)
envio_entry.insert(0, "1")  # Valor padrão
envio_entry.grid(row=3, column=1, sticky="w")

# Botão para iniciar
start_button = tk.Button(root, text="Iniciar", command=iniciar_envio)
start_button.grid(row=4, column=0, columnspan=2)

# Logs
tk.Label(root, text="Logs:").grid(row=5, column=0, sticky="nw")
logs = ScrolledText(root, width=60, height=15)
logs.grid(row=5, column=1)

# Progresso
progress_label = tk.Label(root, text="Progresso: 0%")
progress_label.grid(row=6, column=0, columnspan=2)

root.mainloop()
