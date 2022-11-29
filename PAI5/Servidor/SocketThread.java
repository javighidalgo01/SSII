import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.Signature;
import java.security.SignatureException;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class SocketThread implements Runnable {
	private final Socket socket;

	public void run() {
		try {

			//Leer informacion proporcionada por el cliente
			BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
			DataInputStream dIn = new DataInputStream(socket.getInputStream());
			String msg = input.readLine();
			int length = dIn.readInt();	// read length of incoming message
  			byte[] pk = new byte[length];
    		dIn.readFully(pk, 0, pk.length); // read the message
			PublicKey publicKey = KeyFactory.getInstance("RSA").generatePublic(new X509EncodedKeySpec(pk));
			byte[] sign = new byte[256];
			dIn.readFully(sign, 0, 256); // read the message
			Signature sg = Signature.getInstance("SHA256withRSA");
			sg.initVerify(publicKey);
			sg.update(msg.getBytes());
			Boolean verified = sg.verify(sign);		
			
			

			//escribir en el archivo historico de pedidos
			FileWriter fileWriter = new FileWriter("pedidos.txt", true);
			PrintWriter printWriter = new PrintWriter(fileWriter);
			DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");  
   			LocalDateTime now = LocalDateTime.now();
			printWriter.println(dtf.format(now));
			if(verified){
				printWriter.println("Mensaje Recibido. Firma verificada. Pedido:");
				String pedido = "";
				if(msg.contains("SAB")){
					pedido += "Sabanas. ";
				}
				if(msg.contains("SIL")){
					pedido += "Sillas. ";
				}
				if(msg.contains("MES")){
					pedido += "Mesas. ";
				}
				if(msg.contains("CAM")){
					pedido += "Camas. ";
				}
				printWriter.println(pedido);
				
			}
			else{
				printWriter.println("Mensaje Recibido. Firma no verificada. Pedido no almacenado.");
			}
			printWriter.println("");
			printWriter.close();

			//devolder respuesta al servidor y cerrar socket
			output.println(verified?"Firma Verificada. Peticion Aceptada":"Firma invalida. Peticion Rechazada");			
			output.close();
			input.close();	
			socket.close();
			System.out.println("Se ha procesado un mensaje");

		} catch (IOException ioException) {
			ioException.printStackTrace();
		} catch (InvalidKeyException e) {
			e.printStackTrace();
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		} catch (InvalidKeySpecException e) {
			e.printStackTrace();
		} catch (SignatureException e) {
			e.printStackTrace();
		}

	}

	public SocketThread(Socket socket) {
		this.socket = socket;
	}
}
