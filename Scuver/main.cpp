#include <iostream>
#include <fstream>
using namespace std;
#include "Scuver.h"

uint16_t dis[2] = {100,500};
uint8_t local = 0;


int main(void){
    S_Cuver scuver(0.5,0.01,150,150);
    ofstream myfile;
    myfile.open ("data.txt");

    while(1){
        scuver.upload(dis[local], scuver.get_position());
        if (scuver.finish == true){
            local++;
            if(local == 2){
                break;
            }
        }
        myfile <<scuver.get_position()<<"\t"<<scuver.get_velocity()<<"\t"<<scuver.get_acceleration()<<"\n";

    }
    myfile.close();

    return 1;
}