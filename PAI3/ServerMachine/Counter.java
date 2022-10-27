public class Counter implements Runnable {
   	public void run() {

		while(true){
			System.out.print("Conexiones simultaneas: " + MsgSSLServerSocket.n_connections + "            \r");
			try{
                        Thread.sleep(500);
                        }catch(InterruptedException e){}
		}
        }
}
