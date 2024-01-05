#include <iostream>

using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    char str[10] = {'.', };

    for (int i=0;i<10;i++){
        cin >> str[i];
    }

    for (int i=sizeof(str) - 1;i>=0;i--){
        cout << str[i];
    }
    // 여기에 코드를 작성해주세요.
    return 0;
}