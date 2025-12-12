#include <Codygraphics.h>

void loadBytesFromDataTo(int* startadressram,int startaddressdata,int amount){
int* datapointerregister = 6;
short* data = * datapointerregister;
data = data + startaddressdata;
for(int i = 0; i < amount; i = i+1){ 
    *startadressram = *data
    data = data + 1;
    startadressram = startadressram + 1;
}
}

int main (int x,int y){
        short* chram = 40960;
        vid_set_character_ram_address(0);
        
        vid_set_border_color(3);
        loadBytesFromDataTo(40960,0,8); //lade die null in chram[0]
        loadBytesFromDataTo(40968,8,8); //lade die eins in chram[1]

        vid_place_character_to_screen(0,0);
        vid_place_character_to_screen(1,1);
   return 0;
}


