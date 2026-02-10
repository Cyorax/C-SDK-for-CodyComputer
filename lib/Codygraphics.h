#include <Codyram.h>

// self-explanatory
void vid_toggle_screen_output();
void vid_toggle_vscroll();
void vid_toggle_hscroll();
void vid_toggle_row_effect();
void vid_toggle_bitmap_mode();

/*
    Returns 0 if the screen output is blanked,
    otherwise returns a non-zero value.
*/
short vid_blanking();

/*
    Returns the current screen states.
*/
short vid_screen_enabled_value();
short vid_vscroll_enabled_value();
short vid_hscroll_enabled_value();
short vid_row_effect_enabled_value();
short vid_bitmap_mode_enabled_value();
short vid_get_border_color();

// 0 - 15 for the border color
void vid_set_border_color(short color);

// 0 - 15 for each color
void vid_set_color2(short color);
void vid_set_color3(short color);
void vid_set_common_sprite_color(short color);

// 0 - 15 for the value of the current sprite bank
void vid_set_current_sprite_bank(short bank);

// 0 - 15 for each loc address corresponding to 40960 + loc * 1024
void vid_set_screen_ram_address(int loc); // RAM to specify the character that is currently displayed

// RAM to specify colors 0 and 1 for the character that is currently displayed
void vid_set_color_ram_address(int loc);

// Sets the base address of character RAM.
// Character data is stored as 4x8 pixel characters,
// with 2 bits per pixel for color information.
void vid_set_character_ram_address(int loc);

// loc corresponds to a value < 1024 to place the character
// with characterNumber on the screen
void vid_place_character_to_screen(int loc, int characterNumber);

void vid_insert_character_to_chram(
    int offset,
    short line1,
    short line2,
    short line3,
    short line4,
    short line5,
    short line6,
    short line7,
    short line8
);

void vid_insert_color_to_cram(int offset, short line1);

void vid_set_bitmapped_pixel_x_y(int x, int y);
void vid_insert_sprite_into_sprite_table(int spriteindex, int x, int y, int color, int baseadresssprite);

void vid_change_sprite_position(int spriteindex, int x, int y);

/*
    Copies the initial data of the corresponding RAM from data.lib.
    For further information see the Codyram.h documentation.
*/

// Loads 63 bytes for a 12 x 21 sprite
void copy_spritedata_from_data(int startbytedatanumber, int baseadresssprite);

// Loads 1000 bytes of character RAM
void copy_tiledata_from_data(int startbytedatanumber, int amountbytes);

// Loads 1000 bytes of color RAM
void copy_initial_colormap_from_data(int startbytedatanumber);

// Loads 1000 bytes of screen RAM
void copy_initial_charactermap_from_data(int startbytedatanumber);

// debugging function
void printnum(int loc, int num);

