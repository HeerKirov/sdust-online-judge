all: judge_client.cc
	g++ -Wall -c -I./include -I./lib_json lib_json/json_value.cpp lib_json/json_writer.cpp lib_json/json_reader.cpp
	g++ -Wall -c json_reader.o json_value.o json_writer.o judge_client.cc -I/usr/local/mysql/include/mysql -I/usr/include/mysql -I./include -I./lib_json 
	g++ -Wall -o judge_client judge_client.o json_reader.o json_value.o json_writer.o -L/usr/local/mysql/lib/mysql -L/usr/lib/mysql  -L/usr/lib64/mysql -lmysqlclient -I./include -I./lib_json 

clean:
	rm -rf json_reader.o json_value.o json_writer.o judge_client.o