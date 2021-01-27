all: librreader.so

reader.o: reader.c
	gcc  -fPIC -Wall -g -c reader.c

librreader.so: reader.o
	gcc -shared -fPIC -o librreader.so reader.o

clean:
	rm -f *.o *.so

