//Se comunica con python por el puerto serie
//python ordena girar x grados
//arduino gira y le avisa cuando acaba

String sp_read()
{
  String serialLine = "";
  while (Serial.available() >0)  
  {
    serialLine = serialLine + char(Serial.read());
  }
  return serialLine;

}

void setup()
{
  pinMode (13, OUTPUT);
  Serial.begin(9600);
  delay(2000);
}

void loop()
{
  String lectura_serie = sp_read();
//  Serial.println("echo: " +lectura_serie);
  //Si python dice que hay que rotar se rota
  //if(lectura_serie == "rotate_on")
  //indexOf returns -1 if not found
  if(lectura_serie.indexOf("rotate_on") >= 0)
  {
    lectura_serie = lectura_serie.substring(9);
    int pasos = lectura_serie.toInt();
    //Hacer la rotacion de la plataforma
    for(int x = 0; x < pasos; x++)
    {
      digitalWrite(13,HIGH);
      delay(50);
      digitalWrite(13,LOW);
      delay(50);
    }

    //Avisar a python que ha acabado de rotar
    Serial.println("rotate_off");
  }
  //Es necesario para que lea bien el puerto
  delay(100);
}

