#include "QuinticPolynomial.h"
#include <math.h>
#include <stdio.h>

void toIdentity(f32 m2[6][6]){
    for(int i =0; i < 6; i++){
        m2[i][i] = 1;
    }
}

void divideRowByNumber(f32 number, f32 m1[6][6], int row, f32 m2[6][6]){
    for(int i =0; i < 6; i++){
        m1[row][i] /= number;
        m2[row][i] /= number;
    }
}

void doOperation(f32 number, f32 m1[6][6], int col, int row, f32 m2[6][6]){
    for(int k=0; k < 6; k++){
        m1[row][k] -= number * m1[col][k];
        m2[row][k] -= number * m2[col][k];
    }
}

void invert_matrix_6x6(f32 m1[6][6], f32 m2[6][6]){
    f32 selector;
    toIdentity(m2);
    for(int i =0; i < 6; i++){
        selector = m1[i][i];
        divideRowByNumber(selector, m1, i, m2);
        for(int j = 0; j < 6; j++){
            if (j == i)
               continue;

            if(m1[j][i] != 0){
                doOperation(m1[j][i], m1, i, j, m2);
            }
        }
    }
}

Quintic::Quintic(f32 _Vm,f32 _t){
	t0 = 0;
	tf = 0;

	q0 = 0;
	qf = 0;

    v0 = 0;
	vf = 0;

    Vm = _Vm;
    position = 0;
    velocity = 0;
    acceleration = 0;

	index= _t;
	finished = false;
	t = 0;
}

void Quintic::get_data(f32 _t){
    if (_t< tf){
        position = x[0] + x[1]*_t + x[2]*pow(_t, 2) + x[3]*pow(_t, 3) + x[4]*pow(_t, 4) + x[5]*pow(_t, 5);
        velocity =  x[1] + 2*x[2]*_t + 3*x[3]*pow(_t, 2) + 4*x[4]*pow(_t, 3) + 5*x[5]*pow(_t, 4);
        acceleration = 2*x[2] + 6*x[3]*_t + 12*x[4]*pow(_t, 2) + 20*x[5]*pow(_t, 3);
    }
    else{
        position = position;
        velocity = 0;
        acceleration = 0;
    }
}

f32 Quintic::get_position(void){
    return position;
}

f32 Quintic::get_velocity(void){
    return velocity;
}

f32 Quintic::get_acceleration(void){
    return acceleration;
}

void Quintic::operator() (f32 _qf, f32 _q0){
	f32 delta = _qf-qf;
	if ((delta != 0) && ((t > tf) || (t == 0))){
		q0 = _q0;
		qf = _qf;

        if ((qf - q0) >= 0)
            tf = (qf - q0)/Vm;
        else
            tf = (qf - q0)/-Vm;

        printf("tf %f \r\n",tf);

        mA[0][0]= 1; mA[0][1]= t0; mA[0][2]= pow(t0, 2); mA[0][3]= pow(t0, 3); mA[0][4]= pow(t0, 4); mA[0][5]= pow(t0, 5);

        mA[1][0]= 0; mA[1][1]= 1; mA[1][2]= 2*t0; mA[1][3]= 3*pow(t0, 2); mA[1][4]= 4*pow(t0, 3); mA[1][5]= 5*pow(t0, 4);

        mA[2][0]= 0; mA[2][1]= 0; mA[2][2]= 2; mA[2][3]= 6*t0; mA[2][4]= 12*pow(t0, 2); mA[2][5]= 20*pow(t0, 3);

        mA[3][0]= 1; mA[3][1]= tf; mA[3][2]= pow(tf, 2); mA[3][3]= pow(tf, 3); mA[3][4]= pow(tf, 4); mA[3][5]= pow(tf, 5);

        mA[4][0]= 0; mA[4][1]= 1; mA[4][2]= 2*tf; mA[4][3]= 3*pow(tf, 2); mA[4][4]= 4*pow(tf, 3); mA[4][5]= 5*pow(tf, 4);

        mA[5][0]= 0; mA[5][1]= 0; mA[5][2]= 2; mA[5][3]= 6*tf; mA[5][4]= 12*pow(tf, 2); mA[5][5]= 20*pow(tf, 3);

        invert_matrix_6x6(mA, inv_mA);
        
		for(int i=0;i<6;i++){
			x[i] = inv_mA[i][0]*q0 + inv_mA[i][3]*qf;
        }
        t = 0;
        finished = false;
	}
    if (t <= tf){
    	t += index;
    	get_data(t);
    }
    else{
    	finished = true;
    	get_data(tf);
    }
}


bool Quintic::is_finished(void){
    return finished;
}