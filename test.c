#include <Codyinput.h>
#include <Codygraphics.h>

void waitforblank(){
while(vid_blanking() == 0){}
while(vid_blanking() != 0){}
}

int main (){
          vid_set_border_color(3);
          vid_set_character_ram_address(0);
          copy_tiledata_from_data(0,24); //lade drei Tiles 
          copy_spritedata_from_data(24,16);
          int x = 100,y = 100;
          vid_insert_sprite_into_sprite_table(0,x,y,55,16);
          while(0){
            if(is_W_pressed()){
            y = --y;
            }else if(is_A_pressed()){
            x = --x;
            }else if(is_S_pressed()){
            y = ++ y;
            }else if(is_D_pressed()){
            x = ++ x;
            }
            vid_change_sprite_position(0,x,y);
            waitforblank();
          }
       return 0;
}



/*#include <Codygraphics.h>

void waitforblank(){
while(vid_blanking() == 0){}
while(vid_blanking() != 0){}
}

int main (){
        vid_set_character_ram_address(0);
        vid_set_border_color(1);
        copy_tiledata_from_data(0,24); //lade drei Tiles 
        copy_spritedata_from_data(24,16);
        vid_insert_sprite_into_sprite_table(0,100,100,55,16);

        vid_place_character_to_screen(0,0);
        vid_place_character_to_screen(1,1);
        vid_place_character_to_screen(60,2);
        vid_insert_color_to_cram(60,76);   
        int i = 21;
        while(1==1){        
        if(i==150){
        i=21;
        }
        i+=1;
        vid_change_sprite_position(0,i,i);  
        waitforblank();      
        } 
        vid_place_character_to_screen(2,2);
       return 0;
}
*/

/*
#include <Codygraphics.h>
int main (){
vid_set_border_color(3);
vid_set_character_ram_address(0);
vid_toggle_bitmap_mode();
for(int i = 80;i<140;++i){
vid_set_bitmapped_pixel_x_y(i,i)
}
vid_set_border_color(7);
}*/
