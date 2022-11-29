package com.example.myapplication;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

import javax.net.ssl.*;

public class MessageSender {

    private String ip;
    private int port;
    private String msg;
    private byte[] sign;
    private String response;
    private byte[] publicKey;

    public String sendAndGetReply() throws IOException {
        try {
            Socket socket = new Socket(ip,port);
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
            DataOutputStream dOut = new DataOutputStream(socket.getOutputStream());

            output.println(msg);
            output.flush();
            dOut.writeInt(publicKey.length);
            dOut.write(publicKey);
            dOut.write(sign);
            // read response from server
            response = input.readLine();
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

    public MessageSender(String ip, int port, String message, byte[] firma, byte[] publicKey){
        this.ip = ip;
        this.port = port;
        this.msg = message;
        this.sign = firma;
        this.publicKey = publicKey;
    }
}
