#include <iostream>

using namespace std;

int main() {
    // 여기에 코드를 작성해주세요.
    cin.tie(0);
    ios::sync_with_stdio(0);
    
    int sum = 0;
    int arr[11] = {0, };


    for (int i=0;i<10;i++){
        cin >> arr[i];
        sum += arr[i];
    }

    cout << sum;
    return 0;
}