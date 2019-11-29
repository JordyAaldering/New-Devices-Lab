int buzz = D4;
unsigned long PAUZING = 500;
unsigned long BUZZING = 50;
unsigned long lastTime = 0;

#define LONG 5
unsigned long suits[4*2] = {1,1, 1,LONG, LONG,1, LONG,LONG};
unsigned long ranks[13*5] = {1,0,0,0,0, 1,1,0,0,0, 1,1,1 ,0,0, 1,1,1,1,0, LONG,0,0,0,0, LONG,1,0,0,0, LONG,1,1,0,0, LONG,1,1,1,0, LONG,1,1,1,1, LONG,LONG,0,0,0, LONG,LONG,1,0,0, LONG,LONG,1,1,0, LONG,LONG,1,1,1};
int decode[52*2];

int noCards = 52;

int getSuit(int input) {
    //returns the suit of a card
    int suit = input / 13;
    return suit;
}

int getRank(int input) {
    //returns the rank of a card
    int rank = (input % 13);
    return rank;
}

void decodeInput(int input[52]) {
    //decodes the input obtained from the pi and stores it inside a list
    int x = 0;
    for (int i = 0; i < noCards*2; i+=2) {
        int in = input[x];
        decode[i] = getSuit(in);
        decode[i+1] = getRank(in);
        x++;
    }
}

void buzzCard(int suit, int rank) {
    //lets the buzzer buzz according to the suit and rank from the input
    //suit
    for (int s = 0; s < 2; s++) {
		lastTime = millis();
		while (millis() - (BUZZING * suits[suit * 2 + s]) < lastTime){
		    digitalWrite(buzz, HIGH);
		}
		lastTime = millis();
		while (millis() - PAUZING < lastTime) {
			digitalWrite(buzz, LOW);
		}
	}
	//pauze
    while (millis() - PAUZING*3 < lastTime) {
        digitalWrite(buzz, LOW);
    }
    //rank
    lastTime = millis();
    for(int r = 0; r < 5; r++) {
        if (ranks[rank*5+r] > 0) {
            while (millis() - (BUZZING * ranks[rank*5+r]) < lastTime) {
                digitalWrite(buzz, HIGH);
            }
            lastTime = millis();
            while (millis() - PAUZING < lastTime) {
                digitalWrite(buzz, LOW);
            }
            lastTime = millis();
        } else {
            break;
        }
    }
}

void stringToList(int array[52], String input){
    //converts the string-input from the pi to a list
    for(int i=0;i<52;i++){
        array[i] = ((input[i*2]-'0')*10) + (input[i*2+1]-'0');
    }
}

int buzzFeedback(String input){
    //all converting and decoding combined
    int stringInput[52];
    stringToList(stringInput, input);
    decodeInput(stringInput);
    for (int i = 0; i < 52*2; i += 2) {
        buzzCard(decode[i], decode[i+1]);
        digitalWrite(buzz,LOW);
        delay(PAUZING);
    }
    return 0;
}


void setup() {
    pinMode(buzz, OUTPUT);
    Particle.function("feedback", buzzFeedback);
}

void loop() {
}
