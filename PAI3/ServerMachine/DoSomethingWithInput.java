import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import javax.net.ssl.*;

public class DoSomethingWithInput implements Runnable {
   		private final SSLSocket socket; //initialize in const'r
   		public void run() {
			try{
			MsgSSLServerSocket.n_connections++;
        		BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			String msg = input.readLine();

			// open PrintWriter for writing data to client
			PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

			if (msg.equals("Hola")) {
				output.println("Welcome to the Server");
			} else {
				output.println("Incorrect message.");
			}
			MsgSSLServerSocket.n_connections--;
			output.close();
			input.close();
			socket.close();
			}catch (IOException ioException) {
				ioException.printStackTrace();
			}
        		
        	}
        	public DoSomethingWithInput(SSLSocket socket){
        		this.socket = socket;
    		}
}

