package Proxy;

import java.rmi.RemoteException;
import java.util.*;

public class GumballMonitor {
    GumballMachineRemote machine;

    public GumballMonitor(GumballMachineRemote machine) {
        this.machine = machine;
}

    public void report() {
        try {
            System.out.println("위치: " + this.machine.getLocation());
            System.out.println("재고: " + this.machine.getCount());
            System.out.println("상태: " + this.machine.getState());
        } catch (RemoteException e) {
            e.printStackTrace();
        }

    }
}
