import java.io.*;
import java.net.*;

public class Server {

    public static Integer n_connections = 0;
    public static void main(String[] args) {
        try {
            ServerSocket ss = new ServerSocket(4444);
            System.err.println("Server listening...");
            // new Thread(new Counter()).start();
            while (true) {
                Socket s = (Socket) ss.accept();
                new Thread(new SocketThread(s)).start();
            }
        }

        // handle exception communicating with client
        catch (IOException ioException) {
            ioException.printStackTrace();
        }

    }
}