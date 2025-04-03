import java.awt.*;
import java.awt.geom.GeneralPath;
import java.io.*;

public class BezierSurfaces {
    private double[][][][] pkt_kontrolne; // Tablica przechowująca punkty kontrolne powierzchni Beziera
    int p, n, m; // Liczba powierzchni oraz wymiary siatki punktów
    private Color color = Color.BLACK; // Kolor powierzchni

    // Konstruktor wczytujący punkty kontrolne z pliku
    BezierSurfaces(String filename) {
        try (BufferedReader br = new BufferedReader(
                new FileReader(filename))) {

            p = Integer.parseInt(br.readLine()); // Odczyt liczby powierzchni
            String[] values;
            values = br.readLine().trim().split(" ");
            n = Integer.parseInt(values[0])+1; // Odczyt szerokości siatki
            m = Integer.parseInt(values[1])+1; // Odczyt wysokości siatki
            pkt_kontrolne = new double[p][n][m][3]; // Inicjalizacja tablicy punktów

            // Odczyt punktów kontrolnych dla każdej powierzchni
            for(int i = 0; i < p; i++) {
                for(int j = 0; j < n; j++) {
                    for(int k = 0; k < m; k++) {
                        if (!br.ready()) {
                            break;
                        }
                        values = br.readLine().split(" ");
                        if (values.length != 3) {
                            k--; // Pominięcie linii 3 3
                            continue;
                        }
                        try {
                            // Przekształcenie współrzędnych
                            pkt_kontrolne[i][j][k][0] = Double.parseDouble(values[0]) * 100;
                            pkt_kontrolne[i][j][k][1] = Double.parseDouble(values[1]) * -100;
                            pkt_kontrolne[i][j][k][2] = Double.parseDouble(values[2]) * 100 - 100;
                        } catch (NumberFormatException e) {
                            System.err.println(e.getMessage());
                        }
                    }
                }
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    // Ustawienie ścieżki dla rysowania powierzchni Beziera
    public void setPath(GeneralPath path) {
        double[] punkt;

        for(int i = 0; i < pkt_kontrolne.length; i++) {
            punkt = bezierSurface(0, 0, i);
            path.moveTo(punkt[0], punkt[1]); // Przeniesienie do pierwszego punktu
            for (double v = 0; v <= 1; v += 0.1) {
                for (double w = 0; w <= 1; w += 0.1) {
                    punkt = bezierSurface(v, w, i);
                    path.lineTo(punkt[0], punkt[1]); // Rysowanie kolejnych punktów
                }
            }
        }
    }

    // Obliczenie środka masy wszystkich punktów kontrolnych
    private double[] calcCenter() {
        double sx = 0, sy = 0, sz = 0;
        int count = 0;

        for (double[][][] plat : pkt_kontrolne) {
            for (double[][] points : plat) {
                for (double[] point : points) {
                    sx += point[0];
                    sy += point[1];
                    sz += point[2];
                    count++;
                }
            }
        }
        return new double[]{sx / count, sy / count, sz / count};
    }

    // Obracanie punktów kontrolnych wokół środka masy
    public void rotatePoints(double thetaX, double thetaY, double thetaZ) {
        double[] center = calcCenter();

        double[] rotated;
        double x, y, z;
        for(int i = 0; i < p; i++) {
            for(int j = 0; j < n; j++) {
                for(int k = 0; k < m; k++) {
                    x = pkt_kontrolne[i][j][k][0] - center[0];
                    y = pkt_kontrolne[i][j][k][1] - center[1];
                    z = pkt_kontrolne[i][j][k][2] - center[2];

                    rotated = Rotations3D.rotateX(x, y, z, thetaX);
                    rotated = Rotations3D.rotateY(rotated[0], rotated[1], rotated[2], thetaY);
                    rotated = Rotations3D.rotateZ(rotated[0], rotated[1], rotated[2], thetaZ);

                    pkt_kontrolne[i][j][k][0] = rotated[0] + center[0];
                    pkt_kontrolne[i][j][k][1] = rotated[1] + center[1];
                    pkt_kontrolne[i][j][k][2] = rotated[2] + center[2];
                }
            }
        }
    }

    // Przesunięcie punktów kontrolnych w płaszczyźnie XY
    public void movePoints(double dx, double dy) {
        for(int i = 0; i < p; i++) {
            for(int j = 0; j < n; j++) {
                for(int k = 0; k < m; k++) {
                    pkt_kontrolne[i][j][k][0] += dx;
                    pkt_kontrolne[i][j][k][1] += dy;
                }
            }
        }
    }

    // Obliczenie punktu powierzchni Beziera dla danego parametru (v, w)
    private double[] bezierSurface(double v, double w, int p) {
        double x = 0, y = 0, z = 0, bV, bW, weight;

        for (int i = 0; i < n; i++) {
            bV = calcBernstein(i, n, v);
            for(int j = 0; j < m; j++) {
                bW = calcBernstein(j, m, w);
                weight = bV * bW;
                x += weight * pkt_kontrolne[p][i][j][0];
                y += weight * pkt_kontrolne[p][i][j][1];
                z += weight * pkt_kontrolne[p][i][j][2];
            }
        }
        return new double[]{x, y, z};
    }

    // Obliczenie współczynnika Bernsteina
    public double calcBernstein(int i, int n, double v) {
        return newton(n - 1, i) * Math.pow(v, i) * Math.pow(1 - v, (n - 1) - i);
    }

    // Obliczenie symbolu Newtona (n po k)
    public int newton (int n, int k) {
        if (k > n - k) k = n - k;
        int res = 1;
        for (int i = 1; i <= k; i++) {
            res = Math.floorDiv(res * (n - i + 1), i);
        }
        return res;
    }

    public Color getColor() {
        return color;
    }
    public void setColor(Color color) {
        this.color = color;
    }
}
