int timer1_counter;
int CLK=30;
int DIR = 31;
int Stepper_Position[4] = {0x01, 0x02, 0x04, 0x08};
int i, x, t;
int Searching = 0;
int Velocitys[2000];
volatile int task1 = 0;
void setup() {
  Serial.begin(9600);
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(CLK, OUTPUT);
  pinMode(DIR, OUTPUT);
  noInterrupts();
  TCCR1A = 0;
  TCCR1B = 0;

  timer1_counter = 63935;   //65535 - 63935 = 1600 --------------> 1600/16000000 = 0.0001
  TCNT1 = timer1_counter;
  TCCR1B = TCCR1B & B11111000 | B00000001;   //prescaler = 65535 - timer1_counter / 16Mhz 
  TIMSK1 |= (1<<TOIE1);
  interrupts();

}

void loop() {
  while(Serial.available() > 1){
    for(x=0; x<2000; x++){
      String TempDataS = Serial.readStringUntil('\n');
      int TempDataI = TempDataS.toInt();
      Serial.print(TempDataI);
      Serial.print("\n");
      Velocitys[x] = TempDataI;
      x++;
    }
  }

}

ISR(TIMER1_OVF_vect){
  TCNT1 = timer1_counter;

  task1++;

  if(task1 >= Velocitys[t]){
    PORTA = Stepper_Position[i];
    i++;
    if(i > 4){
      i = 0;
    }
    t++;
    task1 = 0;
  }
    
}
