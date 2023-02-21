all:
	g++ -Wall -g -c ./QuinticPolynomial.cpp -o ./QuinticPolynomial.o -I./QuinticPolynomial.h
	g++ -Wall -g -c ./main.cpp -o ./main.o -I./main.h
	g++ main.o QuinticPolynomial.o -lm -o main
	./main.exe