public class Counter implements Runnable {
   	public void run() {
		while(true){
			System.out.print("\rConexiones simultaneas: " + MsgSSLServerSocket.n_connections + "       ");
			try{
                Thread.sleep(500);
            }catch(InterruptedException e){}
		}
    }
}
