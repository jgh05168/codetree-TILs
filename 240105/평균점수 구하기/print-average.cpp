#include <iostream>

using namespace std;

int main() {
    // 여기에 코드를 작성해주세요.
    ios::sync_with_stdio(0);
    cin.tie(0);

    double arr[8] = {0, };
    double sum = 0;
    for (int i = 0;i < 8;i++) {
        cin >> arr[i];
        sum += arr[i];
    }

    double avg = (double)sum / 8;
    cout << fixed;
    cout.precision(1);

    cout << avg << endl;


    return 0;
}