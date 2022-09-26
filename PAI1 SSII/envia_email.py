import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Establecer variables del sistema
user = "juahurmas@alum.us.es"
passW = "HHpitt66...." 
server = "mail.us.es"
puerto = 587

destinatarios = ['juanpepitt@gmail.com']
asunto = 'Reporte de registro mensual'

#Función de envío de mail
def envioMail (recipient, subject, text):
    smtpserver = smtplib.SMTP(server, puerto)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(user, passW)
    header = 'To: '+recipient+ "\n" + "From: "+user
    header = header + "\n" + "Subject:" +subject+ "\n"
    msg = header + "\n" + text + "\n\n"
    smtpserver.sendmail(user, recipient, msg)
    smtpserver.close()
 
# Iniciamos los parámetros del script
cuerpo = 'Este es el contenido del mensaje'

try:
    file = open('C:/Users/juanp/Documents/APUNTES/2022-2023/SSII/GitHubSSII/PAI1 SSII/registro.log')
    print(file) # File handler
    file.close()
except FileNotFoundError:
    print('Sorry the file we\'re looking for doesn\'t exist. Creando el fichero...')
    file = open('C:/Users/juanp/Documents/APUNTES/2022-2023/SSII/GitHubSSII/PAI1 SSII/registro.log', 'w')
    exit()


ruta_adjunto = 'C:/Users/juanp/Documents/APUNTES/2022-2023/SSII/GitHubSSII/PAI1 SSII/registro.log'
nombre_adjunto = 'registro.log'

# Creamos el objeto mensaje
mensaje = MIMEMultipart()
 
# Establecemos los atributos del mensaje
mensaje['From'] = user
mensaje['To'] = ", ".join(destinatarios)
mensaje['Subject'] = asunto
 
# Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
mensaje.attach(MIMEText(cuerpo, 'plain'))
 
# Abrimos el archivo que vamos a adjuntar
archivo_adjunto = open(ruta_adjunto, 'rb')
 
# Creamos un objeto MIME base
adjunto_MIME = MIMEBase('application', 'octet-stream')
# Y le cargamos el archivo adjunto
adjunto_MIME.set_payload((archivo_adjunto).read())
# Codificamos el objeto en BASE64
encoders.encode_base64(adjunto_MIME)
# Agregamos una cabecera al objeto
adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
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
