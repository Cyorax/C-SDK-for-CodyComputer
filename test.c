#include <Codyinput.h>
#include <Codygraphics.h>
#include <Codymath.h>

void waitforblank(){
while(vid_blanking() == 0){}
while(vid_blanking() != 0){}
}

int main (){
           int x = 12;
          {
            int x = 10;
          }

          {
            int x = 12;
          }
            vid_set_border_color(x);
       return 0;
}
