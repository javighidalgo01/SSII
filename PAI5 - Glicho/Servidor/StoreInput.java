import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class StoreInput implements Runnable {
	private final Socket socket; // initialize in const'r

	public void run() {
		try {
			Server.n_connections++;
			BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			String msg = input.readLine();

			PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
			/*String[] in = msg.split(":");
			if (in.length >= 3) {
				String user = in[0];
				String pass = in[1];
				String message = "";
				for (int i = 2; i < in.length; i++) {
					message = i > 2 ? message + ":" + in[i] : message + in[i];
				}
				try {
					FileWriter fileWriter = new FileWriter("Messages.txt", true);
					PrintWriter printWriter = new PrintWriter(fileWriter);
					printWriter.println("User: " + user + "\nPassword: " + pass + "\nMessage: " + message + "\n\n");
					printWriter.close();
				} catch (IOException e) {
					System.out.println(e);
				}
				output.println("Your credentials and message has been stored");
			} else {
				System.out.println("xdd");
				output.println("Error, you should enter a user, a password and a message separated by colons");
			}
			*/
			output.println(msg);
			
			output.close();
			input.close();
			socket.close();
			System.out.println("Mensaje: " + msg);
			System.out.println("Conexion cerrada");
			Server.n_connections--;
		} catch (IOException ioException) {
			ioException.printStackTrace();
		}

	}

	public StoreInput(Socket socket) {
		this.socket = socket;
	}
}
