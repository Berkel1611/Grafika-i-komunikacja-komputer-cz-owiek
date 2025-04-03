import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.geom.GeneralPath;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Initials extends JPanel {
    // Litera B
    private final int[][][] pointsB = {
            {{100, 100}, {70, 260}}, // Pozioma linia
            {{100, 310, 250, 150}, {260, 325, 130, 170}}, // Dolne wybrzuszenie
            {{150, 250, 310, 100}, {170, 200, 40, 70}}, // Górne wybrzuszenie
            {{120, 120}, {190, 240}}, // Pozioma linia dolnej dziury
            {{120, 260, 230, 120}, {240, 290, 150, 190}}, // Wybrzuszenie dolnej dziury
            {{120, 120}, {90, 150}}, // Pozioma linia górnej dziury
            {{120, 260, 230, 120}, {90, 75, 180, 150}}, // Wybrzuszenie górnej dziury
    };
    // Litera K
    private final int[][][] pointsK = {
            {{320, 320}, {70, 270}},// Pionowa linia 1
            {{340, 340}, {70, 150}},  // Pionowa linia 2.1
            {{340, 340}, {190, 270}},  // Pionowa linia 2.2
            {{320, 340}, {70, 70}},
            {{320, 340}, {270, 270}},
            {{340, 420}, {150, 70}},
            {{420, 450}, {70, 70}},
            {{350, 450}, {170, 70}},
            {{350, 450}, {170, 270}},
            {{420, 450}, {270, 270}},
            {{420, 340}, {270, 190}}
    };
    Initials() {
        readFromFile("KrzyweBeziera/coords.txt");
    }
    private Color color = Color.BLACK;

    public void saveToFile(String filename) {
        try(BufferedWriter bw = new BufferedWriter(new FileWriter(filename))) {
            int[][][][] points = {pointsB, pointsK};
            for(int[][][] inital : points) {
                for(int[][] line : inital) {
                    for (int[] coords : line) {
                        for (int point : coords)
                            bw.write(point + " ");
                    }
                    bw.write("\n");
                }
                bw.write("\n");
            }
            bw.write("\n");
            bw.flush();
            bw.close();

            Path path = Paths.get(filename);
            String content = new String(Files.readAllBytes(path));
            content = content.trim();
            Files.write(path, content.getBytes());
        } catch(IOException e) {
            JOptionPane.showMessageDialog(null, e.getMessage());
        }
    }
    public void readFromFile(String filename) {
        try(BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String[] line1;
            String line;
            int[][][] arr = pointsB;
            int i = 0;
            while((line = br.readLine()) != null) {
                line1 = line.trim().split(" ");
                if(line1.length < 2) {
                    arr = pointsK;
                    i = 0;
                    continue;
                }
                int n = line1.length/2;
                for(int j = 0; j < n; j++) {
                    arr[i][0][j] = Integer.parseInt(line1[j]);
                    arr[i][1][j] = Integer.parseInt(line1[j+n]);
                }
                i++;
            }
        } catch (IOException e) {
            JOptionPane.showMessageDialog(null, e.getMessage());
        }
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D) g;
        g2.setStroke(new BasicStroke(5));
        g2.setColor(color);

        GeneralPath path = new GeneralPath();

        setPath(pointsB, path);
        setPath(pointsK, path);

        g2.draw(path);
    }

    private void setPath(int[][][] points, GeneralPath path) {
        int[] point = new int[2];

        for (int[][] line : points) {
            path.moveTo(line[0][0], line[1][0]);
            for (double t = 0; t <= 1; t += 0.1) {
                point[0] = calcBezier(line[0], t);
                point[1] = calcBezier(line[1], t);
                path.lineTo(point[0], point[1]);
            }
        }
    }
    public int calcBezier(int[] coords, double t) {
        double res = 0;
        int n = coords.length-1;
        for(int i = 0; i <= n; i++)
            res += newton(n, i) * Math.pow(1 - t, n - i) *
                    Math.pow(t, i) * coords[i];
        return (int)res;
    }
    public int newton (int n, int k) {
        if (k > n - k) {
            k = n - k;
        }
        long result = 1;
        for (int i = 0; i < k; i++) {
            result = result * (n - i) / (i + 1);
        }
        return (int)result;
    }
    public void changeColor() {
        color = new Color((int)(Math.random() * 0x1000000));
        repaint();
    }
    public void moveLetters(int dx, int dy) {
        movePoints(pointsB, dx, dy, true);
        movePoints(pointsK, dx, dy, true);
        repaint();
    }
    private void movePoints(int[][][] points, double dx, double dy, boolean moveOrScale) {
        for(int i = 0; i < points.length; i++) {
            for(int j = 0; j < points[i][0].length; j++) {
                if(moveOrScale) {
                    points[i][0][j] += dx;
                    points[i][1][j] += dy;
                }
                else {
                    points[i][0][j] *= dx;
                    points[i][1][j] *= dy;
                }
            }
        }
    }
    public void scaleLetters(double sx, double sy) {
        movePoints(pointsB, sx, sy, false);
        movePoints(pointsK, sx, sy, false);
        repaint();
    }
    public void setDefaultCoords() {
        readFromFile("C:\\Users\\Radek\\OneDrive\\Pulpit\\Studia UWB\\Grafika i komunikacja komputer-człowiek\\Labolatoria\\Programy\\Program 1\\KrzyweBeziera\\default.txt");
        repaint();
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame();
        Initials initialsPanel = new Initials();
        JButton colorButton = new JButton("Zmień kolor");
        colorButton.addActionListener(e -> initialsPanel.changeColor());
        JButton saveButton = new JButton("Zapisz");
        saveButton.addActionListener(e -> initialsPanel.saveToFile("KrzyweBeziera/coords.txt"));
        JButton defaultButton = new JButton("Przywróć domyślne");
        defaultButton.addActionListener(e -> initialsPanel.setDefaultCoords());

        colorButton.setFocusable(false);
        saveButton.setFocusable(false);
        defaultButton.setFocusable(false);

        frame.addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_LEFT -> initialsPanel.moveLetters(-10, 0);
                    case KeyEvent.VK_RIGHT -> initialsPanel.moveLetters(10, 0);
                    case KeyEvent.VK_UP -> initialsPanel.moveLetters(0, -10);
                    case KeyEvent.VK_DOWN -> initialsPanel.moveLetters(0, 10);
                    case KeyEvent.VK_PLUS, KeyEvent.VK_EQUALS -> initialsPanel.scaleLetters(1.1, 1.1);
                    case KeyEvent.VK_MINUS -> initialsPanel.scaleLetters(0.9, 0.9);
                }
            }
        });

        frame.add(initialsPanel, BorderLayout.CENTER);
        JPanel buttons = new JPanel();
        buttons.setLayout(new FlowLayout(FlowLayout.CENTER));
        buttons.add(colorButton);
        buttons.add(saveButton);
        buttons.add(defaultButton);
        frame.add(buttons, BorderLayout.SOUTH);

        frame.setFocusable(true);
        frame.requestFocusInWindow();

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 500);
        frame.setVisible(true);
    }
}
