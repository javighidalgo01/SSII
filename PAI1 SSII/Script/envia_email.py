import smtplib
import params
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pathlib
import os

#Variables del sistema
sender, user, passw, server, puerto, destinatarios, asunto, ruta_registro, cuerpo = params.loadMail()

script_path = pathlib.Path(__file__).parent.parent.resolve()
register_filename = "registro.log"
register_path = os.path.join(script_path, register_filename)
def envia():

    #Excepción si el fichero de log no se encuentra en la carpeta, en ese caso lo crea vacío
    try:
        file = open(register_path, 'r')
        file.close()
    except FileNotFoundError:
        print('El fichero '+register_path+' no se encuentra en el directorio. Creando el nuevo fichero vacio...')
        with open(register_path, 'x') as f:
            f.close()

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = sender
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_registro, 'rb')
    
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    titulo_archivo = ruta_registro.replace('.', '', 1).replace('\\', '').replace('\\', '')
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % titulo_archivo)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP(server, puerto)
    
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login(user,passw)

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(sender, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()