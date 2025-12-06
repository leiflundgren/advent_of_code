#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <list>
#include <print>
#include <ranges>
#include <set>
#include <thread>
#include <vector>
#include <filesystem>

struct Block
{
    size_t id = 0;
    size_t size = 0;
    bool free = false;
};


size_t calc_checksum(const std::vector<size_t>& disk)
{
    size_t checksum = 0;
    for (auto [i, id] : std::views::zip(std::views::iota(0), disk))
    {
        if (id == -1)
            continue;

        checksum += i * id;
    }
    return checksum;
}


size_t calc_checksum(const std::list<Block>& block_disk)
{
    size_t checksum = 0;
    size_t index = 0;
    for (auto [id, size, free] : block_disk)
    {
        if (free)
        {
            index += static_cast<int>(size);
            continue;
        }

        for (size_t s = 0; s < size; s++)
            checksum += index++ * id;
    }
    return checksum;
}


int main()
{
    namespace ch = std::chrono;

    auto input_start = ch::high_resolution_clock::now();
    std::vector<size_t> disk;
    std::list<Block> block_disk;

    std::list<std::list<Block>::iterator> free_blocks, file_blocks;
    std::array<std::list<std::list<Block>::iterator>::iterator, 9> helper{};
    helper.fill(free_blocks.end());

    std::wcout << L"Running from " << std::filesystem::current_path() << std::endl;

    std::stringstream input_test("2333133121414131402");
    std::ifstream input_file{ "C:\\repos\\advent_of_code\\2024\\9 Disk Fragmenter\\input.txt" };

    std::istream* inputs[] = { 
    //    &static_cast<std::istream&>(input_test), 
        &static_cast<std::istream&>(input_file),
    };

    for (std::istream* input_ptr : inputs)
    {
        {
            std::istream& input(*input_ptr);

            bool free = false;
            size_t id = 0;

            char c;
            while (input.get(c))
            {
                auto size = static_cast<size_t>(c - '0');


                auto it = block_disk.insert(block_disk.end(), { id, size, free });

                if (free)
                {
                    for (auto _ = 0; _ < size; ++_)
                        disk.emplace_back(-1);
                    
                    auto fr = free_blocks.insert(free_blocks.end(), it);

                    for (int i = static_cast<int>(size) - 1; i >= 0; --i)
                    {
                        if (auto h = helper[i]; h == free_blocks.end() && (*fr)->size - 1 >= i)
                            helper[i] = fr;
                    }
                }
                else
                {
                    for (auto _ = 0; _ < size; ++_)
                        disk.emplace_back(id);
                    file_blocks.push_back(it);
                
                    id++;
                }

                free = !free;
            }

            std::ranges::reverse(file_blocks);
        }

        std::println("time taken to parse input: {}",
            ch::duration_cast<ch::microseconds>(ch::high_resolution_clock::now() - input_start));
        std::println("");

        std::cout << "Disk parsed \r\n";
        for (auto i = 0; i < disk.size() && i < 100; ++i)
        {
            auto c = disk[i];
            if (c != 0)
                std::cout << ".";
            else
                std::cout << '(' << c << ')';
        }
        std::cout << std::endl;


        auto start = ch::high_resolution_clock::now();

        {
            auto block_it = disk.rbegin();
            auto free_it = std::ranges::find_if(disk, [](auto& id) { return id == -1; });

            while (free_it < block_it.base())
            {
                std::swap(*block_it, *free_it);

                block_it = std::ranges::find_if(++block_it, disk.rend(), [](auto& id) { return id != -1; });
                free_it = std::ranges::find_if(++free_it, disk.end(), [](auto& id) { return id == -1; });
            }
        }

        size_t checksum = calc_checksum(disk);

        auto first_end = ch::high_resolution_clock::now();
        std::println("checksum: {}", checksum);
        std::println("time taken: {}", ch::duration_cast<ch::microseconds>(first_end - start));
        std::println("");
        std::cout << "Disk compact \r\n";
        for (auto i = 0; i < disk.size() && i < 100; ++i)
        {
            auto c = disk[i];
            if (c != 0)
                std::cout << ".";
            else
                std::cout << '(' << c << ')';
        }
        std::cout << std::endl;
        for (auto& file_it : file_blocks)
        {
            auto file = *file_it;

            if (file.size == 0)
            {
                block_disk.erase(file_it);
                continue;
            }

            for (auto h_it : helper | std::views::drop(file.size - 1))
            {
                if (h_it == free_blocks.end())
                {
                    continue;
                }

                if (auto free_it = *h_it; free_it->size == file.size)
                {
                    std::swap(*free_it, *file_it);
                }
                else
                {
                    block_disk.insert(free_it, file);
                    free_it->size -= file.size;
                    file_it->free = true;
                }

                break;
            }

            for (int i = 0; i < 9; ++i)
            {
                auto fl = Block{ file.id, static_cast<size_t>(i + 1), false };
                helper[i] = std::ranges::find_if(helper[i], free_blocks.end(), [&fl](const auto& block_it) {
                    auto& [id, size, free] = *block_it;
                    return id < fl.id && free && fl.size <= size;
                    });
            }
        }

        checksum = calc_checksum(block_disk);

        auto end = ch::high_resolution_clock::now();
        std::println("checksum (by block): {}", checksum);
        std::println("time taken: {}", ch::duration_cast<ch::microseconds>(end - first_end));
    }

    return 0;
}