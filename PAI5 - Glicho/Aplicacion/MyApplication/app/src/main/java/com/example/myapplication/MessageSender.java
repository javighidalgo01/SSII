package com.example.myapplication;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

import javax.net.ssl.*;

public class MessageSender {

    private String ip;
    private String msg;
    private String response;

    public String send() throws IOException {
        try {
            Socket socket = new Socket(ip,6666);
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
            //String msg = JOptionPane.showInputDialog(null, "Enter User:Passsword:Message");

            // send user name to server
            output.println(msg);
            output.flush();

            // read response from server
            response = input.readLine();

            // display response to user

            // clean up streams and Socket
            output.close();
            input.close();
            socket.close();
            return response;

        } // end try

        // handle exception communicating with server
        catch (IOException ioException) {
            ioException.printStackTrace();
        }

        return response;
    }

    public MessageSender(String ip, String message){
        this.ip = ip;
        this.msg = message;
    }
}
