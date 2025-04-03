import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;

public class Main {
    private int objectCounter = 0; // Licznik obiektów dodanych do sceny
    private ButtonGroup objectGroup = new ButtonGroup(); // Grupa przycisków radiowych do wyboru obiektu

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                new Main().createAndShowGUI(); // Uruchomienie GUI w wątku Swing
            } catch (Exception e) {
                JOptionPane.showMessageDialog(null,
                        "Error: " + e.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
    }

    private void createAndShowGUI() {
        JFrame frame = new JFrame("Zastawa"); // Główne okno aplikacji
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        MainPanel mainPanel = new MainPanel(); // Główny panel rysujący obiekty
        frame.add(mainPanel, BorderLayout.CENTER);

        JPanel controlPanel = createControlPanel(mainPanel); // Panel z przyciskami sterującymi
        frame.add(controlPanel, BorderLayout.SOUTH);

        frame.setSize(1000, 800);
        frame.setLocationRelativeTo(null); // Wyśrodkowanie okna na ekranie
        frame.setVisible(true);

        // Ustawienie fokusu na główny panel po kliknięciu okna
        frame.addWindowFocusListener(new WindowAdapter() {
            @Override
            public void windowGainedFocus(WindowEvent e) {
                mainPanel.requestFocusInWindow();
            }
        });
    }

    private JPanel createControlPanel(MainPanel mainPanel) {
        JPanel panel = new JPanel(new GridLayout(2, 1)); // Panel sterujący podzielony na dwie sekcje

        // Panel z przyciskami do dodawania i usuwania obiektów
        JPanel buttonPanel = new JPanel(new FlowLayout());

        JButton addTeapotBtn = createAddButton(mainPanel, "Teapot", "czajnik");
        JButton addSpoonBtn = createAddButton(mainPanel, "Spoon", "lyzka");
        JButton addCupBtn = createAddButton(mainPanel, "Cup", "filizanka");

        JButton removeBtn = new JButton("Remove selected");
        removeBtn.addActionListener(e -> {
            mainPanel.removeSelectedObject(); // Usunięcie wybranego obiektu
            updateObjectButtons(mainPanel); // Aktualizacja listy dostępnych obiektów
        });

        buttonPanel.add(addTeapotBtn);
        buttonPanel.add(addSpoonBtn);
        buttonPanel.add(addCupBtn);
        buttonPanel.add(removeBtn);

        // Panel z przyciskami radiowymi do wyboru obiektów
        JPanel radioPanel = new JPanel(new FlowLayout());
        panel.add(buttonPanel);
        panel.add(radioPanel);

        return panel;
    }

    private JButton createAddButton(MainPanel mainPanel, String displayName, String filename) {
        JButton button = new JButton("Add " + displayName); // Tworzenie przycisku dodającego obiekt
        button.addActionListener(e -> {
            try {
                String objName = displayName + "-" + ++objectCounter; // Generowanie unikalnej nazwy obiektu
                mainPanel.addObject(filename, objName); // Dodanie obiektu do sceny
                updateObjectButtons(mainPanel); // Aktualizacja listy obiektów
            } catch (IOException e1) {
                JOptionPane.showMessageDialog(null, "Error: " + e1.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        return button;
    }

    private void updateObjectButtons(MainPanel mainPanel) {
        // Pobranie panelu z przyciskami radiowymi
        JPanel radioPanel = (JPanel) ((JPanel) mainPanel.
                getParent().getComponent(1)).getComponent(1);
        radioPanel.removeAll(); // Usunięcie starych przycisków
        objectGroup = new ButtonGroup(); // Nowa grupa przycisków radiowych
        JRadioButton button;

        for(String objName : mainPanel.getObjectsNames()) {
            button = new JRadioButton(objName); // Tworzenie przycisku radiowego dla każdego obiektu
            button.addActionListener(e -> mainPanel.selectObject(objName)); // Ustawienie obiektu jako wybranego
            objectGroup.add(button);
            radioPanel.add(button);

            if(objName.equals((mainPanel.getSelectedObjectName()))) {
                button.setSelected(true); // Zaznaczenie aktualnie wybranego obiektu
            }
        }

        radioPanel.revalidate(); // Odświeżenie panelu
        radioPanel.repaint();
    }
}
