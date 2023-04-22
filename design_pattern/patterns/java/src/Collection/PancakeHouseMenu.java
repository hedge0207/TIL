package Collection;

import java.util.ArrayList;
import java.util.List;
import java.util.Iterator;

public class PancakeHouseMenu {
    List<MenuItem> menuItems;
    
    public  PancakeHouseMenu() {
        menuItems = new ArrayList<MenuItem>();

        addItem("블루베리 팬케이크",
                "블루베리 잼을 바른 팬케이크",
                true,
                3.49);

        addItem("레귤러 팬케이크 세트",
                "달걀 프라이와 소시지가 곁들여진 팬케이크",
                false,
                2.99);

        addItem("와플",
                "취향에 따라 토핑을 올릴 수 있는 와플",
                true,
                3.59);
    }
    
    public void addItem(String name, String description, boolean vegetarian, double price) {
        MenuItem menuItem = new MenuItem(name, description, vegetarian, price);
        menuItems.add(menuItem);
    }
    
    public ArrayList<MenuItem> getMenuItems() {
        return (ArrayList<MenuItem>) menuItems;
    }

    public Iterator<MenuItem> createIterator() {
        return menuItems.iterator()
    }
    
    // 기타 메뉴 관련 메서드
}

