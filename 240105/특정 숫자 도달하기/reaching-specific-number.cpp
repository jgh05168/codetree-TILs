#include <iostream>
#include <cmath>

using namespace std;

int main() {
    // 여기에 코드를 작성해주세요.
    ios::sync_with_stdio(0);
    cin.tie(0);

    int arr[11] = {0, };
    int sum = 0;
    float avg = 0;
    int cnt = 0;

    for (int i=0;i<10;i++){
        cin >> arr[i];
        if (arr[i] >= 250){
            break;
        }
        sum += arr[i];
        cnt++;
    }

    avg = (float)sum / cnt;
    
    cout << fixed;
    cout.precision(1);
    cout << sum << ' ' << avg;

    return 0;
}