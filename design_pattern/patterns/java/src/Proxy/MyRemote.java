package Proxy;

import java.rmi.*;

// Remote는 marker용 인터페이스인데, 메서드가 없다.
public interface MyRemote extends Remote {
    public String sayHello() throws RemoteException;
}
