#include <windows.h>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <locale>
#include <cwchar>
#include <thread>
#include <chrono>

std::wstring GenerateRandomUnicodeString(int length) {
    static bool isSeeded = false;
    if (!isSeeded) {
        srand(static_cast<unsigned>(time(0)));
        isSeeded = true;
    }
    const struct {
        WCHAR start;
        WCHAR end;
    } ranges[] = {
        {0x0021, 0x007E},
        {0x0400, 0x04FF},
        {0x3040, 0x309F},
        {0x4E00, 0x9FFF}
    };
    std::wstring result_string;
    result_string.reserve(length);
    for (int i = 0; i < length; i++) {
        int rangeIndex = rand() % (sizeof(ranges) / sizeof(ranges[0]));
        WCHAR start = ranges[rangeIndex].start;
        WCHAR end = ranges[rangeIndex].end;
        result_string += (start + (rand() % (end - start + 1)));
    }
    return result_string;
}

int main() {
    const int NUM_STRINGS = 15;
    const int STRING_LENGTH = 50;
    const std::wstring FILENAME = L"names.txt";
    const auto DELAY = std::chrono::seconds(3);

    while (true) {
        std::vector<std::wstring> unicodeStrings;
        for (int i = 0; i < NUM_STRINGS; ++i) {
            unicodeStrings.push_back(GenerateRandomUnicodeString(STRING_LENGTH));
        }

        std::wofstream outfile(FILENAME.c_str(), std::ios::out | std::ios::binary);

        if (!outfile.is_open()) {
            return 1;
        }

        try {
            outfile.imbue(std::locale("en_US.UTF-8"));
        }
        catch (...) {
            outfile.imbue(std::locale(""));
        }

        for (const auto& str : unicodeStrings) {
            outfile << str << L'\n';
        }

        outfile.close();
        std::this_thread::sleep_for(DELAY);
    }
    system("pause");
    return 0;   
}
