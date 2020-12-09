#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

int main(int argc, char** argv)
{
    std::string fname;
    std::vector<std::string> vec;
    if (argc > 1)
        fname = argv[1];
    int numPws1=0;
    int numPws2=0;
    
    if (!fname.empty())
    {
        std::cout<< "Reading from " << fname << std::endl;
        std::fstream files(fname);
        std::string input;
        while (std::getline(files, input))
        {
            vec.push_back(input);
        }
        std::cout << "Input has length " << vec.size() << std::endl;
        
        for(auto& line : vec)
        {
            int minus = line.find('-');
            int space = line.find(' ');
            int colon = line.find(':');
            int minV = std::stoi(line.substr(0,minus));
            int maxV = std::stoi(line.substr(minus + 1,space));
            char which = line[colon -1];
            
            int count = 0;
            
            for(int i = colon + 1; i < line.size(); i++)
            {
                count += line[i] == which;
            }
            bool iscorrect1 = minV <= count && count <= maxV;
            numPws1 += iscorrect1;
            bool iscorrect2 = !(line[minV + colon + 1] == which) != !(line[maxV + colon + 1] == which);
            numPws2 += iscorrect2;
        }            
    }
    std::cout << "Got " << numPws1 << " and " << numPws2 << " passwords" << std::endl;
    
    return 0;
}

