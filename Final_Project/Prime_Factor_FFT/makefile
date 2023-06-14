CC = g++
CFLAGS = -g -Wall
SRC_DIRS := src/lib
BIN = 10_40875041H
OUT = *.o

SRCS := $(wildcard $(SRC_DIRS:=/*.cpp))
OBJS := $(SRCS:.cpp=.o)

all: $(BIN)

%.o: %.cpp %.h
	$(CC) $(CFLAGS) -c $< -o $@

$(BIN): src/$(BIN).cpp $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

do:
	./$(BIN) ./input/input1.in
	./$(BIN) ./input/input2.in
	./$(BIN) ./input/input3.in
	./$(BIN) ./input/input4.in
	./$(BIN) ./input/input5.in

clean:
	rm -rf src/lib/*.o $(BIN)