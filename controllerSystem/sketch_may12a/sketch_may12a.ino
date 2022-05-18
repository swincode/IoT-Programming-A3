
#include <stdbool.h>

#define BAUD_RATE 9600

#define X_AXIS A0
#define Y_AXIS A1
#define JOYSTICK_BUTTON 2
#define LED_PIN 1
#define DEBOUNCE_DELAY 1000

bool activation_state = false;
int last_debounce_time;

int x_err, y_err, x_val, y_val, prev_x_val = 0, prev_y_val = 0;

void setup() {
  
  // Initialise serial connection
  Serial.begin(BAUD_RATE);

  // Initialise joystick button ISR and pin
  pinMode(JOYSTICK_BUTTON, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(JOYSTICK_BUTTON), activation_ISR, RISING);

  // Initialise joystick error to remove joystick drift effects
  x_err = map_axis(analogRead(X_AXIS));
  y_err = map_axis(analogRead(Y_AXIS));

  // Initisalise LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

}

void loop() {
  
  // Read values from joystick
  x_val = map_axis(analogRead(X_AXIS));
  y_val = map_axis(analogRead(Y_AXIS));

  Serial.print(x_val);
  Serial.print(',');
  Serial.println(y_val);

  // Assign current values to previous
  prev_x_val = x_val;
  prev_y_val = y_val;
  delay(1000);
  
}

bool outside_range(int prev_val, int val, int err) {
  return (val < (prev_val - err) & val > (prev_val + err));
}

int map_axis(int axis) {
  return map(axis, 0, 1023, 0, 180);
}

void activation_ISR() {
  if ((millis() - last_debounce_time) > DEBOUNCE_DELAY) {
    activation_state = !activation_state;
    last_debounce_time = millis();
    digitalWrite(LED_PIN, activation_state);
  }
}
