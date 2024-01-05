#include <iostream>
using namespace std;
int main() {
    // 여기에 코드를 작성해주세요.
    ios::sync_with_stdio(0);
    cin.tie(0);

    int arr[10] = {0, };

    for (int i=0;i<10;i++){
        cin >> arr[i];
        if (arr[i] == 0) {
            break;
        }
    }

    for (int i=9;i >= 0;i--) {
        if (arr[i] == 0) {
            continue;
        }
        cout << arr[i] << ' ';
    }
    return 0;
}