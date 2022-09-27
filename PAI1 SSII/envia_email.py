import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Variables del sistema
user = "juahurmas@alum.us.es"
passW = "HHpitt66...." 
server = "mail.us.es"
puerto = 587
destinatarios = ['juanpepitt@gmail.com']
asunto = 'Reporte de registro mensual'
 
# Iniciamos los parámetros del script
DIRECTORIO_BASE = "C:/Users/juan.hurtado/Desktop/SSII/PAI1 SSII"
ruta_registro = DIRECTORIO_BASE + '/registro.log'
cuerpo = 'Este es el contenido del mensaje'
nombre_registro = 'registro.log'

def envia():

    #Excepción si el fichero de log no se encuentra en la carpeta, en ese caso lo crea vacío
    try:
        file = open(ruta_registro, 'r')
        file.close()
    except FileNotFoundError:
        print('El fichero '+nombre_registro+' no se encuentra en el directorio. Creando el nuevo fichero vacío...')
        file = open(ruta_registro, 'w')
        exit()

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = user
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
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_registro)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP(server, puerto)
    
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login(user,passW)

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(user, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()