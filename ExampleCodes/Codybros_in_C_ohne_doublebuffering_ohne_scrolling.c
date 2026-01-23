#include <Codyinput.h>
#include <Codygraphics.h>

void waitforblank(){
while(vid_blanking() == 0){}
while(vid_blanking() != 0){}
}
int x = 100;
int y = 185;

int main (){
          vid_set_border_color(3);
          vid_set_character_ram_address(0); 
          copy_spritedata_from_data(0,16);
          copy_spritedata_from_data(63,17);
          copy_spritedata_from_data(126,18);
          copy_spritedata_from_data(189,19);
          copy_tiledata_from_data(252,64);
          copy_initial_charactermap_from_data(316);
          copy_initial_colormap_from_data(1316);
          vid_set_color2(0);
          vid_set_color3(14);
          int dir = 0,frame = 0,pressed = 0;
          vid_insert_sprite_into_sprite_table(0,x,y,216,16);
          while(0){            
            if(is_A_pressed()){
                x = --x;
                dir = 1;
                pressed = 0;
            }else if(is_D_pressed()){
                x = ++ x;
                dir = 0;
                pressed = 0;
            }else{
                pressed = 255;
            }
            if(pressed)
                frame ^= 1;
            vid_insert_sprite_into_sprite_table(0,x,y,216,16+2*dir+frame);
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
