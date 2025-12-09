void vid_toggle_screen_output();
void vid_toggle_vscroll();
void vid_toggle_hscroll();
void vid_toggle_row_effect();
void vid_toggle_bitmap_mode();

short vid_blanking();
short vid_screen_enabled_value();
short vid_vscroll_enabled_value();
short vid_hscroll_enabled_value();
short vid_row_effect_enabled_value();
short vid_bitmap_mode_enabled_value();

short vid_get_border_color();
void vid_set_border_color(short color);

void vid_set_color2(short color);
void vid_set_color3(short color);

void vid_set_screen_ram_address(int loc);
void vid_set_color_ram_address(int loc);
void vid_set_character_ram_address(int loc);

void vid_place_character_to_screen(int loc, int character);

void vid_insert_character_to_chram(int offset, short line1, short line2, short line3, short line4, short line5, short line6, short line7, short line8);

void vid_insert_color_to_cram(int offset, short line1);

void vid_set_bitmapped_pixel_x_y(int x, int y, short color);

void printnum(int loc, int num);
