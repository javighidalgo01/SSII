import java.io.IOException;

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
			SSLSocket socket = (SSLSocket) serverSocket.accept();
    		new Thread(new StoreInput(socket)).start();
		} 
	}

	// handle exception communicating with client
	catch (IOException ioException) {
		ioException.printStackTrace();
	}

	}

}
