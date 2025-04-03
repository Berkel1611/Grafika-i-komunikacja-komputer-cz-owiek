import javax.swing.*;
import java.awt.event.*;
import java.awt.event.KeyEvent;
import java.awt.*;
import java.awt.geom.GeneralPath;
import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

public class MainPanel extends JPanel implements MouseMotionListener {
    private final Map<String, BezierSurfaces> objects = new LinkedHashMap<>(); // Mapa przechowująca obiekty BezierSurfaces
    private int lastX, lastY; // Ostatnia pozycja myszy
    private String selectedObjectName; // Nazwa aktualnie wybranego obiektu
    private final Color defaultColor = Color.BLACK; // Domyślny kolor obiektu
    private final Color selectedColor = Color.BLUE; // Kolor zaznaczonego obiektu

    public MainPanel() {
        addMouseMotionListener(this); // Dodanie nasłuchiwacza ruchu myszy
        setupKeyBindings(); // Ustawienie skrótów klawiszowych
        setFocusable(true); // Umożliwia odbieranie zdarzeń klawiatury
    }

    private void setupKeyBindings() {
        InputMap inputMap = getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW);
        ActionMap actionMap = getActionMap();

        // Przypisanie klawiszy strzałek do przesuwania obiektów
        bindKey(inputMap, actionMap, "move.left", KeyEvent.VK_LEFT, -10, 0);
        bindKey(inputMap, actionMap, "move.right", KeyEvent.VK_RIGHT, 10, 0);
        bindKey(inputMap, actionMap, "move.up", KeyEvent.VK_UP, 0, -10);
        bindKey(inputMap, actionMap, "move.down", KeyEvent.VK_DOWN, 0, 10);
    }

    private void bindKey(InputMap inputMap, ActionMap actionMap, String actionName,
                         int keyCode, int dx, int dy) {
        KeyStroke keyStroke = KeyStroke.getKeyStroke(keyCode, 0);
        inputMap.put(keyStroke, actionName);
        actionMap.put(actionName, new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (selectedObjectName != null) {
                    objects.get(selectedObjectName).movePoints(dx, dy); // Przesunięcie wybranego obiektu
                    repaint(); // Odświeżenie ekranu
                }
            }
        });
    }

    public Set<String> getObjectsNames() {
        return objects.keySet(); // Zwraca zbiór nazw obiektów
    }

    public String getSelectedObjectName() {
        return selectedObjectName; // Zwraca nazwę zaznaczonego obiektu
    }

    public boolean hasObjects() {
        return !objects.isEmpty(); // Sprawdza, czy istnieją obiekty na panelu
    }

    private void moveSelected(int dx, int dy) {
        BezierSurfaces obj = objects.get(selectedObjectName);
        if (obj != null) {
            obj.movePoints(dx, dy); // Przesunięcie obiektu
            repaint(); // Odświeżenie ekranu
        }
    }

    public void addObject(String filename, String objectName) throws IOException {
        BezierSurfaces newObj = new BezierSurfaces(filename);
        objects.put(objectName, newObj); // Dodanie nowego obiektu

        if(selectedObjectName != null)
            objects.get(selectedObjectName).setColor(defaultColor); // Przywrócenie koloru poprzedniego obiektu

        selectedObjectName = objectName;
        newObj.setColor(selectedColor); // Ustawienie koloru dla nowo wybranego obiektu

        repaint(); // Odświeżenie ekranu
    }

    public void removeSelectedObject() {
        if (selectedObjectName == null) return;

        objects.remove(selectedObjectName); // Usunięcie wybranego obiektu
        if (!objects.isEmpty()) {
            selectedObjectName = objects.keySet().iterator().next(); // Wybór następnego obiektu
            objects.get(selectedObjectName).setColor(selectedColor); // Ustawienie koloru dla nowego wyboru
        } else {
            selectedObjectName = null;
        }
        repaint(); // Odświeżenie ekranu
    }

    public void selectObject(String objectName) {
        if(objects.containsKey(objectName)) {
            if(selectedObjectName != null) {
                objects.get(selectedObjectName).setColor(defaultColor); // Przywrócenie koloru poprzedniego obiektu
            }
            selectedObjectName = objectName;
            objects.get(objectName).setColor(selectedColor); // Ustawienie koloru dla nowo wybranego obiektu
            repaint(); // Odświeżenie ekranu
        }
    }

    @Override
    public void mouseDragged(MouseEvent e) {
        if(selectedObjectName == null) return;

        int dx = e.getX() - lastX;
        int dy = e.getY() - lastY;

        // Obrót obiektu wokół osi X i Y w zależności od ruchu myszy
        objects.get(selectedObjectName).
                rotatePoints(Math.toRadians(dy), 0, 0);
        objects.get(selectedObjectName).
                rotatePoints(0, Math.toRadians(dx), 0);

        lastX = e.getX();
        lastY = e.getY();
        repaint(); // Odświeżenie ekranu
    }

    @Override
    public void mouseMoved(MouseEvent e) {
        lastX = e.getX();
        lastY = e.getY();
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;

        g2.translate(getWidth() / 2, getHeight() / 2); // Środek panelu jako punkt odniesienia
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON); // Wygładzanie krawędzi

        GeneralPath path;
        for(BezierSurfaces obj : objects.values()) {
            path = new GeneralPath();
            obj.setPath(path);
            g2.setColor(obj.getColor());
            g2.draw(path); // Rysowanie obiektu BezierSurfaces
        }
    }
}
