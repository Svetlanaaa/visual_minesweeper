import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {
   //Чтение данных анонимного тестирования из файла
   public static ArrayList<int[]> getLearningData() throws FileNotFoundException {
       Scanner scanner = new Scanner(new File("C:\\javaProjects\\MACH-IV\\mach.txt"));
       ArrayList<int[]> test = new ArrayList<>();
       while (scanner.hasNextLine()) {
           String s = scanner.nextLine();
           s = s.replaceAll("\\,", " ");
           int[] mas = new int[24];
           Scanner scannerNew = new Scanner(s);
           for (int i = 0; i < mas.length; i++) {
               mas[i] = scannerNew.nextInt();
           }
           test.add(mas);
       }
       return test;
   }

   public static int calcError(ArrayList<int[]> data, NeuronNet net){
       int sum = 0;//количество верно определенный примеров из выборки
       for (int i = 0; i < data.size(); i++) {
           int[] test = data.get(i);
           int[] sample = new int[20];
           for (int j = 0; j < 20; j++)
               sample[j] = test[j];

           //номер группы, к которой сеть отнесла данный пример
           int i2 = net.getResult(sample);

           int i1 = 0;//правильный номер группы
           if (test[20] > 63)
               if (test[20] < 87) i1 = 1;
               else i1 = 2;
           //если воспали, то увеличиваем число верно определенный примеров
           if (i1 == i2) sum++;
       }
       return (data.size() - sum);
   }

   public static void main(String[] args) throws FileNotFoundException {
       ArrayList<int[]> learningData = getLearningData(); //обучающая выборка
       ArrayList<int[]> testingData = new ArrayList<>();//тестируемая выборка
       //распределение общей выборки на обучающую и тестируемую
       int size = learningData.size()/2;
       for (int i = 0; i < size; i++) {
           int[] a = learningData.get(0);
           testingData.add(a);
           learningData.remove(0);
       }

       //создание трехслойной нейронной сети со слоями размеров 20, 8, 3 нейрона
       NeuronNet net = new NeuronNet(3, 20, 8, 3);
       //обучение 1000 эпох
       for (int k = 0; k < 1000; k++) {
           for (int i = 0; i < learningData.size(); i++) {
               int[] test = learningData.get(i);//i-ый тест из выборки
               int[] sample = new int[23];
               for (int j = 0; j < 20; j++) sample[j] = test[j];
               //определение группы, к которой отнесен результат теста
               if (test[20] < 63) sample[20] = 1;
               else if (test[20] < 87) sample[21] = 1;
                   else sample[22] = 1;
               //обучение сети на этом примере
               net.learn(sample);
               }
           }
           System.out.printf("Ошибка обучения: %1.2f%%\n", ((double) calcError(learningData, net) / (double) learningData.size()) * 100.0);
           System.out.printf("Ошибка обобщения: %1.2f%%", ((double) calcError(testingData,net) / (double) testingData.size()) * 100.0);
       }
}

