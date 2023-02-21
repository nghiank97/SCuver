
#ifndef SCUVER_H
#define SCUVER_H

#ifdef __cplusplus
extern "C"{
#endif

#include <inttypes.h>
#include <stdbool.h>

class S_Cuver{

private:
	float Vm = 0; 
	float Am = 0;
	float Throw = 0;
    int Sgn = 1;
    float Gamma = 0;

    float Yf = 0;
    float Ys = 0;
    float Yaux = 0;
	float Ya = 0;
    float Vw = 0;

    float T0 = 0;
    float Ta = 0;
    float Tk = 0;
    float Ts = 0;
    float Tt = 0;

    float t = 0;
    float tau = 0;
    float Tm = 0;

    float qf = 0;
    float q0 = 0;
    float position = 0;
    float velocity = 0;
    float acceleration = 0;
	float index = 0;

public:
	S_Cuver(float gamma,float t,float _Vm, float _Am);
	void upload(float _qf, float _q0);
    void updata_para(float _sp);

    float position_t_T0(float t);
    float position_T0_Ts(float t);
    float position_Ts(float t);
    
    float velocity_t_T0(float t);
    float velocity_T0_Ts(float t);
    float velocity_Ts(float t);

    float acceleration_t_T0(float t);
    float acceleration_T0_Ts(float t);
    float acceleration_Ts(float t);

    float get_position(void);
	float get_velocity(void);
	float get_acceleration(void);

    float get_data(float t);
    bool finish = false;
};

#ifdef __cplusplus
}
#endif
#endif