all: librreader.so

reader.o: reader.c
	gcc -fPIC -Wall -g -c reader.c -o reader.o

librreader.so: reader.o
	gcc -shared -fPIC reader.o -o librreader.so
	cp librreader.so ../recorder_utils/

clean:
	rm -f *.o *.so
