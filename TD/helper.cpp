#include <iostream>
#include <fstream>
#include <wchar.h>
#include <cstring>
#include <ctime>
using namespace std;



void GetMapFunc() {
    ifstream ifs;
    ofstream ofs;
    time_t seconds = time(NULL);
    tm* timeinfo = localtime(&seconds);
    char sLine[2048];
    srand(time(NULL));
    int map = rand() % (3-0);
    
    ofs.open("map.txt");
    ifs.open("maps/" + std::to_string(map) + ".txt", std::ios::app);
    while(!ifs.eof())
    {
    	ifs.getline(sLine,2048);
        ofs<<sLine<<endl;
    }
    
    ofs.close();
    ifs.close();
}

void SetLogFunc(wchar_t* str) {
    wfstream file;
    time_t seconds = time(NULL);
    tm* timeinfo = localtime(&seconds);
    file.open("log.txt", std::ios::app);
            
    file << asctime(timeinfo) << endl;
    file << str << endl;
    file.close();
}
void DropLogFunc() {
    wfstream file;
    file.open( "log.txt", std::ios::in);
    file.close();

}

extern "C" {
    void GetMap() { GetMapFunc(); };
    void Log(wchar_t* str) { SetLogFunc(str); };
    void DropLog() { DropLogFunc(); };

    
    
    
}
