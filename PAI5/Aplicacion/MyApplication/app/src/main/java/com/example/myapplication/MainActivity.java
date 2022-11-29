package com.example.myapplication;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.res.Resources;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.CheckBox;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;

import java.security.InvalidKeyException;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.Signature;
import java.security.SignatureException;
import java.util.ArrayList;
import java.util.List;


public class MainActivity extends AppCompatActivity {

    // Setup Server information
    protected static String server = "192.168.130.27";
    protected static int port = 4444;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        disableStrictMode();
        setContentView(R.layout.activity_main);

        // Capturamos el boton de Enviar
        View button = findViewById(R.id.button_send);

        // Llama al listener del boton Enviar
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDialog();
            }
        });


    }

    private void disableStrictMode(){
        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8)
        {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                    .permitAll().build();
            StrictMode.setThreadPolicy(policy);
            //your codes here

        }
    }

    // Creación de un cuadro de dialogo para confirmar pedido
    private void showDialog() throws Resources.NotFoundException {
        final CheckBox sabanas = (CheckBox) findViewById(R.id.checkBox_sabanas);
        final CheckBox sillas = (CheckBox) findViewById(R.id.checkBox_sillas);
        final CheckBox mesas = (CheckBox) findViewById(R.id.checkBox_mesas);
        final CheckBox camas = (CheckBox) findViewById(R.id.checkBox_camas);

        if (!sabanas.isChecked() && !sillas.isChecked() && !mesas.isChecked() && !camas.isChecked()) {
            // Mostramos un mensaje emergente;
            Toast.makeText(getApplicationContext(), "Selecciona al menos un elemento", Toast.LENGTH_SHORT).show();
        } else {
            new AlertDialog.Builder(this)
                    .setTitle("Enviar")
                    .setMessage("Se va a proceder al envio")
                    .setIcon(android.R.drawable.ic_dialog_alert)
                    .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {

                                // Catch ok button and send information
                                public void onClick(DialogInterface dialog, int whichButton) {
                                    try {
                                        String message = "";
                                        byte[] firma = null;
                                        KeyPairGenerator kgen = KeyPairGenerator.getInstance("RSA");
                                        kgen.initialize(2048);
                                        KeyPair keys = kgen.generateKeyPair();
                                        byte[] publicKey = keys.getPublic().getEncoded();

                                        if(sabanas.isChecked()){
                                            message = "SAB:";
                                        }
                                        if(sillas.isChecked()){
                                            message = message + "SIL:";
                                        }
                                        if(mesas.isChecked()){
                                            message = message + "MES:";
                                        }
                                        if(camas.isChecked()){
                                            message = message + "CAM:";
                                        }

                                        Signature sg = Signature.getInstance("SHA256withRSA");
                                        sg.initSign(keys.getPrivate());
                                        sg.update(message.getBytes());
                                        firma = sg.sign();

                                        // 3. Enviar los datos

                                        String response = "";
                                        MessageSender ms = new MessageSender(server, port, message, firma, publicKey);
                                        try {
                                            response = ms.sendAndGetReply();
                                        } catch (IOException e) {
                                            response = "Error al enviar";
                                            e.printStackTrace();
                                        }
                                        Toast.makeText(MainActivity.this, response, Toast.LENGTH_LONG).show();

                                    }catch(NoSuchAlgorithmException e) {
                                        System.out.println("Something is wrong");
                                    }

                                    catch (SignatureException e) {

                                        System.out.println("Exception thrown : " + e);
                                    }

                                    catch (InvalidKeyException e) {

                                        System.out.println("Exception thrown : " + e);
                                    }




                                }
                            }

                    )
                    .

                            setNegativeButton(android.R.string.no, null)

                    .

                            show();
        }
    }


}
