#include <Codygraphics.h>
#include <Codymath.h>

int main (){
      vid_set_character_ram_address(0);
      vid_insert_character_to_chram(0,20,65,65,65,65,65,20,0);
      vid_insert_character_to_chram(1,20,4,4,4,4,4,21,0);
    for(int i = 0;i!=10;i = i + 1){
    vid_place_character_to_screen(i,0);
    }    
   return 0;
}


