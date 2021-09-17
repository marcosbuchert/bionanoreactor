int pin1,pin2,pin3,pin4;
char ByteReceived;
int temperatura;
int rpm;
int ph;
int od;
int caudal;
int presion;
int sp_temperatura=0;
int sp_rpm=0;
int sp_ph=0;
int sp_od=0;
int sp_caudal=0;
int sp_presion=0;

char AXC[16];
char AYC[16];
char XC[16];
char YC[16];

void setup()   /****** SETUP: RUNS ONCE ******/
{
  Serial.begin(9600);
  pinMode(13,OUTPUT);    
}
void loop()   
{
  /*temperatura= analogRead(A0);*/
  /*rpm= analogRead(A1);*/
  ph= analogRead(A2);
  od= analogRead(A3);
  caudal= analogRead(A4);
  presion= analogRead(A5);
   temperatura=37;
   ph=7 ;
   od =80;
   rpm=1350;
  analogWrite(13,sp_rpm);  

  
          if (Serial.available() > 0)
              {
                ByteReceived = Serial.read();
                 if(ByteReceived == 'R') 
                 {
       
                  Serial.print("La temperatura es: ");
                  Serial.println(temperatura);
                  delay(50);
                  Serial.print("las rpm son: ");
                  Serial.println(rpm);
                  Serial.print("el ph es: ");
                  Serial.println(ph);
                  Serial.print("el od es: ");
                  Serial.println(od);
                  delay(50);
                  
                   }

    
                 if(ByteReceived == 'W')
    
                  {
                   String str = Serial.readStringUntil('\n');
                   int data = str.toInt();
                   //Serial.print("EL setpoint de temperatura es: ");
                   Serial.println(data);
                   ByteReceived=0;
     
                    }
                  if(ByteReceived == 'G')
                    {
                   String str = Serial.readStringUntil('\n');
                   int data = str.toInt();
                   //Serial.print("EL setpoint de rpm es: ");
                   Serial.println(data); 
                   sp_rpm=data;
                   ByteReceived=0;
     
                    }
                  if(ByteReceived == 'H')
                    {
                    String str = Serial.readStringUntil('\n');
                    int data = str.toInt();
                    Serial.print("EL setpoint de ph es: ");
                    Serial.println(data);
                    ByteReceived=0;
                    }
                    if(ByteReceived == 'J')
                    {
                    String str = Serial.readStringUntil('\n');
                    int data = str.toInt();
                    Serial.print("EL setpoint de od es: ");
                    Serial.println(data);
                    ByteReceived=0;
                    }
                  if(ByteReceived == 'A')
                    {
                    Serial.println("bomba B1 activada: ");
                    digitalWrite(pin1, true);
                    ByteReceived=0;
                    }
                      
                    if(ByteReceived == 'B')
                    { Serial.println("bomba B2 activada ");
                     digitalWrite(pin2, true);;
                    ByteReceived=0;
                    } 
                     if(ByteReceived == 'C')
                    {
                     Serial.println("Bomba 3 activada: ");
                     digitalWrite(pin3, true);
                    ByteReceived=0;
                    }
                     if(ByteReceived == 'D')
                    {
                    Serial.println("Bomba B4 activada ");
                    digitalWrite(pin4, true);
                    ByteReceived=0;
                    }
                    
                    if(ByteReceived == 'E')
                    {
                     
                     Serial.println("Bombas detenidas ");
                     digitalWrite(pin1,false );
                      digitalWrite(pin2, false);
                      digitalWrite(pin3, false);
                      digitalWrite(pin4, false);
                      ByteReceived=0;
                    }
    }
}   
   

    
  
