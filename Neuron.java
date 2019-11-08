public class Neuron {
    private double[] w; //веса нейрона
    private double y;//выходное значение нейрона
    private Neuron[] inputs; //предыдущий слой
    private double x0, w0; //смещение
    private double d = 0.0;//текущее значение ошибки

    //Добавление ошибки, полученной от одного из нейронов слоем выше
    public void addD(double _d){
        d+=_d;
    }
    //Обнулить значение ошибки для новой итерации
    public void clearD(){
        d= 0.0;
    }
    //Получить значение ошибки для данного нейрона на данной итерации
    public double getD() {
        return d;
    }
    //Подача в входной нейрон входного значения
    public void setY(double y) {
        this.y = y;
    }
    //Инициализация нейрона скрытого или выходного слоя
    public Neuron(Neuron[] l){
        inputs = l;
        w = new double[inputs.length];
        for(int i =0; i< inputs.length; i++){
            w[i] = Math.random() -0.5;//случайная инициализация весов
        }
        this.x0 = 1;
        this.w0 = Math.random() -0.5;
    }
    //Инициализация нейрона входного слоя
    public Neuron() {
        inputs = null;
    }
    //Изменение весов
    public void modify(double d, double a){
        for(int i = 0; i < w.length; i++){
            w[i] += a * d * inputs[i].y;
        }
        w0 += a * d * w0;
    }
    //Расчет значения net
    private double net(){
        double net = 0;
        for (int i = 0; i < inputs.length; i++) {
            net += w[i] * inputs[i].getY();
        }
        net += x0 * w0;
        return net;
    }
    //Сигмоидная функция. Получение выходного значения нейрона
    public double f() {
        double y = 1.0 / (1.0 + Math.exp(-1 * net()));
        this.y = y;
        return y;
    }
    public Neuron[] getInputs() {
        return inputs;
    }
    public double[] getW() { return w; }
    public double getY() { return y; }
}
