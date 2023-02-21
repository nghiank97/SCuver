
#include "Scuver.h"
#include <math.h>
#include <stdio.h>
#include <float.h>
#include <iostream>
using namespace std;

#define _sign(a) ( ( (a) < 0 )  ?  -1   : ( (a) > 0 ) )

S_Cuver::S_Cuver(float gamma,float t, float _Vm, float _Am){
    Vm = _Vm;
    Am = _Am;
    Gamma = gamma;

    qf = 0;
    q0 = 0;
    index = t;
}

float S_Cuver::position_t_T0(float t){
	if (t< 0){
		return 0;
	}
	else if (t<= tau){
        return (0.5*Vw/T0)*(t*t*t/(3*tau));
    }
    else if ((tau < t) &&(t <= T0)){
        return (0.5*Vw/T0)*((t-tau/2)*(t-tau/2) + tau*tau/12);
    }
    return 0;
}

float S_Cuver::position_T0_Ts(float t){
    if (t <= T0){
    	return position_t_T0(t);
    }
    else{
        return (Ys + Vw*(t-Ts) + position_t_T0(Ta-t));
    }
}

float S_Cuver::position_Ts(float t){
    if (t < Ts){
    	return position_T0_Ts(t);
    }
    else{
        return (Yf - position_T0_Ts(Tt-t));
    }
    return 0;
}


float S_Cuver::velocity_t_T0(float t){
	if (t< 0){
		return 0;
	}
	else if (t<= tau){
        return (0.5*Am)*(t*t/tau);
    }
    else if ((tau < t) &&(t <= T0)){
        return (0.5*Am)*(2*t - tau);
    }
    return 0;
}

float S_Cuver::velocity_T0_Ts(float t){
    if (t <= T0){
    	return velocity_t_T0(t);
    }
    else{
        return (Vw - velocity_t_T0(Ta-t));
    }
}

float S_Cuver::velocity_Ts(float t){
    if (t < Ts){
    	return velocity_T0_Ts(t);
    }
    else{
        return velocity_T0_Ts(Tt-t);
    }
    return 0;
}


float S_Cuver::acceleration_t_T0(float t){
	if (t< 0){
		return 0;
	}
	else if (t<= tau){
        return (Am/tau)*t;
    }
    else if ((tau < t) &&(t <= T0)){
        return Am;
    }
    return 0;
}

float S_Cuver::acceleration_T0_Ts(float t){
    if (t <= T0){
    	return acceleration_t_T0(t);
    }
    else{
        return acceleration_t_T0(Ta-t);
    }
}

float S_Cuver::acceleration_Ts(float t){
    if (t < Ts){
    	return acceleration_T0_Ts(t);
    }
    else{
        return -acceleration_T0_Ts(Tt-t);
    }
    return 0;
}


void S_Cuver::upload(float _qf, float _q0){
	float delta = _qf-qf;
	if ((delta != 0) && ((t > Tt) || (t == 0))){
        qf = _qf;
        q0 = _q0;

        Throw = qf-q0;
        Sgn = _sign(Throw);
        Yf = abs(Throw);
        Ys = Yf/2;
        Yaux = 0.5*(1+Gamma)*(Vm*Vm/Am);
        if (Ys <= Yaux) Ya = Ys;
        else Ya = Yaux;
        if (Ys <= Yaux) Vw = sqrt(Ys*Am/(0.5*(1+Gamma)));
        else Vw = Vm;
        T0 = Vw/Am;
        Ta = T0*(1+Gamma);
        tau = Gamma*T0;
        Tm = Ta/2;
        Tk = 2*(Ys-Ya)/Vm;
        Ts = Ta+Tk/2;
        Tt = 2*Ts;

        t = 0;
        finish = false;
	}
    if (t <= Tt){
    	position = position_Ts(t)*(float)Sgn+q0;
        velocity = velocity_Ts(t)*(float)Sgn;
        acceleration = acceleration_Ts(t)*(float)Sgn;
        t += index;
    }
    else{
    	position = position_Ts(Tt)*(float)Sgn+q0;
        velocity = velocity_Ts(Tt)*(float)Sgn;
        acceleration = acceleration_Ts(Tt)*(float)Sgn;
    	finish = true;
    }
}

float S_Cuver::get_position(void){
    return position;
}

float S_Cuver::get_velocity(void){
    return velocity;
}

float S_Cuver::get_acceleration(void){
    return acceleration;
}
