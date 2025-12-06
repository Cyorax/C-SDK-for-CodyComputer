#include <Codygraphics.h>
#include <Codymath.h>

int main (){
    int counter = 0;
    int counter1 = 0;
    while(counter1!=125){
    if(counter==15)
        counter = 0;
    counter = counter + 1;
    vid_set_border_color(counter);
    counter1 = counter1 + 1;    
    }
   return 0;
}
