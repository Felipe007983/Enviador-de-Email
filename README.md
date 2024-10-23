# Envio de E-mails em Massa com Imagem Incorporada

Este projeto é uma aplicação Python para enviar e-mails em massa com um template HTML personalizado, incorporando uma imagem ao corpo do e-mail. A aplicação lê uma lista de destinatários a partir de um arquivo CSV, envia os e-mails utilizando um servidor SMTP configurado, e gera logs e resultados dos envios.

## Funcionalidades

- **Envio em massa de e-mails** com mensagens HTML personalizadas.
- **Template HTML** para o corpo do e-mail, permitindo a personalização do conteúdo.
- **Incorporação de imagens** no corpo do e-mail usando a técnica CID.
- **Log de envio** detalhado, registrando o status de cada e-mail enviado.
- **Interface gráfica (GUI)** desenvolvida com Tkinter para facilitar a seleção dos arquivos e a configuração dos envios.
- **Taxa de envio ajustável**, permitindo definir a quantidade de e-mails enviados por segundo.
- **Relatório dos resultados de envio** salvo em um arquivo CSV.

## Pré-requisitos

- Python 3.x
- Bibliotecas Python:
  - `smtplib` (nativa do Python)
  - `email` (nativa do Python)
  - `jinja2` (`pip install Jinja2`)
  - `tkinter` (nativa em instalações padrão do Python)
  - `tqdm` (`pip install tqdm`)

## Instalação

1. **Clone o repositório** ou faça o download dos arquivos.
2. **Instale as dependências** listadas acima (caso não estejam instaladas).
3. **Configure as credenciais SMTP** diretamente no código:
   - Servidor SMTP (`smtp_server`)
   - Porta (`smtp_port`)
   - Login (`login`)
   - Senha (`password`)
   - E-mail remetente (`from_email`)

## Uso

### Preencher os campos na interface gráfica:
- **Caminho do arquivo CSV de entrada** (contendo os destinatários e seus respectivos nomes).
- **Diretório** onde os resultados (logs e relatório de envio) serão salvos.
- **Caminho da imagem** que será incorporada ao corpo do e-mail.
- **Definir a taxa de envios por segundo**.

### Formato do arquivo CSV de entrada:
O arquivo CSV deve conter as seguintes colunas:
- `email`: o endereço de e-mail do destinatário.
- `nome_do_cliente`: o nome do cliente que será usado na personalização do e-mail.

### Iniciar o envio:
- Clique no botão **Iniciar** para começar o processo de envio.

### Monitorar o progresso:
- A interface exibe logs em tempo real e uma barra de progresso indicando a porcentagem dos e-mails enviados.

### Resultados:
- Um arquivo de log com o histórico de cada envio e um arquivo CSV com o status de cada e-mail enviado serão gerados no diretório especificado.

## Template HTML

O template HTML é usado para criar o corpo do e-mail e pode ser customizado de acordo com as suas necessidades. Ele utiliza a biblioteca `Jinja2` para renderização, permitindo o uso de variáveis como `{{ nome_do_cliente }}`.

## Exemplo de Uso

### CSV de Entrada:
`csv`
email;nome_do_cliente
cliente1@example.com;João
cliente2@example.com;Maria

### Imagem Incorporada:
- Coloque o caminho para a imagem desejada no campo **"Caminho da imagem"**.
- Essa imagem será anexada ao e-mail usando uma referência CID (`cid:naturagy_image`).

### Ajustes Necessários
- **Credenciais do Servidor SMTP**: Configure as credenciais de acesso ao servidor SMTP diretamente no código, na função `enviar_emails`.
- **Template HTML**: O template pode ser ajustado no código ou carregado de um arquivo externo para personalização do conteúdo do e-mail.

### Observações
- Certifique-se de que o servidor SMTP permite envios em massa e que as credenciais fornecidas têm as permissões necessárias.
- Respeite as políticas de envio de e-mails da sua empresa e do seu servidor SMTP para evitar bloqueios por spam.

### Contribuições
Sinta-se à vontade para contribuir com melhorias para este projeto através de *pull requests*.

### Licença
Este projeto é livre para uso e distribuição, sujeito aos termos da licença MIT.
