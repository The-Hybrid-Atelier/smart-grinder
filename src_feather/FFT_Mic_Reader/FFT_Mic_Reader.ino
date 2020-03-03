/* This example shows how to use the FFT library with a circuit playground express.
 *  
 *  The LEDs will map around the circle when frequencies between FREQ_MIN and FREQ_MAX are detected
 */

//#include <Adafruit_CircuitPlayground.h>
#include "Adafruit_ZeroFFT.h"

//this must be a power of 2
#define DATA_SIZE 256

#define NUM_PIXELS 12

//the sample rate
#define FS 22000

//the lowest frequency that will register on the meter
#define FREQ_MIN 600

//the highest frequency that will register on the meter
#define FREQ_MAX 3000

// FFT_INDEX(freq, fs, size) ((int)((float)freq/((float)fs/(float)size))) ///< return the bin index where the specified frequency 'freq' can be found based on the passed sample rate and FFT size
#define MIN_INDEX FFT_INDEX(FREQ_MIN, FS, DATA_SIZE)
#define MAX_INDEX FFT_INDEX(FREQ_MAX, FS, DATA_SIZE)

#define SCALE_FACTOR 32

int16_t pixelData[NUM_PIXELS];
int16_t inputData[DATA_SIZE];

// the setup routine runs once when you press reset:
void setup() {
//  CircuitPlayground.begin();
  Serial.begin(19200);

//  19200, 115200
}

void capture(int16_t *inputData, int16_t buffer_size){
  for(int i=0; i<buffer_size; i++){
    inputData[i] = (int16_t) analogRead(A0);
  }
}

void loop() {
//  CircuitPlayground.mic.capture(inputData, DATA_SIZE);
  capture(inputData, DATA_SIZE);
  /*******************************
   *   REMOVE DC OFFSET
   ******************************/
  int32_t avg = 0;
  int16_t *ptr = inputData;
  for(int i=0; i<DATA_SIZE; i++) avg += *ptr++;
  avg = avg/DATA_SIZE;

  ptr = inputData;
  for(int i=0; i<DATA_SIZE; i++){
    *ptr -= avg;
    *ptr++ = *ptr*SCALE_FACTOR;
  }
//    for(int i=0; i<DATA_SIZE; i++){
//      Serial.print(inputData[i]);
//      Serial.print("\n");
//  }
   
   
  //run the FFT
  
/**************************************************************************/
/*!
    @brief  run an FFT on an int16_t array. Note that this is run in place.
    @param source the data to FFT
    @param length the length of the data. This must be a power of 2 and less than or equal to ZERO_FFT_MAX [#define ZERO_FFT_MAX 4096]
    @return 0 on success, -1 on failure
    @note The FFT is run in place on the data. A hanning window is applied to the input data. The complex portion is discarded, and the real values are returned.
*/
/**************************************************************************/
  ZeroFFT(inputData, DATA_SIZE);
//  Serial.print("[");
  for(int i=3; i<31; i++){
    Serial.write(inputData[i]);
    Serial.write(' ');
  }

    Serial.write('\n');



}
