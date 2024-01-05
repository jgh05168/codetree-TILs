#include <iostream>
using namespace std;
int main() {
    // 여기에 코드를 작성해주세요.
    ios::sync_with_stdio(0);
    cin.tie(0);

    int n;
    cin >> n;
    int arr[10][4];
    int student = 0;
    int sum;
    for (int i = 0;i<n;i++) {
        sum = 0;
        for (int j = 0;j<4;j++) {
            cin >> arr[i][j];
            sum += arr[i][j];
        }
        if((double)sum / 4 >= 60) {
            cout << "pass" << '\n';
            student++;
        }
        else {
            cout << "fail" << '\n';
        }
    }

    cout << student;

    
    return 0;
}