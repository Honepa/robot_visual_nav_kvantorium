#define FRW_LFT_IK 9
#define FRW_RGT_IK 8
#define BKW_LFT_IK 7
#define LFT_FRW_IK 6
#define LFT_BKW_IK 5
#define BKW_RGT_IK 4
#define RGT_BKW_IK 3
#define RGT_FRW_IK 2

const int trig_pins[6] = {3, 4, 7, 8, 11, 12};
const int echo_pins[6] = {2, 5, 6, 9, 10, 13};
int mm[6] = {0, 0, 0, 0, 0, 0};

String get_output()
{
  String output;
  output = String(mm[0]) + '\n' + String(mm[1]) + '\n' + String(mm[2]) + '\n' + String(mm[3]) + '\n' + String(mm[4]) 
                 + '\n' + String(mm[5]) + '\n' 
                 + String(analogRead(A1)) + '\n' 
                 + String(analogRead(A3)) + '\n' 
                 + String(analogRead(A5)) + '\n' 
                 + String(analogRead(A7)) + '\n' 
                 + String(digitalRead(FRW_LFT_IK)) + '\n' 
                 + String(digitalRead(FRW_RGT_IK)) + '\n' 
                 + String(digitalRead(BKW_LFT_IK)) + '\n' 
                 + String(digitalRead(LFT_FRW_IK)) + '\n' 
                 + String(digitalRead(LFT_BKW_IK)) + '\n' 
                 + String(digitalRead(BKW_RGT_IK)) + '\n' 
                 + String(digitalRead(RGT_BKW_IK)) + '\n' 
                 + String(digitalRead(RGT_FRW_IK)) + '\n'
                 + "<";
  return output;
}

int get_mm(int trigPin, int echoPin)
{
  int mm;
  unsigned long sen_dur = 0;
  sen_dur = 0;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);

  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  sen_dur = pulseIn(echoPin, HIGH, 9000);
  //sen_dur = pulseIn(echoPin, HIGH);
  mm = sen_dur / 5.8;

  return mm;
}

void setup()
{
  for (int i = 0; i < 6; i++)
  {
    pinMode(trig_pins[i], OUTPUT);
  }
  for (int i = 0; i < 6; i++)
  {
    pinMode(echo_pins[i], INPUT);
  }
  pinMode(FRW_LFT_IK, INPUT_PULLUP);
  pinMode(FRW_RGT_IK, INPUT_PULLUP);
  pinMode(BKW_LFT_IK, INPUT_PULLUP);
  pinMode(LFT_FRW_IK, INPUT_PULLUP);
  pinMode(LFT_BKW_IK, INPUT_PULLUP);
  pinMode(BKW_RGT_IK, INPUT_PULLUP);
  pinMode(RGT_BKW_IK, INPUT_PULLUP);
  pinMode(RGT_FRW_IK, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop()
{
  /*
  for (int i = 0; i < 6; i++)
  {
    mm[i] = get_mm(trig_pins[i], echo_pins[i]);
    //delay(100);
  }
  for (int i = 0; i < 6; i++)
  {
    Serial.println(mm[i]);
  }
  */
  Serial.println(get_output());

}
