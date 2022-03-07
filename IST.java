// Array Package for manipulating Arrays
import java.util.Arrays;
// Random Package for Generating Random Arrays
import java.util.Random;

// InterpolationSearchTask (IST)
public class IST {
    
    static int arrayLength;
    static int minVal;
    static int maxVal;
    static int key;
    static int bottom;
    static int top;
    static int iBBottom;
    static int iBTop;
    static int numberOfSearches;
    
    // Interpolation Variables
    static int interpolationArrayLength;
    static int interpolationIterationCount;
    static int interpolationDeletedIndexes;
    static float interpolationArrayElimination;
    
    // Interpolation Binary Variables
    static int interpolationBinaryArrayLength;
    static int interpolationBinaryIterationCount;
    static int interpolationBinaryDeletedIndexes;
    static float interpolationBinaryArrayElimination;
    
    // Generate a pseudorandom array of integers
    public static int[] randomArrayGenerator(int arrayLength, int minVal, int maxVal) {
        Random rd = new Random();
        int[] arr = new int[arrayLength];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = rd.nextInt(minVal, maxVal);
        }
        Arrays.sort(arr);
        
        return arr;
    }
    
    // Generate an array as a G.P.
    public static int[] geometricArrayGenerator(int arrayLength, int minVal, int factor) {
        int[] arr = new int[arrayLength];
        arr[0] = minVal;
        for (int i = 1; i < arr.length; i++) {
            arr[i] = arr[i - 1] * factor;
        } 
        return arr;
    }
    
    // Generate an array as an A.P.
    public static int[] arithmeticProgressionArray(int arrayLength, int minVal, int factor) {
        int[] arr = new int[arrayLength];
        arr[0] = minVal;
        for (int i = 1; i < arr.length; i++) {
            arr[i] = arr[0] + (i * factor);
        } 
        return arr;
    }
    
    // Generate an array based on Fibonacci sequence
    public static int[] fibonacciArray(int arrayLength) {
        int[] arr = new int[arrayLength];
        arr[0] = 0;
        arr[1] = 1;
        for (int i = 2; i < arr.length; i++) {
            arr[i] = arr[i - 1] + arr[i - 2];
        }
        return arr;
    }
    
    // Get a pseudorandom key from the array range for use in the search
    public static int randomKeyInArrayRange(int[] arr, int minVal, int maxVal) {
        int randomKey = new Random().nextInt(minVal, maxVal);
        return randomKey;
    }
    
    // Get a pseudorandom key from the array for use in the search
    public static int randomKeyInArray(int[] arr) {
        int randomKey = new Random().nextInt(arr.length);
        return arr[randomKey];
    }
    
    // Use an interpolation search on array to find key
    static void interpolationSearch(int[] arr) {
        
        int i = 0;
        while (arr[i] != key && key >= arr[bottom] && key <= arr[top] && arr[top] != arr[bottom]) {
            interpolationIterationCount++;
            
            // Print input values:
            /*System.out.println("\nTop: " 
                + top + ", Bottom: " + bottom + ", Vbottom: " 
                + arr[bottom] + ", Vtop: " + arr[top] + ", key: " + key);*/
            
            // Search algorithm (integers round to floor by default)
            i = (((top - bottom) * (key - arr[bottom])) / (arr[top] - arr[bottom])) + bottom;
            
            // Successful Search:
            if (arr[i] == key) {
                //System.out.println("\nIteration: " + interpolationIterationCount + " index guess: " + i);
               // System.out.println("Key: " + key + " was found at array index: " 
                //+ i + " on iteration: " + interpolationIterationCount);
                
            }
                
            // Index guess too low:
            if (arr[i] < key) {
                interpolationArrayElimination = ((float)((i + 1) - bottom) / interpolationArrayLength);
                interpolationDeletedIndexes = ((i + 1) - bottom);
                //System.out.println("Iteration: " + interpolationIterationCount + " index guess: " + i);
                //System.out.println("Percentage of array eliminated: " + arrayElimination);
                //System.out.println("Number of eliminated indexes: " + deletedIndexes);
                interpolationArrayLength -= interpolationDeletedIndexes;
                bottom = (i + 1);
            }
            
            // Index guess too high:
            if (arr[i] > key) {
                interpolationArrayElimination = ((float)(top - (i - 1)) / interpolationArrayLength);
                interpolationDeletedIndexes = (top - (i - 1));
                //System.out.println("Iteration: " + interpolationIterationCount + " index guess: " + i);
                //System.out.println("Percentage of array eliminated: " + arrayElimination);
                //System.out.println("Number of eliminated indexes: " + deletedIndexes);
                interpolationArrayLength -= interpolationDeletedIndexes;
                top = (i - 1);
            }
            
        }
        
        // Test outcome
        if ((key < arr[bottom] || key > arr[top]) && interpolationIterationCount == 0) {
            //System.out.println("Key: " + key + " was outside of array range");
        }
        else if (key < arr[bottom] || key > arr[top] && interpolationIterationCount > 0) {
            //System.out.println("Key: " + key + " was not found in the array after " 
                    //+ interpolationIterationCount + " iteration(s). (Outside modified range)");
        }
        else if (arr[top] == arr[bottom] && key == arr[top]) {
            //System.out.println("Key: " + key + " was found in the array after " 
                    //+ interpolationIterationCount + " iteration(s).(top = bottom value = key)");
        }
        else if (arr[top] == arr[bottom] && key != arr[top]) {
           // System.out.println("Key: " + key + " was not found in the array after " 
                    //+ interpolationIterationCount + " iteration(s).(top = bottom value != key)");
        }
        else if (arr[i] == key && interpolationIterationCount == 0) {
            interpolationIterationCount++;
            //System.out.println("Key: " + key + " was found in the array after " 
                   // + interpolationIterationCount + " iteration(s). (i == 0)");
        }
        
    }
    
    // Use hybrid search on array to find key
    static void interpolationBinarySearch(int[] arr) {

        int i = 0;
        while (arr[i] != key && key >= arr[iBBottom] && key <= arr[iBTop] && arr[iBTop] != arr[iBBottom]) {
            interpolationBinaryIterationCount++;
            // Print input values:
            //System.out.println("\nTop: " + iBTop + ", Bottom: " + iBBottom + ", Vbottom: " + arr[iBBottom] + ", Vtop: " + arr[iBTop] + ", key: " + key);
            
            // Search algorithm (integers round to floor by default)
            i = (((iBTop - iBBottom) * (key - arr[iBBottom])) / (arr[iBTop] - arr[iBBottom])) + iBBottom;
            
            // Successful Search:
            if (arr[i] == key) {
                //System.out.println("\nIteration: " + interpolationIterationCount + " index guess: " + i);
                //System.out.println("Key: " + key + " was found at array index: " 
                //+ i + " on iteration: " + interpolationBinaryIterationCount);
                
            }
                
            // Index guess too low:
            if (arr[i] < key) {
                interpolationBinaryArrayElimination = ((float)((i + 1) - iBBottom) / interpolationBinaryArrayLength);
                interpolationBinaryDeletedIndexes = ((i + 1) - iBBottom);
                //System.out.println("Iteration: " + interpolationBinaryIterationCount + " index guess: " + i);
                interpolationBinaryArrayLength -= interpolationBinaryDeletedIndexes;
                iBBottom = (i + 1);
                // Check array elimination and either implement binary search or continue while loop
                if (interpolationBinaryArrayElimination < 0.25f) {
                    binarySearch(arr);
                }
                   
            }
            
            // Index guess too high:
            if (arr[i] > key) {
                interpolationBinaryArrayElimination = ((float)(iBTop - (i - 1)) / interpolationBinaryArrayLength);
                interpolationBinaryDeletedIndexes = (iBTop - (i - 1));
                //System.out.println("Iteration: " + interpolationBinaryIterationCount + " index guess: " + i);
                interpolationBinaryArrayLength -= interpolationBinaryDeletedIndexes;
                iBTop = (i - 1);
                // Check array elimination and either implement binary search or continue while loop
                if (interpolationBinaryArrayElimination < 0.25f) {
                    binarySearch(arr);
                }
                 
                
            }
            
        }
        
        // Test outcome
        if ((key < arr[iBBottom] || key > arr[iBTop]) && interpolationBinaryIterationCount == 0) {
            //System.out.println("Key: " + key + " was outside of array range");
        }
        else if (key < arr[iBBottom] || key > arr[iBTop] && interpolationBinaryIterationCount > 0) {
            //System.out.println("Key: " + key + " was not found in the array after " 
                    //+ interpolationBinaryIterationCount + " iteration(s). (Outside modified range)");
        }
        else if (arr[iBTop] == arr[iBBottom] && key == arr[iBTop]) {
            //System.out.println("Key: " + key + " was found in the array after " 
                   // + interpolationBinaryIterationCount + " iteration(s).(top = bottom value = key)");
        }
        else if (arr[iBTop] == arr[iBBottom] && key != arr[iBTop]) {
            //System.out.println("Key: " + key + " was not found in the array after " 
                   // + interpolationBinaryIterationCount + " iteration(s).(top = bottom value != key)");
        }
        else if (arr[i] == key && interpolationBinaryIterationCount == 0) {
            interpolationBinaryIterationCount++;
            //System.out.println("Key: " + key + " was found in the array after " 
                   // + interpolationBinaryIterationCount + " iteration(s). (i == 0)");
        }
        
    }
    
    // Binary search function
    static void binarySearch(int[] arr) {
       
       //System.out.println("\nTop: " + iBTop + ", Bottom: " + iBBottom + ", Vbottom: " + arr[iBBottom] + ", Vtop: " + arr[iBTop]);
       int mid = (iBBottom + iBTop) / 2;
       
       if (arr[mid] == key) {
            interpolationBinaryIterationCount++;
       }
       
       if (arr[mid] > key) {
            interpolationBinaryIterationCount++;
            //System.out.println("Iteration: " + interpolationBinaryIterationCount + " index guess: " + mid);
            //System.out.println("Index guess too high. Top value updated from: " + iBTop + " to: " + (mid - 1));
            interpolationBinaryArrayElimination = ((float)(iBTop - (mid - 1)) / interpolationBinaryArrayLength);
            interpolationBinaryDeletedIndexes = (iBTop - (mid - 1));
            interpolationBinaryArrayLength -= interpolationBinaryDeletedIndexes;
            iBTop = mid - 1;
       }
       
       if (arr[mid] < key) {
            interpolationBinaryIterationCount++;
            //System.out.println("Iteration: " + interpolationBinaryIterationCount + " index guess: " + mid);
            //System.out.println("Index guess too low. Bottom value updated from: " + iBBottom + " to: " + (mid + 1));
            interpolationBinaryArrayElimination = ((float)((mid + 1) - iBBottom) / interpolationBinaryArrayLength);
            interpolationBinaryDeletedIndexes = ((mid + 1) - iBBottom);
            interpolationBinaryArrayLength -= interpolationBinaryDeletedIndexes;
            iBBottom = mid + 1;
       }
   
       
   }
    
    // Method to call search algorithms
    static int[] searchAlgorithms(int[] arr) {
        
        // Initialise search variables
        interpolationIterationCount = 0;
        interpolationDeletedIndexes = 0;
        interpolationArrayElimination = 0.00f;
        interpolationBinaryIterationCount = 0;
        interpolationBinaryDeletedIndexes = 0;
        interpolationBinaryArrayElimination = 0.00f;
        interpolationArrayLength = arrayLength;
        interpolationBinaryArrayLength = arrayLength;
        bottom = 0;
        top = arrayLength - 1;
        iBBottom = 0;
        iBTop = arrayLength - 1;
        
        // Generate a key to be searched
        key = randomKeyInArray(arr);
        
        // Call the interpolation search 
        //System.out.println("\n -- Interpolation Search -- ");
        interpolationSearch(arr);
        
        // Call the hybrid search 
        //System.out.println("\n -- Interpolation Binary Search -- ");
        interpolationBinarySearch(arr);
        
        return {key, interpolationIterationCount, interpolationBinaryIterationCount};
        
    }
    
    
    public static void main(String[] args) {
        
        // Array parameters
        arrayLength = 30;
        minVal = 1;
        maxVal = 500;
        
        // Generate array
        //int[] randArray = randomArrayGenerator(arrayLength, minVal, maxVal);
        //int[] gPArray = geometricArrayGenerator(arrayLength, minVal, 2);
        //int[] aPArray = arithmeticProgressionArray(arrayLength, minVal, 4);
        int[] fibArray = fibonacciArray(arrayLength);
        
        int[] arr = fibArray;
        
        // Print array
        System.out.println("Array: " + Arrays.toString(arr));
        
        // Number of searches to be completed
        numberOfSearches = 40;

        // Arrays to capture results of searches
        int[] keys = new int[numberOfSearches];
        int[] interpolationIterationCounts = new int[numberOfSearches];
        int[] interpolationBinaryIterationCounts = new int[numberOfSearches];
        
        // Initiate search as many times as specified by numberOfSearches
        for (int i = 1; i <= numberOfSearches; i++) {
            //System.out.println("\nSearch number: " + i);
            // Call search algorithms
            int[] searchResults = searchAlgorithms(arr);
            //System.out.println(Arrays.toString(searchResults));
            keys[i - 1] = searchResults[0];
            interpolationIterationCounts[i - 1] = searchResults[1];
            interpolationBinaryIterationCounts[i - 1] = searchResults[2];
            
        }
        System.out.println("Keys:  " + Arrays.toString(keys));
        System.out.println("Interpolation Search Results:  " + Arrays.toString(interpolationIterationCounts));
        System.out.println("Interpolation Binary Search Results: " + Arrays.toString(interpolationBinaryIterationCounts));
        
      
    }
}
