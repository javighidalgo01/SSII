import smtplib
import params
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Variables del sistema
sender, user, passw, server, puerto, destinatarios, asunto, ruta_registro, cuerpo = params.loadMail()

def envia():

    #Excepción si el fichero de log no se encuentra en la carpeta, en ese caso lo crea vacío
    try:
        file = open(ruta_registro, 'r')
        file.close()
    except FileNotFoundError:
        print('El fichero '+ruta_registro+' no se encuentra en el directorio. Creando el nuevo fichero vacío...')
        with open(ruta_registro, 'x') as f:
            f.write("#Registro de los archivos comprometidos al final de cada día\n")

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
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % ruta_registro)
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