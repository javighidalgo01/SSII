import java.io.*;
import java.net.*;

public class Server {

    public static Integer n_connections = 0;
    public static void main(String[] args) {
        try {
            ServerSocket ss = new ServerSocket(6666);
            System.err.println("Waiting connection...");
            // new Thread(new Counter()).start();
            while (true) {
                Socket s = (Socket) ss.accept();
                System.out.println("Conexion iniciada");
                new Thread(new StoreInput(s)).start();
            }
        }

        // handle exception communicating with client
        catch (IOException ioException) {
            ioException.printStackTrace();
        }

    }
}