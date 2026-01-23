int main() {
    int x = 1;
    {
        int x = 2;
        x = x + 1;
        while(x!=10){ 
            x+=1;
            int x = 12;
        }
    }
    return x;
}
