#include<iostream>
using namespace std;
int main()
{
    int a = 10;
    // char* b = "chen";
    char* c;
    sprintf(c, "%d", a);
    cout << c << endl;
    return 0;
}