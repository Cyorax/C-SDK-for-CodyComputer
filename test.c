#include <Codyinput.h>
#include <Codygraphics.h>
#include <Codymath.h>

void waitforblank(){
while(vid_blanking() == 0){}
while(vid_blanking() != 0){}
}

int main (){
          vid_set_border_color(3);
          vid_set_character_ram_address(0);
          copy_tiledata_from_data(0,104); 
          copy_spritedata_from_data(104,16);
          copy_spritedata_from_data(167,17);
          //placement of the flag
          vid_place_character_to_screen(890,10);
          vid_place_character_to_screen(930,11);
          //Bottom line 
          for(int xi = 960;xi!=1000;xi++){
          vid_place_character_to_screen(xi,12);
          }
          while(0){
          //init score 
          vid_place_character_to_screen(0,0);
          vid_place_character_to_screen(1,0);
          vid_place_character_to_screen(2,0);
          int x = 172,y = 42;
          short notfinished = 0,jumped = 255;
          vid_insert_sprite_into_sprite_table(0,x,y,15,16);
          while(notfinished){
                x -= 1;
               if(is_E_pressed()){
                   jumped = 0;
                   vid_insert_sprite_into_sprite_table(1,x,y,15,17);
               }
               if(jumped){
                    vid_change_sprite_position(1,x,y);
                    y += 2;
               }                
               vid_change_sprite_position(0,x,42);
               if(x < 20 || y > 204){
                 vid_place_character_to_screen(0,1);
                 notfinished = 255; // finished 
                }
               waitforblank();
          }
          short abstandx = abs(x - 22),abstandy = abs(y - 204),score = 500 -(abstandx + abstandy),letze = score % 10;
          vid_place_character_to_screen(2,letze);      
          score /= 10;
          letze = score % 10;
          vid_place_character_to_screen(1,letze);
          score /= 10;
          letze = score % 10; 
          vid_place_character_to_screen(0,letze);        
         while(is_R_pressed() != 0){}
            vid_change_sprite_position(1,0,0);
        }
       return 0;
}
