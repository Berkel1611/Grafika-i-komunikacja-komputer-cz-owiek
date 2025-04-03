public class Rotations3D {
    // Obrót punktu wokół osi X
    public static double[] rotateX(double x, double y, double z, double angle) {
        double[] cosSin = calcTrigonometrics(angle);
        double newY = y * cosSin[0] - z * cosSin[1];
        double newZ = y * cosSin[1] + z * cosSin[0];
        return new double[]{x, newY, newZ};
    }

    // Obrót punktu wokół osi Y
    public static double[] rotateY(double x, double y, double z, double angle) {
        double[] cosSin = calcTrigonometrics(angle);
        double newX = x * cosSin[0] + z * cosSin[1];
        double newZ = -x * cosSin[1] + z * cosSin[0];
        return new double[]{newX, y, newZ};
    }

    // Obrót punktu wokół osi Z
    public static double[] rotateZ(double x, double y, double z, double angle) {
        double[] cosSin = calcTrigonometrics(angle);
        double newX = x * cosSin[0] - y * cosSin[1];
        double newY = x * cosSin[1] + y * cosSin[0];
        return new double[]{newX, newY, z};
    }

    private static double[] calcTrigonometrics(double angle) {
        return new double[]{Math.cos(angle), Math.sin(angle)};
    }
}
