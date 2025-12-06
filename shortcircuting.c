#include <Codygraphics.h>
/* lost 


*/
int funcA() {
    vid_set_border_color(3);
    return 1;
}

int funcB() {
    vid_set_border_color(4);
    return 1;
}

int main() {
    if (funcA() && funcB()) {
        vid_set_border_color(5);
        return 1;
    }
return 0;
}

