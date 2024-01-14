# build the test code
# remember -g
ARTIFACTS := test1 test2

all: $(ARTIFACTS)

% : %.cpp
	g++ $< -g -o $@

clean:
	rm -fr $(ARTIFACTS)


