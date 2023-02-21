#ifndef QuinticPolynomial_H
#define QuinticPolynomial_H

#ifdef __cplusplus
extern "C"{
#endif

#include <stdbool.h>
#include <inttypes.h>

#define u08 uint8_t
#define u16 uint16_t
#define u32 uint32_t

#define i08 int8_t
#define i16 int16_t
#define i32 int32_t

#define f32 float

class Quintic{
private:
	f32 t0, tf;
	f32 q0, qf;
	f32 v0, vf;
    f32 a0, af;
	f32 Vm;

	f32 mA[6][6] = {0};
	f32 inv_mA[6][6] = {0};
	f32 x[6] = {0};

	f32 t;
	f32 index;
	f32 position;
	f32 velocity;
    f32 acceleration;
	bool finished = false;

public:
	Quintic(f32 _Vm,f32 _t);
	void operator()(f32 _qf, f32 _q0);
	void get_data(f32 _t);
	f32 get_position(void);
	f32 get_velocity(void);
    f32 get_acceleration(void);
	bool is_finished(void);
};

#ifdef __cplusplus
}
#endif
#endif /* QuinticPolynomial_H */
