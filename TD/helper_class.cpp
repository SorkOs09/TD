#include <iostream>
#include <fstream>
#include <wchar.h>
#include <cstring>

using namespace std;


class Logger{
    public:
        void SetScoreTable(wchar_t* str) {
            wfstream file;
            file.open("ScoreTable.txt", std::ios::app);
            file << str <<endl;
            file.close();
};

};
extern "C" {
    void SetScore(wchar_t* str) { Logger logger; logger.SetScoreTable(str); };
}
