#define SPEED 32000 // Delay between steps in us
#define MICROSTEPS 1 // Microsteps in each step

int pin_dir    = 5;
int pin_step   = 4;
int pin_enable = 3;

String sp_read()
{
  String line = "";
  while (Serial.available() > 0)
  {
    line = line + char(Serial.read());
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

  if(msg.indexOf("enable") >= 0)
  {
    digitalWrite(pin_enable, HIGH);
    delay(50);
    Serial.println("enabled");
    alarm = 1;
  }

  if(msg.indexOf("step") >= 0)
  {
    msg = msg.substring(5);
    int steps = msg.toInt() * MICROSTEPS;
    for(int i = 0 ; i < steps ; i++)
    {
      delayMicroseconds(10);
      digitalWrite(pin_step, HIGH);
      delayMicroseconds(10);
      digitalWrite(pin_step, LOW);
      delayMicroseconds(SPEED);
    }
    Serial.println("stop");
  }

  if(msg.indexOf("disable") >= 0 || alarm > 6000) // 10 min
  {
    digitalWrite(pin_enable, LOW);
    Serial.println("disabled");
    delay(50);
    alarm = 0;
  }

  delay(100);
  if( alarm > 0 )
  {
    alarm++;
  }
}
