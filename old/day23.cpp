#include <iostream>
#include <list>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <array>
#include <vector>


std::list<int> createList(std::string input)
{
    std::list<int> result;
    for(auto c : input)
        result.push_back(c - '0');

    int listSize;
    listSize = 1000000;
//    listSize = result.size();

    for (int i = result.size(); i < listSize; ++i)
        result.push_back(i + 1);

    return result;
}

int main()
{
    std::string input;

//    input = "389125467";
    input = "398254716";

    int nIterations = 10000000;

    auto allCups = createList(input);
    int listSize = allCups.size();

    std::cout << "List size: " << allCups.size() << ", last element: " << allCups.back() << std::endl;
    auto current = allCups.begin();

    std::vector<std::list<int>::iterator> iterators;
    iterators.resize(allCups.size());
    for(auto it = allCups.begin(); it != allCups.end(); it++)
        iterators[*it - 1] = it;

    for (int iteration = 0; iteration < nIterations; ++iteration)
    {
        int currentNumber = *current;
        std::array<int,3> pickup;
        auto pickupIt = current;
        pickupIt++;
        for (int i = 0; i < 3; i++)
        {
            if(pickupIt == allCups.end())
                pickupIt = allCups.begin();
            pickup[i] = (*pickupIt);
            pickupIt = allCups.erase(pickupIt);
        }
//        int count = 0;
//        std::cout<< " (current number: "<< currentNumber;
//        for (auto& elt : pickup)
//            std::cout << ", pickup[" << count++ << "]: " << elt;
//        std::cout<<")" << std::endl;

        int insertTo = (currentNumber - 2 + listSize) % listSize + 1;
        while (std::find(pickup.begin(), pickup.end(), insertTo) != pickup.end())
        {
            insertTo = (insertTo - 2 + listSize) % listSize + 1;;
        }
        auto insertToIt = iterators[insertTo - 1];  // std::find(allCups.begin(), allCups.end(), insertTo);
        if(insertToIt == allCups.end())
        {
            std::cout<< "something is WRONG! Couldn't find " << insertTo << " in whole list (current number: "<< currentNumber;
            int count = 0;
            for (auto& elt : pickup)
                std::cout << ", pickup[" << count++ << "]: " << elt;
            std::cout<<")" << std::endl;
            throw 1;
        }
        else
        {
            ++insertToIt;
//            if(insertToIt == allCups.end())
//                insertToIt = allCups.begin();
            for(auto elt : pickup)
            {
                insertToIt = allCups.insert(insertToIt, elt);
                iterators[elt - 1] = insertToIt++;
            }

        }
        current++;
        if (current == allCups.end())
            current = allCups.begin();
//        std::cout << "List" << iteration << ": ";
//        for (auto elt : allCups)
//            std::cout<< elt << ", ";
//        std::cout << std::endl;

    }

//    std::cout << "List: ";
//    for (auto elt : allCups)
//        std::cout<< elt << ", ";
//    std::cout << std::endl;
    auto oneIt = std::find(allCups.begin(), allCups.end(), 1);

    std::list<int> oneNumbers;
    for (int i = 0; i < 9; i++)
    {
        oneNumbers.push_back(*oneIt);
        std::cout<< i << ": " << *oneIt++ <<", ";
        if(oneIt == allCups.end())
            oneIt = allCups.begin();
    }

//    int count = 0;
//    for (auto it : iterators)
//    {
//        std::cout << count++ << ": " << *it << ".\n";
//    }

    auto it = oneNumbers.begin();
    ++it;
    int a = *it;
    ++it;
    int b = *it;
    std::cout<< "Multiply " << a<< " * " << b << " = " << static_cast<size_t>(a) * b;
    std::cout << std::endl;



    return 0;
}