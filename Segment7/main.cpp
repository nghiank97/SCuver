
#include <iostream>
#include <fstream>
#include "Segment7.h"

using namespace std;

int16_t list[2] = {50,-50};
uint16_t i = 0;
uint16_t j = 0;
int main(void){
    Segment7 segment7(10, 10, 20, 0.02);
    ofstream myfile;
    myfile.open ("data.txt");
    while(1){
        segment7(list[0]);
		if(segment7.is_finished() == true){
            break;
		}
        myfile <<segment7.get_position()<<"\n";
    }
    myfile.close();

    return 1;
}