#include <Codyram.h>

void vid_toggle_screen_output(void);
void vid_toggle_vscroll(void);
void vid_toggle_hscroll(void);
void vid_toggle_row_effect(void);
void vid_toggle_bitmap_mode(void);

short vid_blanking(void);

short vid_screen_enabled_value(void);
short vid_vscroll_enabled_value(void);
short vid_hscroll_enabled_value(void);
short vid_row_effect_enabled_value(void);
short vid_bitmap_mode_enabled_value(void);

short vid_get_border_color(void);
void vid_set_border_color(short color);

void vid_set_color2(short color);
void vid_set_color3(short color);

void vid_set_common_sprite_color(short color);
void vid_set_current_sprite_bank(short bank);

void vid_set_screen_ram_address(int loc);
void vid_set_color_ram_address(int loc);
void vid_set_character_ram_address(int loc);

void vid_place_character_to_screen(int loc, int character);

void vid_insert_character_to_chram(int offset, short line1, short line2, short line3, short line4, short line5, short line6, short line7, short line8);

void vid_insert_color_to_cram(int offset, short line1);

void vid_set_bitmapped_pixel_x_y(int x, int y);

void vid_insert_sprite_into_sprite_table(int spriteindex, int x, int y, int color, int baseadresssprite);

void vid_change_sprite_position(int spriteindex, int x, int y);

void copy_spritedata_from_data(int startbytedatanumber, int baseadresssprite);

void copy_tiledata_from_data(int startbytedatanumber, int amountbytes);

void copy_initial_colormap_from_data(int startbytedatanumber);

void copy_initial_charactermap_from_data(int startbytedatanumber);

void printnum(int loc, int num);

