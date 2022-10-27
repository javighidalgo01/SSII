import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

import java.io.*;

import javax.net.ssl.*;

public class MsgSSLServerSocket {
	/**
	 * @param args
	 * @throws IOException
	 * @throws InterruptedException
	 */
	public static Integer n_connections = 0;
	public static void main(String[] args) throws IOException, InterruptedException {

	try {		
		SSLServerSocketFactory factory = (SSLServerSocketFactory) SSLServerSocketFactory.getDefault();
		SSLServerSocket serverSocket = (SSLServerSocket) factory.createServerSocket(3343);
		System.err.println("Waiting connection...");
		new Thread(new Counter()).start();
		while(true){
			
			//System.err.println("Conexiones simultaneas: " + n_connections);
      			SSLSocket socket = (SSLSocket) serverSocket.accept();
    			new Thread(new DoSomethingWithInput(socket)).start();
    			//System.out.print("\033\143Conexiones simultaneas: " + n_connections);	
		} 
	}

	// handle exception communicating with client
	catch (IOException ioException) {
		ioException.printStackTrace();
	}

	}

}
