#include <signal.h>
#include <stdio.h>
#include <string>
#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>
#include "libpixyusb2.h"

using json = nlohmann::json;

Pixy2 pixy;
static bool run_flag = true;

struct Tile { uint16_t x; uint16_t y; };

void handle_SIGINT(int unused)
{
    run_flag = false;
}

// Helper function: average a small 3x3 region around a tile
void getAverageRGB(Tile tile, uint8_t &avgR, uint8_t &avgG, uint8_t &avgB)
{
    int sumR=0, sumG=0, sumB=0;
    int count=0;
    for(int dx=-1; dx<=1; dx++)
    {
        for(int dy=-1; dy<=1; dy++)
        {
            uint8_t r,g,b;
            pixy.video.getRGB(tile.x+dx, tile.y+dy, &r,&g,&b);
            sumR += r; sumG += g; sumB += b;
            count++;
        }
    }
    avgR = sumR / count;
    avgG = sumG / count;
    avgB = sumB / count;
}

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <angle>\n";
        return 1;
    }
    std::string angle = argv[1];

    int Result;
    uint8_t r,g,b;

    signal(SIGINT, handle_SIGINT);

   // printf("=============================================================\n");
   // printf("= PIXY2 Get RGB values demo (24 tiles, 3 faces, no centers) =\n");
   // printf("=============================================================\n");

   // printf("Connecting to Pixy2...");

    // Initialize Pixy2
    Result = pixy.init();
    if (Result < 0) { printf("Error, pixy.init() returned %d\n", Result); return Result; }
   // printf("Success\n");

    // Get Pixy2 Version info
    Result = pixy.getVersion();
    if (Result < 0) { printf("pixy.getVersion() returned %d\n", Result); return Result; }
   // pixy.version->print();

    // Load coordinates JSON
    std::ifstream coordFile("coords.json");
    if (!coordFile.is_open()) { std::cerr << "Failed to open coords.json\n"; return 1; }
    json tileData;
    coordFile >> tileData;
    coordFile.close();

    if (!tileData.contains(angle)) { std::cerr << "Angle not found: " << angle << "\n"; return 1; }

    json facesJson = tileData[angle];

    Tile face1[8], face2[8], face3[8];

    for (int i=0; i<8; ++i) {
        face1[i].x = facesJson["face1"][i]["x"];
        face1[i].y = facesJson["face1"][i]["y"];
        face2[i].x = facesJson["face2"][i]["x"];
        face2[i].y = facesJson["face2"][i]["y"];
        face3[i].x = facesJson["face3"][i]["x"];
        face3[i].y = facesJson["face3"][i]["y"];
    }

    while(run_flag)
    {
        json cubeJson = json::array();

        Tile* faces[3] = {face1, face2, face3};
        for(int f=0; f<3; f++)
        {
            for(int i=0; i<8; i++)
            {
                getAverageRGB(faces[f][i], r,g,b);
                // Add raw RGB to JSON array
                cubeJson.push_back({{"r", r}, {"g", g}, {"b", b}});
            }
        }

        // Output as JSON string
        std::cout << cubeJson.dump() << std::endl;

        break; // remove or comment if you want continuous capture
    }

   // printf("PIXY2 RGB Demo Exit\n");
}

