
#ifndef Segment7_H
#define Segment7_H

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

class Segment7{

private:
    f32 Jmax;
    f32 Amax;
    f32 Vmax;
	f32 V0;
    f32 qf;
	f32 q0 = 0;
    f32 index;

    f32 T,t1,t3,t2,t4,t5,t6;
	f32 a1,a2,a3,a4,a5,a6,a7;

    f32 b1,b2,b3,b4,b5,b6,b7;
	f32 c1,c2,c3,c4,c5,c6,c7;
	f32 d1,d2,d3,d4,d5,d6,d7;

	f32 position;
	f32 velocity;
	f32 acceleration;
	f32 time;
	bool finished = false;
	int8_t Sign = 1;

public:
	Segment7(f32 _Am, f32 _Vm, f32 _Jm, f32 _t);
	void operator()(f32 sp);
	void get_data(f32 _t);

	f32 get_position(void);
	f32 get_velocity(void);
	f32 get_acceleration(void);

	bool is_finished(void);
};

#ifdef __cplusplus
}
#endif

#endif /* Segment7_H */
