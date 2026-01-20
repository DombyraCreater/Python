#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cmath>
#include <numeric>
using namespace std;

int main() {
    vector<int> l1,l2,fin_vector;
    int temp1,temp2;
    int fin1=0,fin2=0;
    int fin;
    while(cin>>temp1){
        l1.push_back(temp1);
        if(cin.peek()=='\n')break;
    }
    while(cin>>temp2){
        l2.push_back(temp2);
        if(cin.peek()=='\n')break;
    }
    for (int i = l1.size()-1; i >=0; i--) {
        fin1 = fin1 * 10 + l1[i];
    }for (int i = l2.size()-1; i >=0; i--) {
        fin2 = fin2 * 10 + l2[i];
    }
    fin = fin1+fin2;
    string sum_str = to_string(fin);
    for(int i = 0;i<sum_str.length();i++){
        int temp;
        temp = fin%10;
        fin = fin/10;
        fin_vector.push_back(temp);
    }
    for(int i:fin_vector){
        cout<<i<<" ";
    }
    cout<<fin_vector.size();
    return 0;
}
