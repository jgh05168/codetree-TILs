#include <iostream>

using namespace std;

int main() {
    // 여기에 코드를 작성해주세요.
    ios::sync_with_stdio(0);
    cin.tie(0);

    int n;
    cin >> n;

    double arr[6] = {0, };
    double sum = 0;
    for (int i=0;i<n;i++){
        cin >> arr[i];
        sum += arr[i];
    }

    double avg = (double)sum / n;

    cout << fixed;
    cout.precision(1);
    cout << avg << '\n';
    if (avg >= 4) {
        cout << "Perfect";
    }
    else if (avg >= 3 ) {
        cout << "Good";
    }
    else {
        cout << "Poor";
    }

    return 0;
}