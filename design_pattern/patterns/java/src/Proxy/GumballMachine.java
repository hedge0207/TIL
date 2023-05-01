package Proxy;

import java.rmi.*;
import java.rmi.server.*;

public class GumballMachine extends UnicastRemoteObject implements GumballMachineRemote {
    private static final long serialVersionUID = 2L;

    public GumballMachine(String location, int count) throws RemoteException{
        // 생성자 코드
    }

    public int getCount() {
        return count;
    }

    public State getState() {
        return state;
    }
    public String getLocation() {
        return location;
    }

    // 기타 메서드
}
