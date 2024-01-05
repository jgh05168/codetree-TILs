#include <iostream>
using namespace std;
int main() {
    // 여기에 코드를 작성해주세요.
    ios::sync_with_stdio(0);
    cin.tie(0);

    int arr[10];
    int cnt = 0;
    double sum = 0;

    for (int i=0;i<10;i++) {
        cin >> arr[i];
        if (arr[i] == 0) {
            break;
        }
        cnt++;
        sum += arr[i];
    }

    cout << fixed;
    cout.precision(1);
    cout << (int)sum << ' ' << sum / cnt << endl;

    return 0;
}