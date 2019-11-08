//Нейронная сеть
public class NeuronNet {
   int N_INPUTS; //количество входных нейронов
   int N_OUTPUTS;//количество выходных нейронов
   int nLayers;//количество слоев в сети
   Neuron[][] net; //Нейроны сети

   //Инициализация
   public NeuronNet(int nLayers, int... n) {

       this.nLayers = nLayers;
       N_INPUTS = n[0];
       N_OUTPUTS = n[n.length-1];

       net = new Neuron[nLayers][];
       for(int i =0; i<n.length; i++)
           net[i] = new Neuron[n[i]];
       //Создание нейронов входного слоя
       for (int i = 0; i < N_INPUTS; i++){
           net[0][i] = new Neuron();
       }
       //Создание нейронов скрытых и выходного слоев
       for(int i = 1; i<nLayers; i++)
           for(int j=0; j<net[i].length; j++)
               net[i][j]= new Neuron(net[i-1]);
   }

   //Обратное распространение ошибки для скрытых слоев
   public void learnLayers(Neuron[] l, int n){
       double[] d = new double[l.length]; //ошибки этого слоя
       for(int i = 0; i< l.length; i++){
           //вычисление ошибки для i-ого нейрона l-ого слоя
           d[i] = l[i].getD() * l[i].getY() * (1 - l[i].getY());
           //предыдущий слой
           Neuron[] currentInputs = l[i].getInputs();
           //если предыдущий слой - не входной, то
           //передаем нейронам предыдущего слоя вычисленную ошибку
           if (n != 1){
               for(int k = 0; k<currentInputs.length; k++){
                   currentInputs[k].addD(d[i] * l[i].getW()[k]);
               }
           }
       }
       //если предыдущий слой - не входной, то обучаем следующий слой
       if (n != 1){
           learnLayers(net[n-1], n-1);
       }
       //Изменение весов слоя
       for(int i = 0; i< l.length; i++){
           l[i].modify(d[i], 0.5);
           l[i].f();
       }
   }
   //Обучение сети
   public void learn(int[] t) {
       //Обнуление ошибок нейронов, полученных на прошлой итерации
       for(int i = 0; i<net.length;i++)
           for(int j = 0; j< net[i].length; j++)
               net[i][j].clearD();
       //Подача вектора на вход сети
       for(int i = 0; i<N_INPUTS; i++){
           net[0][i].setY(t[i]);
       }
       //Вычисление выходных значений
       for(int i = 1; i < net.length; i++)
           for(int j = 0; j < net[i].length; j++)
               net[i][j].f();
       //Ошибки выходного слоя
       double[] d = new double[N_OUTPUTS];
       for(int i = 0; i<N_OUTPUTS; i++){
           //Для каждого нейрона выходного слоя вычисляем ошибку
           d[i] = net[nLayers-1][i].getY() * (1 -  net[nLayers-1][i].getY()) * (t[i+20] -  net[nLayers-1][i].getY());
           Neuron[] currentInputs = net[nLayers-1][i].getInputs();
           //Распространение ошибки на предыдущий слой
           for(int k = 0; k<currentInputs.length; k++){
               currentInputs[k].addD(d[i] * net[nLayers-1][i].getW()[k]);
           }
       }
       //Обучение предыдущего слоя
       learnLayers(net[nLayers-2], nLayers-2);
   }

   //Результат на выходе
   public int getResult(int[] t){
       //Подача вектора на вход нейронной сети
       for(int i = 0; i<N_INPUTS; i++){
           net[0][i].setY(t[i]);
       }
       //Вычисление выходных значений
       for(int i = 1; i < nLayers; i++)
           for(int j = 0; j < net[i].length; j++)
               net[i][j].f();

       int k=0; //номер выходного нейрона-победителя
       double r = net[nLayers-1][0].getY();
       for(int i=1; i<N_OUTPUTS; i++){
           if (net[nLayers-1][i].getY() > r){
               r = net[nLayers-1][i].getY();
               k = i;
           }
       }
       return k;
   }
}

