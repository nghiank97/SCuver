
#include <iostream>
#include <fstream>
#include "QuinticPolynomial.h"

using namespace std;
f32 p,v,a;
int main(void){
    Quintic scuver(120, 0.01);
    ofstream myfile;
    myfile.open ("data.txt");
    while(1){
        scuver(260,0);
		if(scuver.is_finished() == true){
            break;
		}
        p = scuver.get_position();
        v = scuver.get_velocity();
        a = scuver.get_acceleration();
        myfile <<p<<"\t"<<v<<"\t"<<a<<"\n";
    }
    myfile.close();

    return 1;
}