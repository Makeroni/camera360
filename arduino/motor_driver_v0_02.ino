#define SPEED 8 // Delay between steps in ms

int pin_dir    = 5;
int pin_step   = 4;
int pin_enable = 3;

String sp_read()
{
  String line = "";
  while (Serial.available() > 0)
  {
    line = line + char(Serial.read());
    //Add this delay to ensure that all the values are read
    delay(10);
  }
  return line;
}

// Disable if the user forgets
int alarm = 0;

void setup()
{
  pinMode (pin_step,   OUTPUT);
  pinMode (pin_enable, OUTPUT);
  pinMode (pin_dir,    OUTPUT);

  digitalWrite(pin_step,   LOW);
  digitalWrite(pin_enable, LOW);
  digitalWrite(pin_dir,    LOW);

  Serial.begin(9600);
  delay(2000);
}

void loop()
{
  String msg = sp_read();

  if(msg.indexOf("RQen") >= 0)
  {
	Serial.println("RQen_srv");
    digitalWrite(pin_enable, HIGH);
    delay(50);
    Serial.println("GRen");
    alarm = 1;
  }

  if(msg.indexOf("RQstp") >= 0)
  {
	Serial.println("RQstp_srv");
    msg = msg.substring(5);
    int steps = msg.toInt();
    for(int i = 0 ; i < steps ; i++)
    {
//      delayMicroseconds(SPEED*1000/128);
      delayMicroseconds(10);
      digitalWrite(pin_step, HIGH);
//      delayMicroseconds(SPEED*1000/128);
      delayMicroseconds(10);
      digitalWrite(pin_step, LOW);
      delay(SPEED);
    }
    alarm = 1; //Si hay actividad la alarma se resetea
    Serial.println("GRstp");
  }

  if(msg.indexOf("RQdis") >= 0 || alarm > 600) // 1 min
  {
	Serial.println("RQdis_srv");
    digitalWrite(pin_enable, LOW);
    Serial.println("GRdis");
    delay(50);
    alarm = 0;
  }

  delay(100);
  if( alarm > 0 )
  {
    alarm++;
  }
}
