#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

int main(int argc, char** argv)
{
    std::string fname;
    std::vector<int> vec;
    if (argc > 1)
        fname = argv[1];
    
    if (!fname.empty())
    {
        std::cout<< "Reading from " << fname << std::endl;
        std::fstream files(fname);
        int input;
        while (files >> input)
        {
            vec.push_back(input);
        }
        std::cout << "Input has length " << vec.size() << std::endl;
            
        std::sort(vec.begin(), vec.end());
        
        int i = 0;


        for(int i = 0; i< vec.size(); ++i)
        for(int j = i+1; j < vec.size()-1; ++j)
        {
            int k = vec.size() -1;
            int sum1 = vec[i] + vec[j];
            while(sum1 + vec[k] > 2020 && j < k)
                k--;
            if(sum1 + vec[k] == 2020)
               std::cout << "Woohoo! found " << vec[i] << " and " << vec[j] <<  " and " << vec[k] << " summing to 2020. Thier product is " << vec[i] * vec[j] * vec[k] << std::endl;
            else continue;
        }
            
       /* while(i < k)
        {
            while (vec[i]*2 + vec[k] > 2020)
            {
                k--;
                std::cout<<vec[i] << " :i | k: " << vec[k] << std::endl;
            }
            int j = i + 1;
            while (j < k)
            {
                int sum = vec[i] + vec[j] + vec[k];
                std::cout<<sum << std::endl;
                if (sum >= 2020)
                {
                    if (sum == 2020)
                    {
                       std::cout << "Woohoo! found " << vec[i] << " and " << vec[j] <<  " and " << vec[k] << " summing to 2020. Thier product is " << vec[i] * vec[j] * vec[k] << std::endl;
                       return 0;
                    }
                    else
                        break;
                }
                j++;
            }
            k--; 
        }*/
        std::cout << "found nothing :(";
    }
    
    bool isFinished = false;
    while (!isFinished)
    {   
        int input;
        std::cin >> input;
        vec.emplace_back(input);
        for(int i = 0; i < vec.size(); ++i)
            for(int j = i + 1; j < vec.size(); ++j)
                if (vec[i] + vec[j] < 2020)
                for(int k = j + 1; j < vec.size(); ++j)
                    if (vec[i] + vec[j] + vec[k] == 2020)
                    {
                        std::cout << "Woohoo! found " << vec[i] << " and " << vec[j] <<  " and " << vec[k] << " summing to 2020. Thier product is " << vec[i] * vec[j] * vec[k] << std::endl;
                        return 0;
                    }
    }   
    return -1;
}

